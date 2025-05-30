# Okta

Okta is the complete identity solution for all your apps and people that’s universal, reliable, and easy

## Prerequisites

- Created Okta account with added application on [Add Application Page](https://okta-domain.okta.com/enduser/catalog) page. (change okta-domain to your domain received after complete registration)

## Airbyte Open Source

- Name
- Okta-Domain
- Start Date
- Personal Api Token (look [here](https://developer.okta.com/docs/guides/find-your-domain/-/main/) to find it)

## Airbyte Cloud

- Name
- Start Date
- Client ID (received when application was added).
- Client Secret (received when application was added).
- Refresh Token (received when application was added)

## Setup guide

### Step 1: Set up Okta

1. Create account on Okta by following link [signup](https://www.okta.com/free-trial/)
2. Confirm your Email
3. Choose authorization method (Application or SMS)
4. Add application in your [Dashboard](https://okta-domain.okta.com/app/UserHome)

### For Airbyte Cloud:

1. [Log into your Airbyte Cloud](https://cloud.airbyte.com/workspaces) account.
2. In the left navigation bar, click **Sources**. In the top-right corner, click **+ new source**.
3. On the source setup page, select **Okta** from the Source type dropdown and enter a name for this connector.
4. Add **Name**
5. Add **Okta Domain** (If your Okta URL is `https://MY_DOMAIN.okta.com/`, then `MY_DOMAIN` is your Okta domain.)
6. Add **Start date** (defaults to 7 days if no date is included)
7. Choose the method of authentication
8. If you select Token authentication - fill the field **Personal Api Token**
9. If you select OAuth2.0 authorization - fill the fields **Client ID**, **Client Secret**, **Refresh Token**
10. Click `Set up source`.

### For Airbyte Open Source:

1. Go to local Airbyte page.
2. Use API token from requirements and Okta [domain](https://developer.okta.com/docs/guides/find-your-domain/-/main/).
3. Go to local Airbyte page.
4. In the left navigation bar, click **Sources**. In the top-right corner, click **+ new source**.
5. On the Set up the source page select **Okta** from the Source type dropdown.
6. Add **Name**
7. Add **Okta-Domain**
8. Add **Start date**
9. Paste all data to required fields fill the fields **Client ID**, **Client Secret**, **Refresh Token**
10. Click `Set up source`.

## Supported sync modes

The Okta source connector supports the following [sync modes](https://docs.airbyte.com/cloud/core-concepts#connection-sync-modes):

- Full Refresh
- Incremental

## Supported Streams

- [Users](https://developer.okta.com/docs/reference/api/users/#list-users)
- [User Role Assignments](https://developer.okta.com/docs/reference/api/roles/#list-roles-assigned-to-a-user)
- [Groups](https://developer.okta.com/docs/reference/api/groups/#list-groups)
- [Group Members](https://developer.okta.com/docs/reference/api/groups/#list-group-members)
- [Group Role Assignments](https://developer.okta.com/docs/reference/api/roles/#list-roles-assigned-to-a-group)
- [System Log](https://developer.okta.com/docs/reference/api/system-log/#get-started)
- [Custom Roles](https://developer.okta.com/docs/reference/api/roles/#list-roles)
- [Permissions](https://developer.okta.com/docs/reference/api/roles/#list-permissions)
- [Resource Sets](https://developer.okta.com/docs/reference/api/roles/#list-resource-sets)

## Performance considerations

The connector is restricted by normal Okta [requests limitation](https://developer.okta.com/docs/reference/rate-limits/).

## Changelog

<details>
  <summary>Expand to review</summary>

| Version | Date       | Pull Request                                             | Subject                                                                        |
|:--------|:-----------|:---------------------------------------------------------|:-------------------------------------------------------------------------------|
| 0.3.21 | 2025-02-24 | [54167](https://github.com/airbytehq/airbyte/pull/54167) | Remove stream_state interpolation |
| 0.3.20 | 2025-02-01 | [52728](https://github.com/airbytehq/airbyte/pull/52728) | Update dependencies |
| 0.3.19 | 2025-01-25 | [52469](https://github.com/airbytehq/airbyte/pull/52469) | Update dependencies |
| 0.3.18 | 2025-01-18 | [51920](https://github.com/airbytehq/airbyte/pull/51920) | Update dependencies |
| 0.3.17 | 2025-01-11 | [51170](https://github.com/airbytehq/airbyte/pull/51170) | Update dependencies |
| 0.3.16 | 2025-01-04 | [50899](https://github.com/airbytehq/airbyte/pull/50899) | Update dependencies |
| 0.3.15 | 2024-12-28 | [50670](https://github.com/airbytehq/airbyte/pull/50670) | Update dependencies |
| 0.3.14 | 2024-12-21 | [50073](https://github.com/airbytehq/airbyte/pull/50073) | Update dependencies |
| 0.3.13 | 2024-12-14 | [49264](https://github.com/airbytehq/airbyte/pull/49264) | Starting with this version, the Docker image is now rootless. Please note that this and future versions will not be compatible with Airbyte versions earlier than 0.64 |
| 0.3.12 | 2024-12-12 | [49145](https://github.com/airbytehq/airbyte/pull/49145) | Update dependencies |
| 0.3.11 | 2024-11-04 | [47900](https://github.com/airbytehq/airbyte/pull/47900) | Update dependencies |
| 0.3.10 | 2024-10-28 | [47058](https://github.com/airbytehq/airbyte/pull/47058) | Update dependencies |
| 0.3.9 | 2024-10-12 | [46804](https://github.com/airbytehq/airbyte/pull/46804) | Update dependencies |
| 0.3.8 | 2024-10-05 | [46481](https://github.com/airbytehq/airbyte/pull/46481) | Update dependencies |
| 0.3.7 | 2024-09-28 | [46148](https://github.com/airbytehq/airbyte/pull/46148) | Update dependencies |
| 0.3.6 | 2024-09-21 | [45763](https://github.com/airbytehq/airbyte/pull/45763) | Update dependencies |
| 0.3.5 | 2024-09-14 | [45543](https://github.com/airbytehq/airbyte/pull/45543) | Update dependencies |
| 0.3.4 | 2024-09-07 | [45319](https://github.com/airbytehq/airbyte/pull/45319) | Update dependencies |
| 0.3.3 | 2024-08-31 | [44977](https://github.com/airbytehq/airbyte/pull/44977) | Update dependencies |
| 0.3.2 | 2024-08-24 | [44741](https://github.com/airbytehq/airbyte/pull/44741) | Update dependencies |
| 0.3.1 | 2024-08-17 | [44332](https://github.com/airbytehq/airbyte/pull/44332) | Update dependencies |
| 0.3.0 | 2024-08-13 | [43382](https://github.com/airbytehq/airbyte/pull/43382) | Support OAuth 2.0 with private key |
| 0.2.11 | 2024-08-12 | [43820](https://github.com/airbytehq/airbyte/pull/43820) | Update dependencies |
| 0.2.10 | 2024-08-10 | [43672](https://github.com/airbytehq/airbyte/pull/43672) | Update dependencies |
| 0.2.9 | 2024-08-03 | [43279](https://github.com/airbytehq/airbyte/pull/43279) | Update dependencies |
| 0.2.8 | 2024-07-27 | [42739](https://github.com/airbytehq/airbyte/pull/42739) | Update dependencies |
| 0.2.7 | 2024-07-20 | [42284](https://github.com/airbytehq/airbyte/pull/42284) | Update dependencies |
| 0.2.6 | 2024-07-13 | [41756](https://github.com/airbytehq/airbyte/pull/41756) | Update dependencies |
| 0.2.5 | 2024-07-10 | [41269](https://github.com/airbytehq/airbyte/pull/41269) | Update dependencies |
| 0.2.4 | 2024-07-06 | [40904](https://github.com/airbytehq/airbyte/pull/40904) | Update dependencies |
| 0.2.3 | 2024-06-25 | [40316](https://github.com/airbytehq/airbyte/pull/40316) | Update dependencies |
| 0.2.2 | 2024-06-22 | [40002](https://github.com/airbytehq/airbyte/pull/40002) | Update dependencies |
| 0.2.1 | 2024-06-04 | [39016](https://github.com/airbytehq/airbyte/pull/39016) | [autopull] Upgrade base image to v1.2.1 |
| 0.2.0 | 2024-05-16 | [36509](https://github.com/airbytehq/airbyte/pull/36509) | Migrate to Low Code |
| 0.1.16 | 2023-07-07 | [20833](https://github.com/airbytehq/airbyte/pull/20833) | Fix infinite loop for GroupMembers stream |
| 0.1.15 | 2023-06-20 | [27533](https://github.com/airbytehq/airbyte/pull/27533) | Fixed group member stream and resource sets stream pagination |
| 0.1.14 | 2022-12-24 | [20877](https://github.com/airbytehq/airbyte/pull/20877) | Disabled OAuth2.0 authorization method |
| 0.1.13 | 2022-08-12 | [14700](https://github.com/airbytehq/airbyte/pull/14700) | Add resource sets |
| 0.1.12 | 2022-08-05 | [15050](https://github.com/airbytehq/airbyte/pull/15050) | Add parameter `start_date` for Logs stream |
| 0.1.11 | 2022-08-03 | [14739](https://github.com/airbytehq/airbyte/pull/14739) | Add permissions for custom roles |
| 0.1.10 | 2022-08-01 | [15179](https://github.com/airbytehq/airbyte/pull/15179) | Fix broken schemas for all streams |
| 0.1.9 | 2022-07-25 | [15001](https://github.com/airbytehq/airbyte/pull/15001) | Return deprovisioned users |
| 0.1.8 | 2022-07-19 | [14710](https://github.com/airbytehq/airbyte/pull/14710) | Implement OAuth2.0 authorization method |
| 0.1.7 | 2022-07-13 | [14556](https://github.com/airbytehq/airbyte/pull/14556) | Add User_Role_Assignments and Group_Role_Assignments streams (full fetch only) |
| 0.1.6 | 2022-07-11 | [14610](https://github.com/airbytehq/airbyte/pull/14610) | Add custom roles stream |
| 0.1.5 | 2022-07-04 | [14380](https://github.com/airbytehq/airbyte/pull/14380) | Add Group_Members stream to okta source |
| 0.1.4 | 2021-11-02 | [7584](https://github.com/airbytehq/airbyte/pull/7584) | Fix incremental params for log stream |
| 0.1.3 | 2021-09-08 | [5905](https://github.com/airbytehq/airbyte/pull/5905) | Fix incremental stream defect |
| 0.1.2 | 2021-07-01 | [4456](https://github.com/airbytehq/airbyte/pull/4456) | Fix infinite pagination in logs stream |
| 0.1.1   | 2021-06-09 | [3937](https://github.com/airbytehq/airbyte/pull/3973)   | Add `AIRBYTE_ENTRYPOINT` env variable for kubernetes support                   |
| 0.1.0   | 2021-05-30 | [3563](https://github.com/airbytehq/airbyte/pull/3563)   | Initial Release                                                                |

</details>
