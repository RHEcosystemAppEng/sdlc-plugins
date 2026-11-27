# Changes Log — Project Configuration

## Added

| Section | Change |
|---|---|
| Repository Registry | New row: `trustify-ui` / `TypeScript frontend` / `serena_ui` / `/home/user/trustify-ui` |
| Code Intelligence > Limitations | New entry: `` `serena_ui`: No known limitations `` |

## Preserved (no changes)

| Section | Content kept exactly as it was |
|---|---|
| Repository Registry | `trustify-backend` row (Rust backend service, serena_backend, /home/user/trustify-backend) |
| Jira Configuration | Project key TC, Cloud ID 2b9e35e3-6bd3-4cec-b838-f4249ee02432, Feature issue type ID 10142, Git Pull Request field customfield_10875, GitHub Issue field customfield_10747 |
| Code Intelligence | Naming-convention text and the `serena_backend` find_symbol example (still the first Registry instance) |
| Code Intelligence > Limitations | `serena_backend`: rust-analyzer may take 30-60 seconds to index on first use |
| Bug Configuration | Bug issue type ID 10001, Bug template docs/bug-template.md, link type Blocks |
| Non-config content | `# trustify-backend` title and `## Documentation` section (outside Project Configuration, not touched) |

## Not added

| Section | Reason |
|---|---|
| Security Configuration | The user declined to enable security triage |
| Hierarchy Configuration | Missing from the input. It needs Jira hierarchy discovery (not allowed in this eval) and a user choice of grouping strategy (not given). Deferred instead of inventing a value |
| Jira Field Defaults | Missing from the input. It needs Jira field metadata discovery (not allowed in this eval) and user choices (not given). Deferred instead of inventing values |

## Removed or overwritten

None.
