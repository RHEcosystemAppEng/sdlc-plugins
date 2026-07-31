# Step 4.5 -- Affects Version Resolution

## 4.5.1 -- Check Existing Field

The bug's `affectsVersions` field is **not populated** -- recorded as "(none)" in Step 1 metadata extraction. Since the field is empty, there is no existing value to keep, replace, or augment. Proceeding directly to version extraction.

## 4.5.2 -- Extract Version from Description

Parsing the **Environment / Version** section extracted in Step 1:

```
Product version: 0.9.0
OS: RHEL 9.2
Deployment: OpenShift 4.14
```

Extracted version identifier: **0.9.0**

Source: the line "Product version: 0.9.0" contains an explicit version number pattern (`0.9.0`).

The OS and Deployment lines provide environment context but are not product version identifiers.

## 4.5.3 -- Discover Available Jira Versions

Available Jira versions for project ACME (retrieved via `jira.getJiraIssueTypeMetaWithFields` or `get_versions`):

| Jira ID | Name          | Released | Release Date |
|---------|---------------|----------|--------------|
| 62643   | RHTPA 0.9.0   | yes      | 2025-06-15   |
| 62644   | RHTPA 1.0.0   | yes      | 2025-09-01   |
| 62645   | RHTPA 1.1.0   | no       | 2026-01-15   |

## 4.5.4 -- Match

Comparing extracted version text "0.9.0" against available Jira version names using substring matching:

- "0.9.0" matches **RHTPA 0.9.0** (ID: 62643) -- substring "0.9.0" found in "RHTPA 0.9.0"
- "0.9.0" does not match "RHTPA 1.0.0" -- no substring match
- "0.9.0" does not match "RHTPA 1.1.0" -- no substring match

Single match found: **RHTPA 0.9.0** (ID: 62643)

## 4.5.5 -- Confirm with User

The following confirmation prompt would be presented to the user:

```
Extracted version info: "0.9.0"
Matched Jira version: RHTPA 0.9.0 (ID: 62643)

Set this as the Affects Version on ACME-510? (yes/no/skip)
```

Upon user confirmation ("yes"), the following Jira update would be executed:

```
jira.edit_issue(ACME-510, fields={
  "versions": [{"id": "62643"}]
})
```

This sets the Affects Version/s field on ACME-510 to "RHTPA 0.9.0".
