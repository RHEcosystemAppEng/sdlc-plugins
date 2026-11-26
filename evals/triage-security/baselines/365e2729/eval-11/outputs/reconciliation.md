# Step 4 – Duplicate, Sibling, Overlap, and Reconciliation Check: TC-8021

## 4.1 / 4.2 – Sibling Vulnerability issues

Query (simulated): `project = TC AND labels = 'CVE-2026-55123' AND issuetype = 10024 AND key != TC-8021`

- **Same-stream (rhtpa-2.1) duplicates**: none were provided, so TC-8021 is not a duplicate.
- **Cross-stream companion**: TC-8020 (stream rhtpa-2.2), known from the issue description and TC-8022's Related link. This is a companion tracker, not a duplicate. TC-8021 has no existing links, so a proposed **Related** link TC-8021 ↔ TC-8020 goes to the engineer for confirmation (idempotency check: no existing Related link found).

## 4.3 – Cross-CVE overlap detection

**Skipped.** The Security Configuration does not declare the Upstream Affected Component, PS Component or Stream custom fields, and the step requires all three.

## 4.4 – Preemptive task reconciliation

### 1. Search

```
jira.search_jql(
  "project = TC AND issuetype = Task AND labels = 'security-preemptive' AND labels = 'CVE-2026-55123' ORDER BY created DESC",
  fields: ["summary", "status", "labels", "issuelinks"]
)
```

Result (as given):

| Key | Summary | Status | Labels | Links |
|---|---|---|---|---|
| TC-8022 | Remediate CVE-2026-55123: bump tokio to 1.42.0 (rhtpa-2.1) | Open | ai-generated-jira, Security, CVE-2026-55123, security-preemptive | Related → TC-8020 (originating CVE Jira, stream rhtpa-2.2) |

### 2. Filter by stream

- Current issue stream suffix: `rhtpa-2.1`.
- TC-8022's summary contains `(rhtpa-2.1)`, so it **matches**.
- Status is Open (not Done/Closed), so the task is still live and usable as this stream's remediation.
- Its bump target (tokio 1.42.0) equals the CVE's fixed version (1.42.0), so it covers the fix threshold.

### 3. Matching preemptive task found: reconciliation actions

Each Jira mutation needs engineer confirmation in interactive mode. They are proposed as follows:

**a. Link TC-8021 → TC-8022 with "Depend"** (standard remediation linkage, replacing the preemptive-only relationship for this stream)

```
jira.create_link(
  inwardIssue: "TC-8021",
  outwardIssue: "TC-8022",
  type: "Depend"
)
```

Idempotency: TC-8021 has no existing links, so the link is created. TC-8022's existing **Related** link to TC-8020 is left alone because it records the originating cross-stream analysis.

**b. Remove the `security-preemptive` label from TC-8022**

```
current_labels = ["ai-generated-jira", "Security", "CVE-2026-55123", "security-preemptive"]
updated_labels = ["ai-generated-jira", "Security", "CVE-2026-55123"]
jira.edit_issue("TC-8022", fields={ "labels": ["ai-generated-jira", "Security", "CVE-2026-55123"] })
```

All other labels stay as they are. Only `security-preemptive` is filtered out.

**c. Inform the engineer**

```
Existing preemptive remediation task TC-8022 found for this CVE and
stream. Created from cross-stream analysis of TC-8020
(linked via "Related").

Actions taken:
- Linked TC-8021 → TC-8022 with "Depend"
- Removed "security-preemptive" label from TC-8022

The preemptive task is now a standard remediation task for this CVE Jira.
Skipping new remediation task creation in Step 8.
```

**d. Record the reconciliation**

`reconciled_streams = { "2.1.x": "TC-8022" }`. Step 8 sees that remediation already exists for stream 2.1.x and **skips task creation** for it.

### Notes

- The input provides only TC-8022 (one task). If a preemptive downstream-propagation subtask for rhtpa-2.1 also existed, it would carry the same labels and get the same reconciliation: a Depend link and label removal. None was returned by the JQL.
- Fullsend equivalent (not used here, since the run is interactive): a `link` action (`link_type: Depend`, TC-8021 → TC-8022, marker `triage-security:tc-8021:link-depend:tc-8022`) and a `field-edit` action on TC-8022 removing `security-preemptive` (marker `triage-security:tc-8021:remove-preemptive-label:tc-8022`).
