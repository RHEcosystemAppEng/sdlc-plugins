# Step 4 – Duplicate, Sibling, Overlap, and Reconciliation Check: TC-8021

## Step 4 (sibling search) / 4.1 / 4.2

Sibling JQL (would be run live):
```
project = TC AND labels = 'CVE-2026-55123' AND issuetype = 10024 AND key != TC-8021
```
- Known sibling: **TC-8020**, CVE-2026-55123, stream **[rhtpa-2.2]**. This is a different-stream companion tracker, **not a duplicate**.
- 4.1 Same-stream duplicates: none. TC-8021 is the only known [rhtpa-2.1] issue, so it is not closed as Duplicate.
- 4.2 Cross-stream coordination: TC-8021 has no existing issue links, so the proposal is to create a **Related** link TC-8021 to TC-8020, after confirmation. Affects Versions overlap check: TC-8021 claims only 2.1.x versions, which belong to its own stream.

| Issue | Stream | Status | Affects Versions |
|---|---|---|---|
| TC-8020 | 2.2.x | (per Jira) | (2.2.x versions) |
| TC-8021 ← | 2.1.x | New | RHTPA 2.1.0, RHTPA 2.1.1 |

## Step 4.3 – Cross-CVE Overlap Detection

**Skipped.** The Upstream Affected Component, PS Component, and Stream custom fields are not configured in Security Configuration. The issue does carry customfield_10632/10669/10832, but the skill keys this step on configuration, not on which fields are present.

## Step 4.4 – Preemptive Task Reconciliation

### 1. Search

```
jira.search_jql(
  "project = TC AND issuetype = Task AND labels = 'security-preemptive' AND labels = 'CVE-2026-55123' ORDER BY created DESC",
  fields: ["summary", "status", "labels", "issuelinks"]
)
```

Result (provided):

| Key | Summary | Status | Labels | Links |
|---|---|---|---|---|
| TC-8022 | Remediate CVE-2026-55123: bump tokio to 1.42.0 (rhtpa-2.1) | Open | ai-generated-jira, Security, CVE-2026-55123, security-preemptive | Related → TC-8020 (originating CVE Jira, [rhtpa-2.2]) |

### 2. Filter by stream

The current issue's stream suffix is `rhtpa-2.1`. The TC-8022 summary contains `(rhtpa-2.1)`, so it is a **match**. The task targets the same CVE, the same stream, and the same library (tokio), with fix target 1.42.0, which equals the fixed version.

### 3. Matching preemptive task found: reconciliation actions

Each action below is presented to the engineer and runs only after explicit confirmation (interactive mode).

**a. Link with "Depend"** (standard remediation linkage):
```
jira.create_link(
  inwardIssue: "TC-8021",
  outwardIssue: "TC-8022",
  type: "Depend"
)
```
The existing **Related** link TC-8022 to TC-8020 is kept. It records where the task came from and is not removed or replaced.

**b. Remove the `security-preemptive` label** (filter the current labels, keep all others):
```
current_labels = ["ai-generated-jira", "Security", "CVE-2026-55123", "security-preemptive"]
updated_labels = ["ai-generated-jira", "Security", "CVE-2026-55123"]
jira.edit_issue("TC-8022", fields={ "labels": ["ai-generated-jira", "Security", "CVE-2026-55123"] })
```

**c. Inform the engineer:**
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

**d. Record the reconciliation:** `reconciled_streams = { "2.1.x": "TC-8022" }`. Step 8 skips remediation task creation for stream 2.1.x.

### What is NOT done

- No new remediation Task is created for rhtpa-2.1. That would duplicate TC-8022.
- TC-8022 is not closed, recreated, or re-described. Its summary, description, and status (Open) stay unchanged.
- No new Vulnerability issue is created.
- The TC-8022 → TC-8020 Related link is not removed.
