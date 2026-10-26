# Affects Version Resolution - ACME-510

## Step 4.5: Affects Version/s Resolution

### Sub-step 4.5.1: Existing Field Check

The Affects Version/s field on ACME-510 is currently **(none)** -- the field is empty / not set. Since no version is already assigned, this sub-step is skipped and we proceed to version extraction.

### Sub-step 4.5.2: Version Extraction from Environment / Version Section

The bug description contains an **Environment / Version** section with the following content:

```
Product version: 0.9.0
OS: RHEL 9.2
Deployment: OpenShift 4.14
```

**Extracted version identifier**: `0.9.0`

The version was extracted from the line `Product version: 0.9.0`. The other lines (OS, Deployment) describe the runtime environment, not the product version.

### Sub-step 4.5.3: Available Jira Versions

The following versions are configured in the Jira project:

| Jira ID | Name          | Released | Release Date |
|---------|---------------|----------|--------------|
| 62643   | RHTPA 0.9.0   | yes      | 2025-06-15   |
| 62644   | RHTPA 1.0.0   | yes      | 2025-09-01   |
| 62645   | RHTPA 1.1.0   | no       | 2026-01-15   |

### Sub-step 4.5.4: Substring Matching

Matching extracted version `0.9.0` against available Jira versions using substring matching:

- `RHTPA 0.9.0` -- **MATCH** (contains substring "0.9.0")
- `RHTPA 1.0.0` -- no match
- `RHTPA 1.1.0` -- no match

**Matched version**: RHTPA 0.9.0 (Jira ID: 62643)

A single match was found, so no ambiguity resolution is needed.

### Sub-step 4.5.5: Confirmation Prompt

The following confirmation would be presented to the user before updating the Jira issue:

---

> The Environment / Version section of ACME-510 specifies **Product version: 0.9.0**.
>
> This matches the Jira version **RHTPA 0.9.0** (ID: 62643).
>
> The Affects Version/s field is currently not set on this issue.
>
> **Would you like to set the Affects Version/s field on ACME-510 to "RHTPA 0.9.0"?**

---

Upon user confirmation, the following Jira MCP call would be made:

```
jira_updateIssue(issueKey: "ACME-510", fields: { "versions": [{ "id": "62643" }] })
```
