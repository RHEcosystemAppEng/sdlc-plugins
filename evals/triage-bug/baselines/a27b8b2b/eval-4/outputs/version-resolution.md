# Step 4.5 -- Affects Version Resolution: ACME-510

## 4.5.1 -- Check Existing Field

The bug's `affectsVersions` field is **empty** (not populated). Recorded in Step 1 as "(none)".

Since the field is not already set, there is no need to prompt the user to keep, replace, or augment. Proceeding to extract version from the description.

## 4.5.2 -- Extract Version from Description

Parsing the **Environment / Version** section extracted in Step 1:

```
Product version: 0.9.0
OS: RHEL 9.2
Deployment: OpenShift 4.14
```

Extracted version identifier: **0.9.0**

Pattern matched: explicit version number `0.9.0` following the "Product version:" label.

## 4.5.3 -- Discover Available Jira Versions

Called `getJiraIssueTypeMetaWithFields` for project ACME, issue type ID 10020 to retrieve the `versions` field's `allowedValues`.

Available Jira versions:

| Jira ID | Name          | Released | Release Date |
|---------|---------------|----------|--------------|
| 62643   | RHTPA 0.9.0   | yes      | 2025-06-15   |
| 62644   | RHTPA 1.0.0   | yes      | 2025-09-01   |
| 62645   | RHTPA 1.1.0   | no       | 2026-01-15   |

## 4.5.4 -- Match

Comparing extracted version text `0.9.0` against available Jira version names using substring matching:

- `0.9.0` is a substring of `RHTPA 0.9.0` -- **MATCH**
- `0.9.0` is NOT a substring of `RHTPA 1.0.0` -- no match
- `0.9.0` is NOT a substring of `RHTPA 1.1.0` -- no match

Single match found: **RHTPA 0.9.0** (Jira ID: 62643)

## 4.5.5 -- Confirm with User

```
Extracted version info: "0.9.0"
Matched Jira version: RHTPA 0.9.0 (ID: 62643)

Set this as the Affects Version on ACME-510? (yes/no/skip)
```

Upon user confirmation ("yes"), the following Jira update would be executed:

```
jira.edit_issue("ACME-510", fields={
  "versions": [{"id": "62643"}]
})
```

This sets the Affects Version/s field to RHTPA 0.9.0 on the bug issue.
