# Step 4 – Duplicate, Sibling, Overlap, and Reconciliation Check: TC-8021

## Step 4.1 / 4.2 – Siblings

JQL (would run): `project = TC AND labels = 'CVE-2026-55123' AND issuetype = 10024 AND key != TC-8021`

- Known sibling: **TC-8020**, the same CVE for stream **[rhtpa-2.2]**. Its stream differs from this issue's, so it is a **cross-stream companion tracker** and not a duplicate. Step 4.1 does not apply because there is no same-stream sibling.
- Step 4.2: TC-8021 has no existing issue links, so a `Related` link TC-8021 <-> TC-8020 is proposed. It needs confirmation and was not executed.

| Issue | Stream | Status | Affects Versions |
|---|---|---|---|
| TC-8020 | 2.2.x | (per Jira) | 2.2.x versions |
| TC-8021 <- | 2.1.x | New | RHTPA 2.1.0, RHTPA 2.1.1 |

## Step 4.3 – Cross-CVE Overlap Detection

- **Skipped.** The Security Configuration in the project CLAUDE.md does not configure the Upstream Affected Component, PS Component or Stream custom field IDs, and this step needs all three. The issue does carry values in customfield_10632/10669/10832, but configuration controls whether the step runs.

## Step 4.4 – Preemptive Task Reconciliation

### 1. Search

```
jira.search_jql(
  "project = TC AND issuetype = Task AND labels = 'security-preemptive' AND labels = 'CVE-2026-55123' ORDER BY created DESC",
  fields: ["summary", "status", "labels", "issuelinks"]
)
```

Result (provided by the eval):

| Key | Summary | Status | Labels | Links |
|---|---|---|---|---|
| TC-8022 | Remediate CVE-2026-55123: bump tokio to 1.42.0 (rhtpa-2.1) | Open | ai-generated-jira, Security, CVE-2026-55123, security-preemptive | Related -> TC-8020 (originating CVE Jira, [rhtpa-2.2]) |

### 2. Filter by stream

- Current issue stream suffix: `rhtpa-2.1`.
- The TC-8022 summary contains `(rhtpa-2.1)`, so it **matches**.
- TC-8022 also carries the `CVE-2026-55123` label and is Open, so it is a valid reconciliation target. It was created by an earlier Case A cross-stream run on TC-8020 for a stream that had no CVE Jira at the time.

### 3. Matching preemptive task found: reconciliation actions

Interactive mode, so each mutation is presented for engineer confirmation. Nothing was executed here because Jira calls are forbidden in this eval.

**a. Link TC-8021 -> TC-8022 with "Depend"** (standard remediation linkage, replacing the preemptive-only relationship for this stream)

Idempotency check: TC-8021 `issuelinks` is empty, so there is no existing Depend link to TC-8022 and the link should be created.

```
jira.create_link(
  inwardIssue: "TC-8021",
  outwardIssue: "TC-8022",
  type: "Depend"
)
```

**b. Remove the `security-preemptive` label from TC-8022**

```
current_labels = ["ai-generated-jira", "Security", "CVE-2026-55123", "security-preemptive"]
updated_labels = ["ai-generated-jira", "Security", "CVE-2026-55123"]
jira.edit_issue("TC-8022", fields={ "labels": ["ai-generated-jira", "Security", "CVE-2026-55123"] })
```

All other labels are kept. Only `security-preemptive` is removed. The existing `Related` link from TC-8022 to TC-8020 stays as cross-stream traceability.

**c. Inform the engineer**

```
Existing preemptive remediation task TC-8022 found for this CVE and
stream. Created from cross-stream analysis of TC-8020
(linked via "Related").

Actions taken:
- Linked TC-8021 -> TC-8022 with "Depend"
- Removed "security-preemptive" label from TC-8022

The preemptive task is now a standard remediation task for this CVE Jira.
Skipping new remediation task creation in Step 8.
```

**d. Record the reconciliation**

- `reconciled_streams = { "2.1.x": "TC-8022" }`. Step 8 must **not** create new remediation tasks for stream 2.1.x.

### Proposed Jira mutations (all require confirmation, none executed)

| # | Target | Operation | Detail |
|---|---|---|---|
| 1 | TC-8021 <-> TC-8020 | create_link | Related (Step 4.2 cross-stream companion) |
| 2 | TC-8021 -> TC-8022 | create_link | Depend (Step 4.4a) |
| 3 | TC-8022 | edit_issue labels | Remove `security-preemptive` (Step 4.4b) |

### Not done (and why)

- No new remediation tasks for 2.1.x, because TC-8022 already covers this stream.
- TC-8022 is not re-created or duplicated, and its description is not modified.
- The Related link TC-8022 -> TC-8020 is not removed.
- TC-8021 is not closed as Duplicate. TC-8022 is a remediation Task, not a sibling Vulnerability, so TC-8021 stays open as the CVE tracker for 2.1.x.
