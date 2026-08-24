# Step 4.5 -- Affects Version Resolution: ACME-510

## 4.5.1 -- Check Existing Field

The bug's `affectsVersions` field is **not populated** (recorded as "(none)" in Step 1 metadata). No existing value to keep, replace, or augment. Proceeding to version extraction.

## 4.5.2 -- Extract Version from Description

Parsing the **Environment / Version** section content:

```
Product version: 0.9.0
OS: RHEL 9.2
Deployment: OpenShift 4.14
```

Extracted version identifiers:
- **`0.9.0`** -- explicit version number following "Product version:" label. This is the primary product version relevant to the Affects Version field.
- `9.2` -- OS version (RHEL); not a product version, excluded.
- `4.14` -- Platform version (OpenShift); not a product version, excluded.

**Extracted product version: `0.9.0`**

## 4.5.3 -- Discover Available Jira Versions

Would call:
```
jira.getJiraIssueTypeMetaWithFields(
  projectIdOrKey: "ACME",
  issueTypeId: "10020"
)
```

Available Jira versions (from fixture data):

| Jira ID | Name          | Released | Release Date |
|---------|---------------|----------|--------------|
| 62643   | RHTPA 0.9.0   | yes      | 2025-06-15   |
| 62644   | RHTPA 1.0.0   | yes      | 2025-09-01   |
| 62645   | RHTPA 1.1.0   | no       | 2026-01-15   |

## 4.5.4 -- Match

Comparing extracted version `0.9.0` against available Jira version names using substring matching:

- `RHTPA 0.9.0` -- **MATCH** (contains substring `0.9.0`)
- `RHTPA 1.0.0` -- no match
- `RHTPA 1.1.0` -- no match

**Single match found: RHTPA 0.9.0 (ID: 62643)**

## 4.5.5 -- Confirmation Prompt

The following prompt would be presented to the user:

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

This sets the Affects Version/s field on ACME-510 to **RHTPA 0.9.0**.

## 4.5.6 -- Gap Flagging

Not applicable -- version was successfully extracted (sub-step 4.5.2) and matched to a Jira version (sub-step 4.5.4). No gap to flag.
