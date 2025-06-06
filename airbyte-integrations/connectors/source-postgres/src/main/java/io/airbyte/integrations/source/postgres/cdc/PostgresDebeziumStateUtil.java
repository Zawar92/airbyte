/*
 * Copyright (c) 2023 Airbyte, Inc., all rights reserved.
 */

package io.airbyte.integrations.source.postgres.cdc;

import static io.debezium.connector.postgresql.PostgresOffsetContext.LAST_COMMIT_LSN_KEY;
import static io.debezium.connector.postgresql.SourceInfo.LSN_KEY;
import static io.debezium.relational.RelationalDatabaseConnectorConfig.DATABASE_NAME;

import com.fasterxml.jackson.databind.JsonNode;
import com.google.common.annotations.VisibleForTesting;
import com.google.common.base.Preconditions;
import io.airbyte.cdk.db.PostgresUtils;
import io.airbyte.cdk.db.jdbc.JdbcDatabase;
import io.airbyte.cdk.integrations.debezium.internals.AirbyteFileOffsetBackingStore;
import io.airbyte.cdk.integrations.debezium.internals.DebeziumPropertiesManager;
import io.airbyte.cdk.integrations.debezium.internals.DebeziumStateUtil;
import io.airbyte.cdk.integrations.debezium.internals.RelationalDbDebeziumPropertiesManager;
import io.airbyte.commons.json.Jsons;
import io.airbyte.protocol.models.v0.ConfiguredAirbyteCatalog;
import io.debezium.config.Configuration;
import io.debezium.connector.common.OffsetReader;
import io.debezium.connector.postgresql.PostgresConnectorConfig;
import io.debezium.connector.postgresql.PostgresOffsetContext;
import io.debezium.connector.postgresql.PostgresOffsetContext.Loader;
import io.debezium.connector.postgresql.PostgresPartition;
import io.debezium.connector.postgresql.connection.Lsn;
import io.debezium.pipeline.spi.Offsets;
import io.debezium.pipeline.spi.Partition;
import io.debezium.time.Conversions;
import java.sql.SQLException;
import java.time.Instant;
import java.util.Collections;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Objects;
import java.util.Optional;
import java.util.OptionalLong;
import java.util.Properties;
import java.util.Set;
import org.apache.kafka.connect.storage.FileOffsetBackingStore;
import org.apache.kafka.connect.storage.OffsetStorageReaderImpl;
import org.postgresql.core.BaseConnection;
import org.postgresql.replication.LogSequenceNumber;
import org.postgresql.replication.PGReplicationStream;
import org.postgresql.replication.fluent.logical.ChainedLogicalStreamBuilder;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

/**
 * This class is inspired by Debezium's Postgres connector internal implementation on how it parses
 * the state
 */
public class PostgresDebeziumStateUtil implements DebeziumStateUtil {

  private static final Logger LOGGER = LoggerFactory.getLogger(PostgresDebeziumStateUtil.class);

  public boolean isSavedOffsetAfterReplicationSlotLSN(final JsonNode replicationSlot,
                                                      final OptionalLong savedOffset) {

    if (Objects.isNull(savedOffset) || savedOffset.isEmpty()) {
      return true;
    }

    if (replicationSlot.has("confirmed_flush_lsn")) {
      final long confirmedFlushLsnOnServerSide = Lsn.valueOf(replicationSlot.get("confirmed_flush_lsn").asText()).asLong();
      LOGGER.info("Replication slot confirmed_flush_lsn : " + confirmedFlushLsnOnServerSide + " Saved offset LSN : " + savedOffset.getAsLong());
      return savedOffset.getAsLong() >= confirmedFlushLsnOnServerSide;
    } else if (replicationSlot.has("restart_lsn")) {
      final long restartLsn = Lsn.valueOf(replicationSlot.get("restart_lsn").asText()).asLong();
      LOGGER.info("Replication slot restart_lsn : " + restartLsn + " Saved offset LSN : " + savedOffset.getAsLong());
      return savedOffset.getAsLong() >= restartLsn;
    }

    // We return true when saved offset is not present cause using an empty offset would result in sync
    // from scratch anyway
    return true;
  }

  public OptionalLong savedOffset(final Properties baseProperties,
                                  final ConfiguredAirbyteCatalog catalog,
                                  final JsonNode cdcState,
                                  final JsonNode config) {
    final var offsetManager = AirbyteFileOffsetBackingStore.initializeState(cdcState, Optional.empty());
    final DebeziumPropertiesManager debeziumPropertiesManager =
        new RelationalDbDebeziumPropertiesManager(baseProperties, config, catalog, Collections.emptyList());
    final Properties debeziumProperties = debeziumPropertiesManager.getDebeziumProperties(offsetManager);
    return parseSavedOffset(debeziumProperties);
  }

  public void commitLSNToPostgresDatabase(final JsonNode jdbcConfig,
                                          final OptionalLong savedOffset,
                                          final String slotName,
                                          final String publicationName,
                                          final String plugin) {
    if (Objects.isNull(savedOffset) || savedOffset.isEmpty()) {
      return;
    }

    final LogSequenceNumber logSequenceNumber = LogSequenceNumber.valueOf(savedOffset.getAsLong());

    LOGGER.info("Committing upto LSN: {}", savedOffset.getAsLong());
    try (final BaseConnection pgConnection = (BaseConnection) PostgresReplicationConnection.createConnection(jdbcConfig)) {
      ChainedLogicalStreamBuilder streamBuilder = pgConnection
          .getReplicationAPI()
          .replicationStream()
          .logical()
          .withSlotName("\"" + slotName + "\"")
          .withStartPosition(logSequenceNumber);

      streamBuilder = addSlotOption(publicationName, plugin, pgConnection, streamBuilder);

      try (final PGReplicationStream stream = streamBuilder.start()) {
        stream.forceUpdateStatus();

        stream.setFlushedLSN(logSequenceNumber);
        stream.setAppliedLSN(logSequenceNumber);

        stream.forceUpdateStatus();
      }
    } catch (SQLException e) {
      throw new RuntimeException(e);
    }
  }

  private ChainedLogicalStreamBuilder addSlotOption(final String publicationName,
                                                    final String plugin,
                                                    final BaseConnection pgConnection,
                                                    ChainedLogicalStreamBuilder streamBuilder) {
    if (plugin.equalsIgnoreCase("pgoutput")) {
      streamBuilder = streamBuilder.withSlotOption("proto_version", 1)
          .withSlotOption("publication_names", publicationName);

      if (pgConnection.haveMinimumServerVersion(140000)) {
        streamBuilder = streamBuilder.withSlotOption("messages", true);
      }
    } else {
      throw new RuntimeException("Unknown plugin value : " + plugin);
    }
    return streamBuilder;
  }

  /**
   * Loads the offset data from the saved Debezium offset file.
   *
   * @param properties Properties should contain the relevant properties like path to the debezium
   *        state file, etc. It's assumed that the state file is already initialised with the saved
   *        state
   * @return Returns the LSN that Airbyte has acknowledged in the source database server
   */
  private OptionalLong parseSavedOffset(final Properties properties) {
    FileOffsetBackingStore fileOffsetBackingStore = null;
    OffsetStorageReaderImpl offsetStorageReader = null;

    try {
      fileOffsetBackingStore = getFileOffsetBackingStore(properties);
      offsetStorageReader = getOffsetStorageReader(fileOffsetBackingStore, properties);

      final PostgresConnectorConfig postgresConnectorConfig = new PostgresConnectorConfig(Configuration.from(properties));
      final PostgresCustomLoader loader = new PostgresCustomLoader(postgresConnectorConfig);
      final Set<Partition> partitions =
          Collections.singleton(new PostgresPartition(postgresConnectorConfig.getLogicalName(), properties.getProperty(DATABASE_NAME.name())));

      final OffsetReader<Partition, PostgresOffsetContext, Loader> offsetReader = new OffsetReader<>(offsetStorageReader, loader);
      final Map<Partition, PostgresOffsetContext> offsets = offsetReader.offsets(partitions);

      return extractLsn(partitions, offsets, loader);
    } finally {
      LOGGER.info("Closing offsetStorageReader and fileOffsetBackingStore");
      if (offsetStorageReader != null) {
        offsetStorageReader.close();
      }

      if (fileOffsetBackingStore != null) {
        fileOffsetBackingStore.stop();
      }
    }
  }

  private OptionalLong extractLsn(final Set<Partition> partitions,
                                  final Map<Partition, PostgresOffsetContext> offsets,
                                  final PostgresCustomLoader loader) {
    boolean found = false;
    for (final Partition partition : partitions) {
      final PostgresOffsetContext postgresOffsetContext = offsets.get(partition);

      if (postgresOffsetContext != null) {
        found = true;
        LOGGER.info("Found previous partition offset {}: {}", partition, postgresOffsetContext.getOffset());
      }
    }

    if (!found) {
      LOGGER.info("No previous offsets found");
      return OptionalLong.empty();
    }

    final Offsets<Partition, PostgresOffsetContext> of = Offsets.of(offsets);
    final PostgresOffsetContext previousOffset = of.getTheOnlyOffset();

    final Map<String, ?> offset = previousOffset.getOffset();

    if (offset.containsKey(LAST_COMMIT_LSN_KEY)) {
      return OptionalLong.of((long) offset.get(LAST_COMMIT_LSN_KEY));
    } else if (offset.containsKey(LSN_KEY)) {
      return OptionalLong.of((long) offset.get(LSN_KEY));
    } else if (loader.getRawOffset().containsKey(LSN_KEY)) {
      return OptionalLong.of(Long.parseLong(loader.getRawOffset().get(LSN_KEY).toString()));
    }

    return OptionalLong.empty();

  }

  private static ThreadLocal<JsonNode> initialState = new ThreadLocal<>();

  /**
   * Method to construct initial Debezium state which can be passed onto Debezium engine to make it
   * process WAL from a specific LSN and skip snapshot phase
   */
  public JsonNode constructInitialDebeziumState(final JdbcDatabase database, final String dbName) {
    if (initialState.get() == null) {
      try {
        final JsonNode asJson = format(currentXLogLocation(database), currentTransactionId(database), dbName, Instant.now());
        initialState.set(asJson);
      } catch (SQLException e) {
        throw new RuntimeException(e);
      }
    }
    return initialState.get();
  }

  @VisibleForTesting
  public JsonNode format(final Long currentXLogLocation, final Long currentTransactionId, final String dbName, final Instant time) {
    final String key = "[\"" + dbName + "\",{\"server\":\"" + dbName + "\"}]";
    final String value =
        "{\"transaction_id\":null,\"lsn\":" + currentXLogLocation + ",\"txId\":" + currentTransactionId + ",\"ts_usec\":" + Conversions.toEpochMicros(
            time) + "}";

    final Map<String, String> result = new HashMap<>();
    result.put(key, value);

    final JsonNode jsonNode = Jsons.jsonNode(result);
    LOGGER.info("Initial Debezium state constructed: {}", jsonNode);

    return jsonNode;
  }

  private long currentXLogLocation(JdbcDatabase database) throws SQLException {
    return PostgresUtils.getLsn(database).asLong();
  }

  private Long currentTransactionId(final JdbcDatabase database) throws SQLException {
    final List<Long> transactionId = database.bufferedResultSetQuery(
        conn -> conn.createStatement().executeQuery(
            "SELECT CASE WHEN pg_is_in_recovery() THEN txid_snapshot_xmin(txid_current_snapshot()) ELSE txid_current() END AS pg_current_txid;"),
        resultSet -> resultSet.getLong(1));
    Preconditions.checkState(transactionId.size() == 1);
    return transactionId.get(0);
  }

  public static void disposeInitialState() {
    LOGGER.debug("Dispose initial state cached for {}", Thread.currentThread());
    initialState.remove();
  }

}
