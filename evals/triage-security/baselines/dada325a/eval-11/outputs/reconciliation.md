# Step 4 – Duplicate, Sibling, Overlap, and Reconciliation Check: TC-8021

## 4.1 / 4.2 – Siblings

Sibling JQL: `project = TC AND labels = 'CVE-2026-55123' AND issuetype = 10024 AND key != TC-8021`

- **TC-8020**: stream `[rhtpa-2.2]`. It is a different-stream companion, not a duplicate. The issue description references it as the originating CVE Jira of TC-8022.
  - TC-8021 has no existing links, so this is the proposed action: create a **Related** link TC-8021 <-> TC-8020. Engineer confirmation is required.
  - Affects Versions overlap check: TC-8021 carries only 2.1.x versions. No overlap is expected with a 2.2.x issue.
- No same-stream (2.1.x) duplicate exists, so Step 4.1 does not apply.

## 4.3 – Cross-CVE Overlap

The issue carries customfield_10632 (tokio), customfield_10669 and customfield_10832. However, the project's Security Configuration does not declare the Upstream Affected Component, PS Component or Stream fields. Per Step 0, **Step 4.3 is skipped**. No other mock data shows cross-CVE tokio remediation in any case.

## 4.4 – Preemptive Task Reconciliation

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
| TC-8022 | Remediate CVE-2026-55123: bump tokio to 1.42.0 (rhtpa-2.1) | Open | ai-generated-jira, Security, CVE-2026-55123, security-preemptive | Related -> TC-8020 (originating CVE Jira, [rhtpa-2.2]) |

### 2. Filter by stream

- Current issue stream suffix: `rhtpa-2.1`.
- TC-8022's summary contains `(rhtpa-2.1)`, so it **matches**.
- Supporting checks:
  - The task carries the `CVE-2026-55123` label.
  - Its status is Open, so it is still actionable.
  - Its Related link to TC-8020 identifies it as a Case A preemptive task.
  - Its bump target (tokio 1.42.0) equals TC-8021's fixed version (1.42.0), so it fully covers the fix threshold.

### 3. Matching preemptive task found: reconciliation actions

Each action needs engineer confirmation in interactive mode. They are recorded here only, not executed.

**a. Link TC-8021 to TC-8022 with "Depend"** (standard remediation linkage)

```
jira.create_link(
  inwardIssue: "TC-8021",
  outwardIssue: "TC-8022",
  type: "Depend"
)
```

Idempotency: TC-8021 has no existing links, so the link is created.

**b. Remove the `security-preemptive` label from TC-8022**

```
current_labels = ["ai-generated-jira", "Security", "CVE-2026-55123", "security-preemptive"]
updated_labels = ["ai-generated-jira", "Security", "CVE-2026-55123"]
jira.edit_issue("TC-8022", fields={ "labels": updated_labels })
```

All other labels are kept. Only `security-preemptive` is removed.

- The existing **Related** link TC-8022 -> TC-8020 is kept. It preserves traceability to the originating cross-stream analysis.
- The task gets no new labels and no change to its summary or description.

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

| Stream | Remediation state | Step 8 behavior |
|---|---|---|
| 2.1.x | Reconciled. Existing task is TC-8022. | **Skip new task creation** |

### Note on task count

TC-8022 is a single "bump tokio to 1.42.0" task. The ecosystem table calls for 2 tasks per stream for Cargo (bump/backport plus downstream propagation). Step 4.4 says to skip task creation for the reconciled stream, so no new tasks are created automatically.

The engineer should check whether a downstream propagation task, from the Konflux release repo `rhtpa-release.0.3.z`, already accompanies TC-8022. One may exist: the JQL returns only tasks labelled `security-preemptive`, and a Blocks-linked companion task may also carry that label. If none exists, the engineer can request one manually.

### Fullsend equivalent (for reference only)

If this were mutation-authorized Fullsend mode, Step 4.4 would serialize to:

1. `link` with `link_type: "Depend"`, TC-8021 -> TC-8022, marker `triage-security:tc-8021:link-depend:tc-8022`
2. `field-edit` on TC-8022 removing `security-preemptive`, marker `triage-security:tc-8021:remove-preemptive-label:tc-8022`
3. `comment` (ADF, with footnote) on TC-8021 carrying the reconciliation notice
