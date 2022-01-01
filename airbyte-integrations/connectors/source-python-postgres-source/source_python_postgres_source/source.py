#
# Copyright (c) 2021 Airbyte, Inc., all rights reserved.
#


import json
from datetime import datetime, timedelta
from typing import Dict, Generator
from typing import Iterable, Mapping

from airbyte_cdk.logger import AirbyteLogger
from airbyte_cdk.models import (
    AirbyteCatalog,
    AirbyteConnectionStatus,
    AirbyteMessage,
    AirbyteRecordMessage,
    AirbyteStream,
    ConfiguredAirbyteCatalog,
    Status,
    Type,
)
from airbyte_cdk.sources import Source
from . import connection_list
import psycopg2 as psycopg2
from psycopg2.extensions import STATUS_BEGIN, STATUS_READY


class SourcePythonPostgresSource(Source):

    def check(self, logger: AirbyteLogger, config: json) -> AirbyteConnectionStatus:
        """
        Tests if the input configuration can be used to successfully connect to the integration
            e.g: if a provided Stripe API token can be used to connect to the Stripe API.

        :param logger: Logging object to display debug/info/error to the logs
            (logs will not be accessible via airbyte UI if they are not passed to this logger)
        :param config: Json object containing the configuration of this source, content of this json is as specified in
        the properties of the spec.json file

        :return: AirbyteConnectionStatus indicating a Success or Failure
        """
        global driver
        try:
            input_host = config["host"]
            input_port = config["port"]
            input_database = config["database"]
            input_username = config["username"]
            input_password = config["password"]
            if input_host in connection_list.HOST_LIST and \
               input_port in connection_list.PORT_LIST and \
               input_database in connection_list.DATABASE_LIST and \
               input_username in connection_list.USERNAME_LIST and \
               input_password in connection_list.PASSWORD_LIST:

                driver = 'postgres://' + input_username\
                                       + ':' + input_password\
                                       + '@' + input_host\
                                       + ':' + input_port\
                                       + '/' + input_database
                postgresconnection = psycopg2.connect(driver)
                if postgresconnection.status == STATUS_READY:
                    return AirbyteConnectionStatus(status=Status.SUCCEEDED)
            else:
                return AirbyteConnectionStatus(status=Status.FAILED, message=f"An exception occurred")
        except Exception as e:
            return AirbyteConnectionStatus(status=Status.FAILED, message=f"An exception occurred: {str(e)}")

    def discover(self, logger: AirbyteLogger, config: json) -> AirbyteCatalog:
        """
        Returns an AirbyteCatalog representing the available streams and fields in this integration.
        For example, given valid credentials to a Postgres database,
        returns an Airbyte catalog where each postgres table is a stream, and each table column is a field.

        :param logger: Logging object to display debug/info/error to the logs
            (logs will not be accessible via airbyte UI if they are not passed to this logger)
        :param config: Json object containing the configuration of this source, content of this json is as specified in
        the properties of the spec.json file

        :return: AirbyteCatalog is an object describing a list of all available streams in this source.
            A stream is an AirbyteStream object that includes:
            - its stream name (or table name in the case of Postgres)
            - json_schema providing the specifications of expected schema for this stream (a list of columns described
            by their names and types)
        """

        streams = []
        print(streams)
        stream_name = "states"  # Example
        json_schema = {
            # Example
            "type": "object",
            "properties": {"date": {"type": "string"},
                           "state_name": {"type": "string"},
                           "incidence_value": {"type": "float"},
                           "state_population": {"type": "float"},
                           "date_end_incidence": {"type": "string"},
                           "date_start_incidence": {"type": "string"}},
        }
        # Not Implemented
        streams.append(AirbyteStream(name=stream_name, json_schema=json_schema))
        # [States(state=config["state"])]
        return AirbyteCatalog(streams=streams)

    def main_table_struct(self,):
        data = {
            "date": "",
            "date_start_incidence": "",
            "date_end_incidence": "",
            "state_name": "",
            "state_population": "",
            "incidence_value": ""
        }
        return data

    def set_main_table(self, config):
        data_list = []
        # current_date = datetime.now().date() - timedelta(30)
        driver = 'postgres://' \
                 + config['username'] \
                 + ':' + config['password'] \
                 + '@' + config['host'] \
                 + ':' + config['port'] \
                 + '/' + config['database']
        postgres_connection = psycopg2.connect(driver)
        postgres_cursor = postgres_connection.cursor()
        # if postgres_connection.status == STATUS_READY:
        postgres_cursor.execute('SELECT date, state_name, incidence_value, state_population, date_end_incidence, date_start_incidence FROM states')
        rows = postgres_cursor.fetchall()
        for row in rows:
            data1 = self.main_table_struct()
            data1["date"] = row[0]
            data1["state_name"] = row[1]
            data1["incidence_value"] = row[2]
            data1["state_population"] = row[3]
            data1["date_end_incidence"] = row[4]
            data1["date_start_incidence"] = row[5]
            data_list.append(data1.copy())
        postgres_cursor.close()
        postgres_connection.close()
        return data_list

    def read(
        self, logger: AirbyteLogger, config: json, catalog: ConfiguredAirbyteCatalog, state: Dict[str, any]
    ) -> Generator[AirbyteMessage, None, None]:
        """
        Returns a generator of the AirbyteMessages generated by reading the source with the given configuration,
        catalog, and state.

        :param logger: Logging object to display debug/info/error to the logs
            (logs will not be accessible via airbyte UI if they are not passed to this logger)
        :param config: Json object containing the configuration of this source, content of this json is as specified in
            the properties of the spec.json file
        :param catalog: The input catalog is a ConfiguredAirbyteCatalog which is almost the same as AirbyteCatalog
            returned by discover(), but
        in addition, it's been configured in the UI! For each particular stream and field, there may have been provided
        with extra modifications such as: filtering streams and/or columns out, renaming some entities, etc
        :param state: When a Airbyte reads data from a source, it might need to keep a checkpoint cursor to resume
            replication in the future from that saved checkpoint.
            This is the object that is provided with state from previous runs and avoid replicating the entire set of
            data everytime.

        :return: A generator that produces a stream of AirbyteRecordMessage contained in AirbyteMessage object.
        """
        stream_name = "states"  # Example
        data = self.set_main_table(config)
        # data = {"date": data}  # Example
        # Not Implemented
        for x in data:
            yield AirbyteMessage(
                type=Type.RECORD,
                record=AirbyteRecordMessage(stream=stream_name, data=x, emitted_at=int(datetime.now().timestamp()) * 1000),
            )
