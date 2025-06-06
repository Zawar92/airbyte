# Northpass LMS

This page contains the setup guide and reference information for the Northpass LMS source connector.

## Prerequisites

- A [Northpass LMS Account](https://www.northpass.com) at least
<!-- env:oss -->
- A Northpass API Token generated [here](https://developers.northpass.com/docs/api-authentication)
  <!-- /env:oss -->

## Setup guide

<!-- env:oss -->

### Step 1: (For Airbyte Open Source) Setup a Northpass LMS Account

Setup and account in [Northpass](https://www.northpass.com/). 


### Step 2: (For Airbyte Open Source) Obtain an api key

A simple api key is all that is needed to access the Northpass LMS API. This token is generated [here](https://developers.northpass.com/docs/api-authentication).


#### For Airbyte Cloud:

To set up Northpass LMS as a source in Airbyte Cloud:

1. [Log in to your Airbyte Cloud](https://cloud.airbyte.com/workspaces) account.
2. In the left navigation bar, click **Sources**. In the top-right corner, click **+ New source**.
3. Find and select **Northpass LMS** from the list of available sources.
4. Enter a **Source name** of your choosing.
5. Enter the **api key** you obtained from Northpass LMS.
6. Click **Set up source** and wait for the tests to complete.

<!-- /env:cloud -->

<!-- env:oss -->

#### For Airbyte Open Source:

To set up Northpass LMS as a source in Airbyte Open Source:

1. Log in to your Airbyte Open Source account.
2. In the left navigation bar, click **Sources**. In the top-right corner, click **+ New source**.
3. Find and select **Northpass LMS** from the list of available sources.
4. Enter a **Source name** of your choosing.
5. Enter the **api key** you obtained from Northpass LMS.
6. Click **Set up source** and wait for the tests to complete.

<!-- /env:oss -->

## Supported Sync Modes

The Northpass LMS source connector supports the following [sync modes](https://docs.airbyte.com/cloud/core-concepts#connection-sync-modes):

- [Full Refresh - Overwrite](https://docs.airbyte.com/understanding-airbyte/connections/full-refresh-overwrite/)
- [Full Refresh - Append](https://docs.airbyte.com/understanding-airbyte/connections/full-refresh-append)

Incremental modes are not supported as the Northpass LMS API at the time of this writing.

## Supported Streams

The Northpass LMS source connector can sync the following streams.

### Main Tables

Link to Northpass LMS API documentation [here](https://developers.northpass.com/docs/).

- [People](https://developers.northpass.com/reference/get_v2-people)

- [Courses](https://developers.northpass.com/reference/get_v2-courses)

- [Course Enrollments](https://developers.northpass.com/reference/get_v2-courses-course-uuid-enrollments)

## Changelog

<details>
  <summary>Expand to review</summary>

| Version  | Date       | Pull Request                                             | Subject                                                                                                                              |
|:---------|:-----------|:---------------------------------------------------------|:-------------------------------------------------------------------------------------------------------------------------------------|
| 0.2.24 | 2025-05-10 | [60156](https://github.com/airbytehq/airbyte/pull/60156) | Update dependencies |
| 0.2.23 | 2025-05-03 | [59487](https://github.com/airbytehq/airbyte/pull/59487) | Update dependencies |
| 0.2.22 | 2025-04-27 | [58530](https://github.com/airbytehq/airbyte/pull/58530) | Update dependencies |
| 0.2.21 | 2025-04-12 | [57915](https://github.com/airbytehq/airbyte/pull/57915) | Update dependencies |
| 0.2.20 | 2025-04-05 | [57305](https://github.com/airbytehq/airbyte/pull/57305) | Update dependencies |
| 0.2.19 | 2025-03-29 | [56727](https://github.com/airbytehq/airbyte/pull/56727) | Update dependencies |
| 0.2.18 | 2025-03-22 | [56204](https://github.com/airbytehq/airbyte/pull/56204) | Update dependencies |
| 0.2.17 | 2025-03-08 | [55515](https://github.com/airbytehq/airbyte/pull/55515) | Update dependencies |
| 0.2.16 | 2025-03-01 | [54763](https://github.com/airbytehq/airbyte/pull/54763) | Update dependencies |
| 0.2.15 | 2025-02-22 | [54294](https://github.com/airbytehq/airbyte/pull/54294) | Update dependencies |
| 0.2.14 | 2025-02-15 | [53799](https://github.com/airbytehq/airbyte/pull/53799) | Update dependencies |
| 0.2.13 | 2025-02-08 | [53287](https://github.com/airbytehq/airbyte/pull/53287) | Update dependencies |
| 0.2.12 | 2025-02-01 | [52768](https://github.com/airbytehq/airbyte/pull/52768) | Update dependencies |
| 0.2.11 | 2025-01-25 | [52223](https://github.com/airbytehq/airbyte/pull/52223) | Update dependencies |
| 0.2.10 | 2025-01-18 | [51832](https://github.com/airbytehq/airbyte/pull/51832) | Update dependencies |
| 0.2.9 | 2025-01-11 | [51219](https://github.com/airbytehq/airbyte/pull/51219) | Update dependencies |
| 0.2.8 | 2024-12-28 | [50606](https://github.com/airbytehq/airbyte/pull/50606) | Update dependencies |
| 0.2.7 | 2024-12-21 | [50125](https://github.com/airbytehq/airbyte/pull/50125) | Update dependencies |
| 0.2.6 | 2024-12-14 | [49625](https://github.com/airbytehq/airbyte/pull/49625) | Update dependencies |
| 0.2.5 | 2024-12-12 | [49221](https://github.com/airbytehq/airbyte/pull/49221) | Update dependencies |
| 0.2.4 | 2024-12-11 | [48907](https://github.com/airbytehq/airbyte/pull/48907) | Starting with this version, the Docker image is now rootless. Please note that this and future versions will not be compatible with Airbyte versions earlier than 0.64 |
| 0.2.3 | 2024-11-04 | [48257](https://github.com/airbytehq/airbyte/pull/48257) | Update dependencies |
| 0.2.2 | 2024-10-29 | [47863](https://github.com/airbytehq/airbyte/pull/47863) | Update dependencies |
| 0.2.1 | 2024-10-28 | [47520](https://github.com/airbytehq/airbyte/pull/47520) | Update dependencies |
| 0.2.0 | 2024-08-26 | [44771](https://github.com/airbytehq/airbyte/pull/44771) | Refactor connector to manifest-only format |
| 0.1.4 | 2024-08-24 | [44684](https://github.com/airbytehq/airbyte/pull/44684) | Update dependencies |
| 0.1.3 | 2024-08-17 | [44231](https://github.com/airbytehq/airbyte/pull/44231) | Update dependencies |
| 0.1.2 | 2024-08-12 | [43867](https://github.com/airbytehq/airbyte/pull/43867) | Update dependencies |
| 0.1.1 | 2024-08-10 | [43484](https://github.com/airbytehq/airbyte/pull/43484) | Update dependencies |
| 0.1.0 | 2024-08-06 | [43319](https://github.com/airbytehq/airbyte/pull/43319) | New Source: Northpass LMS |
</details>
