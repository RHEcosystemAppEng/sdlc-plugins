# Affects Version Resolution – ACME-510 (Step 4.5)

## 4.5.1 – Existing Field Check

The bug issue's `affectsVersions` field is **empty** (no versions currently set).
Skipping the keep/replace/augment prompt and proceeding directly to version extraction.

---

## 4.5.2 – Version Extraction from Description

**Environment / Version section content (from Step 1):**

```
Product version: 0.9.0
OS: RHEL 9.2
Deployment: OpenShift 4.14
```

**Extraction result:**

Scanning the section for version patterns:
- `Product version: 0.9.0` — matches the pattern `version [number]` / explicit version number
- Extracted version identifier: **`0.9.0`**

The section contains a clear, explicit version number. Proceeding to match against available Jira versions.

---

## 4.5.3 – Available Jira Versions

Retrieved from the project's Jira version metadata (equivalent to `jira.getJiraIssueTypeMetaWithFields` or `get_versions ACME`):

| Jira ID | Name         | Released | Release Date |
|---------|--------------|----------|--------------|
| 62643   | RHTPA 0.9.0  | yes      | 2025-06-15   |
| 62644   | RHTPA 1.0.0  | yes      | 2025-09-01   |
| 62645   | RHTPA 1.1.0  | no       | 2026-01-15   |

---

## 4.5.4 – Match

Comparing extracted version `0.9.0` against available Jira version names using substring matching:

| Jira Version Name | Contains `0.9.0`? | Result   |
|-------------------|-------------------|----------|
| RHTPA 0.9.0       | Yes               | **MATCH** |
| RHTPA 1.0.0       | No                | No match  |
| RHTPA 1.1.0       | No                | No match  |

**Single match found:** `RHTPA 0.9.0` (Jira ID: 62643)

---

## 4.5.5 – Confirmation Prompt

The following prompt would be presented to the user before setting the Affects Version field:

```
Extracted version info: "0.9.0"
Matched Jira version: RHTPA 0.9.0 (ID: 62643)

Set this as the Affects Version on ACME-510? (yes/no/skip)
```

**Upon user selecting "yes"**, the following Jira API call would be made:

```
jira.edit_issue("ACME-510", fields={
  "versions": [{"id": "62643"}]
})
```

**Upon user selecting "no"**, the user would be asked to select from the available versions
list above or enter a version manually.

**Upon user selecting "skip"**, Affects Version setting would be skipped and execution
would proceed to Step 5.

---

## Summary

| Sub-step | Action | Outcome |
|----------|--------|---------|
| 4.5.1 | Check existing field | Empty — proceed to extraction |
| 4.5.2 | Extract version from Environment/Version section | `0.9.0` extracted |
| 4.5.3 | Discover available Jira versions | 3 versions found |
| 4.5.4 | Match extracted version to Jira versions | `RHTPA 0.9.0` (ID: 62643) matched |
| 4.5.5 | Confirm with user | Prompt presented (awaiting user response) |
