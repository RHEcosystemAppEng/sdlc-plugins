# Step 4.5 -- Affects Version Resolution

## 4.5.1 -- Check Existing Field

The bug's `affectsVersions` field is **empty** (recorded as "(none)" in Step 1). No existing versions are set on ACME-510, so there is nothing to keep, replace, or augment. Proceeding to version extraction.

## 4.5.2 -- Extract Version from Description

Parsing the **Environment / Version** section extracted in Step 1:

```
Product version: 0.9.0
OS: RHEL 9.2
Deployment: OpenShift 4.14
```

Identified version pattern: **`0.9.0`** (extracted from "Product version: 0.9.0").

This is an explicit semantic version number matching the pattern `X.Y.Z`.

## 4.5.3 -- Discover Available Jira Versions

Available Jira versions for project ACME (retrieved via `jira.getJiraIssueTypeMetaWithFields`):

| Jira ID | Name          | Released | Release Date |
|---------|---------------|----------|--------------|
| 62643   | RHTPA 0.9.0   | yes      | 2025-06-15   |
| 62644   | RHTPA 1.0.0   | yes      | 2025-09-01   |
| 62645   | RHTPA 1.1.0   | no       | 2026-01-15   |

## 4.5.4 -- Match

Comparing extracted version `0.9.0` against available Jira version names using substring matching:

- `0.9.0` is a substring of `RHTPA 0.9.0` -- **MATCH**
- `0.9.0` is NOT a substring of `RHTPA 1.0.0` -- no match
- `0.9.0` is NOT a substring of `RHTPA 1.1.0` -- no match

**Single match found**: RHTPA 0.9.0 (ID: 62643)

## 4.5.5 -- Confirm with User

The following confirmation prompt would be presented to the user:

```
Extracted version info: "0.9.0"
Matched Jira version: RHTPA 0.9.0 (ID: 62643)

Set this as the Affects Version on ACME-510? (yes/no/skip)
```

- **yes**: Update the Affects Version field on ACME-510 by calling:
  ```
  jira.edit_issue("ACME-510", fields={
    "versions": [{"id": "62643"}]
  })
  ```
- **no**: Ask the user to select from the available versions list, or enter a version manually.
- **skip**: Skip Affects Version setting entirely and proceed to Step 5.

## 4.5.6 -- Gap Flagging

Not applicable -- a version was successfully extracted from the description and matched against an available Jira version.
