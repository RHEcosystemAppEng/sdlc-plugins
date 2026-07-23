# Step 4.5 -- Affects Version Resolution: ACME-510

## 4.5.1 -- Check Existing Field

The bug's `affectsVersions` field is **not populated** (recorded as "(none)" in Step 1).
No keep/replace/augment prompt is needed. Proceeding to version extraction.

## 4.5.2 -- Extract Version from Description

Parsing the **Environment / Version** section content from Step 1:

```
Product version: 0.9.0
OS: RHEL 9.2
Deployment: OpenShift 4.14
```

**Extracted version identifier**: `0.9.0`

Source: the "Product version:" line contains an explicit version number pattern matching `X.Y.Z`.

Other values in this section (RHEL 9.2, OpenShift 4.14) are infrastructure/platform
versions, not the product version, and are not relevant for the Affects Version field.

## 4.5.3 -- Discover Available Jira Versions

Available Jira versions for project ACME (retrieved via `getJiraIssueTypeMetaWithFields`
or `get_versions`):

| Jira ID | Name          | Released | Release Date |
|---------|---------------|----------|--------------|
| 62643   | RHTPA 0.9.0   | yes      | 2025-06-15   |
| 62644   | RHTPA 1.0.0   | yes      | 2025-09-01   |
| 62645   | RHTPA 1.1.0   | no       | 2026-01-15   |

## 4.5.4 -- Match

Comparing extracted version `0.9.0` against available Jira version names using
substring matching:

- `RHTPA 0.9.0` -- **MATCH** (contains substring `0.9.0`)
- `RHTPA 1.0.0` -- no match
- `RHTPA 1.1.0` -- no match

**Result**: Single match found -- `RHTPA 0.9.0` (ID: 62643).

## 4.5.5 -- Confirmation Prompt

The following confirmation prompt would be presented to the user:

```
Extracted version info: "0.9.0"
Matched Jira version: RHTPA 0.9.0 (ID: 62643)

Set this as the Affects Version on ACME-510? (yes/no/skip)
```

- **yes**: Update the field via `jira.edit_issue(ACME-510, fields={"versions": [{"id": "62643"}]})`
- **no**: Ask the user to select from the available versions list, or enter a version manually.
- **skip**: Skip Affects Version setting entirely and proceed to Step 5.

## Proposed Jira Update (on user confirmation "yes")

```
jira.edit_issue("ACME-510", fields={
  "versions": [{"id": "62643"}]
})
```

REST API fallback equivalent:
```
python3 scripts/jira-client.py update_issue ACME-510 --fields-json '{"versions": [{"name": "RHTPA 0.9.0"}]}'
```
