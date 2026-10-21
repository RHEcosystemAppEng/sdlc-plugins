# Step 4.5 -- Affects Version Resolution: ACME-510

## 4.5.1 -- Check Existing Field

The bug's `affectsVersions` field is NOT populated (recorded as "(none)" in Step 1).
Since no versions are currently set, sub-step 4.5.1 is skipped -- there is nothing
to keep, replace, or augment.

## 4.5.2 -- Extract Version from Description

Parsing the **Environment / Version** section content:

```
Product version: 0.9.0
OS: RHEL 9.2
Deployment: OpenShift 4.14
```

Extracted version identifier: **0.9.0**

Source: "Product version: 0.9.0" -- explicit version number pattern matched.

## 4.5.3 -- Discover Available Jira Versions

Available Jira versions for project ACME:

| Jira ID | Name          | Released | Release Date |
|---------|---------------|----------|--------------|
| 62643   | RHTPA 0.9.0   | yes      | 2025-06-15   |
| 62644   | RHTPA 1.0.0   | yes      | 2025-09-01   |
| 62645   | RHTPA 1.1.0   | no       | 2026-01-15   |

## 4.5.4 -- Match

Comparing extracted version text "0.9.0" against available Jira version names using
substring matching:

- "0.9.0" is a substring of "RHTPA 0.9.0" -- **MATCH** (ID: 62643)
- "0.9.0" is NOT a substring of "RHTPA 1.0.0" -- no match
- "0.9.0" is NOT a substring of "RHTPA 1.1.0" -- no match

Single match found: **RHTPA 0.9.0** (ID: 62643)

## 4.5.5 -- Confirm with User

Confirmation prompt to present to the user:

```
Extracted version info: "0.9.0"
Matched Jira version: RHTPA 0.9.0 (ID: 62643)

Set this as the Affects Version on ACME-510? (yes/no/skip)
```

- **yes**: Set Affects Version to RHTPA 0.9.0 via:
  ```
  jira.edit_issue("ACME-510", fields={
    "versions": [{"id": "62643"}]
  })
  ```
- **no**: Ask the user to select from the available versions list or enter a version manually.
- **skip**: Skip Affects Version setting and proceed to Step 5.
