# Step 4.5 -- Affects Version Resolution: ACME-510

## 4.5.1 -- Check Existing Field

The bug's `affectsVersions` field is **not populated** (value: `(none)`). No existing versions to keep, replace, or augment. Proceeding to version extraction.

## 4.5.2 -- Extract Version from Description

Parsed the **Environment / Version** section content:

```
Product version: 0.9.0
OS: RHEL 9.2
Deployment: OpenShift 4.14
```

Extracted version identifier: **0.9.0**

Pattern matched: explicit version number `0.9.0` following the keyword "Product version:".

## 4.5.3 -- Discover Available Jira Versions

Available Jira versions for project ACME (retrieved via `jira.getJiraIssueTypeMetaWithFields` or `get_versions`):

| Jira ID | Name          | Released | Release Date |
|---------|---------------|----------|--------------|
| 62643   | RHTPA 0.9.0   | yes      | 2025-06-15   |
| 62644   | RHTPA 1.0.0   | yes      | 2025-09-01   |
| 62645   | RHTPA 1.1.0   | no       | 2026-01-15   |

## 4.5.4 -- Match

Comparing extracted version `0.9.0` against available Jira version names using substring matching:

- `0.9.0` matches **RHTPA 0.9.0** (Jira ID: 62643) -- substring match confirmed

Single match found. No ambiguity.

## 4.5.5 -- Confirmation Prompt

The following confirmation prompt would be presented to the user:

```
Extracted version info: "0.9.0"
Matched Jira version: RHTPA 0.9.0 (ID: 62643)

Set this as the Affects Version on ACME-510? (yes/no/skip)
```

Upon user confirmation ("yes"), the following Jira operation would be executed:

```
jira.edit_issue("ACME-510", fields={
  "versions": [{"id": "62643"}]
})
```

REST API fallback equivalent:
```
python3 scripts/jira-client.py update_issue ACME-510 --fields-json '{"versions": [{"name": "RHTPA 0.9.0"}]}'
```
