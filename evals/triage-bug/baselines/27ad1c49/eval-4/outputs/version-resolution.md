# Step 4.5 -- Affects Version Resolution

## 4.5.1 -- Check Existing Field

The bug's `Affects Version/s` field is **(none)** -- the field is empty. No existing versions are set.

Since the field is not populated, there is nothing to keep, replace, or augment. Skipping the keep/replace/augment prompt and proceeding to sub-step 4.5.2.

## 4.5.2 -- Extract Version from Description

Parsing the **Environment / Version** section extracted in Step 1:

```
Product version: 0.9.0
OS: RHEL 9.2
Deployment: OpenShift 4.14
```

Extracted version identifier: **0.9.0**

Source: the line `Product version: 0.9.0` contains an explicit version number matching the pattern `<major>.<minor>.<patch>`.

## 4.5.3 -- Discover Available Jira Versions

Available Jira versions for project ACME (retrieved via `jira.getJiraIssueTypeMetaWithFields`):

| Jira ID | Name          | Released | Release Date |
|---------|---------------|----------|--------------|
| 62643   | RHTPA 0.9.0   | yes      | 2025-06-15   |
| 62644   | RHTPA 1.0.0   | yes      | 2025-09-01   |
| 62645   | RHTPA 1.1.0   | no       | 2026-01-15   |

## 4.5.4 -- Match

Comparing extracted version text **"0.9.0"** against available Jira version names using substring matching:

- `RHTPA 0.9.0` -- contains substring "0.9.0" -- **MATCH**
- `RHTPA 1.0.0` -- does not contain "0.9.0" -- no match
- `RHTPA 1.1.0` -- does not contain "0.9.0" -- no match

**Single match found**: RHTPA 0.9.0 (ID: 62643)

## 4.5.5 -- Confirm with User

The following confirmation prompt would be presented to the user:

```
Extracted version info: "0.9.0"
Matched Jira version: RHTPA 0.9.0 (ID: 62643)

Set this as the Affects Version on ACME-510? (yes/no/skip)
```

- **yes**: Update the Affects Version field on ACME-510 with:
  ```
  jira.edit_issue("ACME-510", fields={
    "versions": [{"id": "62643"}]
  })
  ```
- **no**: Ask the user to select from the available versions list, or enter a version manually.
- **skip**: Skip Affects Version setting entirely and proceed to Step 5.
