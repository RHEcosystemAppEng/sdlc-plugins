# Step 4.5 -- Affects Version Resolution

## 4.5.1 -- Check Existing Field

The bug's `affectsVersions` field is **not populated** (recorded as "(none)" in Step 1).
No existing versions to keep, replace, or augment. Proceeding to version extraction.

## 4.5.2 -- Extract Version from Description

Parsing the **Environment / Version** section content extracted in Step 1:

```
Product version: 0.9.0
OS: RHEL 9.2
Deployment: OpenShift 4.14
```

Extracted version identifier: **0.9.0**

Source: the line "Product version: 0.9.0" contains an explicit version number pattern
(`version` keyword followed by a semantic version number).

## 4.5.3 -- Discover Available Jira Versions

Called `jira.getJiraIssueTypeMetaWithFields(projectIdOrKey: "ACME", issueTypeId: "10020")`
to retrieve the `versions` field's `allowedValues`.

Available Jira versions:

| Jira ID | Name          | Released | Release Date |
|---------|---------------|----------|--------------|
| 62643   | RHTPA 0.9.0   | yes      | 2025-06-15   |
| 62644   | RHTPA 1.0.0   | yes      | 2025-09-01   |
| 62645   | RHTPA 1.1.0   | no       | 2026-01-15   |

## 4.5.4 -- Match

Comparing extracted version text **"0.9.0"** against available Jira version names
using substring matching:

- "0.9.0" matches **RHTPA 0.9.0** (ID: 62643) -- substring match confirmed
- "0.9.0" does not match "RHTPA 1.0.0" -- no substring overlap
- "0.9.0" does not match "RHTPA 1.1.0" -- no substring overlap

Single match found: **RHTPA 0.9.0** (ID: 62643)

## 4.5.5 -- Confirmation Prompt

The following prompt would be presented to the user:

```
Extracted version info: "0.9.0"
Matched Jira version: RHTPA 0.9.0 (ID: 62643)

Set this as the Affects Version on ACME-510? (yes/no/skip)
```

Upon user confirming **"yes"**, the following Jira API call would be made:

```
jira.edit_issue("ACME-510", fields={
  "versions": [{"id": "62643"}]
})
```

This sets the Affects Version/s field on ACME-510 to **RHTPA 0.9.0**.
