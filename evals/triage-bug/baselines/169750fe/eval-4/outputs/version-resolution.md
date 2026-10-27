# Step 4.5 -- Affects Version Resolution: ACME-510

## Sub-step 4.5.1 -- Check Existing Field

The bug's `affectsVersions` field is **not populated** (recorded as "(none)" in Step 1).
There is no existing value to keep, replace, or augment. Proceeding to extract version
from the description.

## Sub-step 4.5.2 -- Extract Version from Description

Parsing the **Environment / Version** section content:

```
Product version: 0.9.0
OS: RHEL 9.2
Deployment: OpenShift 4.14
```

Extracted version identifier: **`0.9.0`**

Source: "Product version: 0.9.0" -- the "Product version:" prefix followed by a
semantic version number `0.9.0`.

## Sub-step 4.5.3 -- Discover Available Jira Versions

Would call:

```
jira.getJiraIssueTypeMetaWithFields(
  projectIdOrKey: "ACME",
  issueTypeId: "10020"
)
```

Available Jira versions (from `versions` field `allowedValues`):

| Jira ID | Name          | Released | Release Date |
|---------|---------------|----------|--------------|
| 62643   | RHTPA 0.9.0   | yes      | 2025-06-15   |
| 62644   | RHTPA 1.0.0   | yes      | 2025-09-01   |
| 62645   | RHTPA 1.1.0   | no       | 2026-01-15   |

## Sub-step 4.5.4 -- Match

Comparing extracted version text `0.9.0` against available Jira version names using
substring matching:

- `RHTPA 0.9.0` -- contains substring `0.9.0` -- **MATCH**
- `RHTPA 1.0.0` -- does not contain `0.9.0` -- no match
- `RHTPA 1.1.0` -- does not contain `0.9.0` -- no match

**Single match found**: RHTPA 0.9.0 (ID: 62643)

## Sub-step 4.5.5 -- Confirm with User

```
Extracted version info: "0.9.0"
Matched Jira version: RHTPA 0.9.0 (ID: 62643)

Set this as the Affects Version on ACME-510? (yes/no/skip)
```

Upon user confirmation ("yes"), would execute:

```
jira.edit_issue("ACME-510", fields={
  "versions": [{"id": "62643"}]
})
```

This sets the Affects Version/s field on ACME-510 to "RHTPA 0.9.0".
