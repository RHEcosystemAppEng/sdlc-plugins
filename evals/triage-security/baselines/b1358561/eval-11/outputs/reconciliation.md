# TC-8021 — Step 4 / Step 4.4 Preemptive Task Reconciliation

## Steps 4.1 / 4.2 – Sibling check (context)

- Sibling JQL: `project = TC AND labels = 'CVE-2026-55123' AND issuetype = 10024 AND key != TC-8021`
- Known sibling: **TC-8020**, stream `[rhtpa-2.2]` (2.2.x). This is a **different-stream companion**, not a duplicate. No same-stream duplicate exists, so Step 4.1 does not apply.
- Step 4.2: TC-8021 has no issue links, so there is no existing Related link to TC-8020. Planned: `create_link(inward: TC-8021, outward: TC-8020, type: "Related")`.

| Issue | Stream | Status | Affects Versions |
|---|---|---|---|
| TC-8020 | 2.2.x | (not provided) | (2.2.x versions) |
| TC-8021 (current) | 2.1.x | New | RHTPA 2.1.0, RHTPA 2.1.1 |

## Step 4.3 – Cross-CVE overlap

**Skipped.** The Upstream Affected Component, PS Component, and Stream custom fields are not configured in Security Configuration. Step 4.3 requires all three.

## Step 4.4 – Preemptive task reconciliation

### 1. Search

```
jira.search_jql(
  "project = TC AND issuetype = Task AND labels = 'security-preemptive' AND labels = 'CVE-2026-55123' ORDER BY created DESC",
  fields: ["summary", "status", "labels", "issuelinks"]
)
```

Result (provided, simulated):

| Key | Summary | Status | Labels | Links |
|---|---|---|---|---|
| TC-8022 | Remediate CVE-2026-55123: bump tokio to 1.42.0 (rhtpa-2.1) | Open | ai-generated-jira, Security, CVE-2026-55123, security-preemptive | Related → TC-8020 (originating CVE, [rhtpa-2.2]) |

### 2. Filter by stream

- Current issue stream suffix: `rhtpa-2.1`.
- TC-8022's summary contains `(rhtpa-2.1)`, so it **matches**.
- Further checks: the CVE label matches (CVE-2026-55123). The status is Open, so the task is still actionable. It targets tokio 1.42.0, which equals the fix threshold (1.42.0) and so covers this CVE. The Related link to TC-8020 confirms it came from Case A cross-stream analysis of the 2.2.x CVE.

### 3. Matching task found, reconciliation actions

**a. Depend link** (standard remediation linkage). TC-8021 has no links, so no existing Depend link is present.

```
jira.create_link(
  inwardIssue: TC-8021,
  outwardIssue: TC-8022,
  type: "Depend"
)
```

**b. Remove the `security-preemptive` label from TC-8022**

```
current_labels = ["ai-generated-jira", "Security", "CVE-2026-55123", "security-preemptive"]
updated_labels = ["ai-generated-jira", "Security", "CVE-2026-55123"]
jira.edit_issue(TC-8022, fields={"labels": ["ai-generated-jira", "Security", "CVE-2026-55123"]})
```

Only `security-preemptive` is removed. All other labels stay. The existing **Related** link TC-8022 to TC-8020 also stays, as provenance and traceability.

**c. Engineer notification**

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

**d. Record reconciliation.** Stream `2.1.x` is marked "remediation exists (TC-8022)". Step 8 will **not** create new remediation tasks for 2.1.x.

### Confirmation

Interactive mode requires engineer confirmation before each Jira mutation. Proposed mutations for approval:

1. `create_link` TC-8021 → TC-8022 (Depend)
2. `edit_issue` TC-8022 labels: drop `security-preemptive`

Per the eval instructions, neither mutation was executed.

### Observations for the engineer

- The search returned only one task, TC-8022. Under the source-dependency rule (2 tasks per stream), a Case A preemptive run may also have created a downstream propagation task. If that companion task exists but is missing the `security-preemptive` or `CVE-2026-55123` label, this search will not find it. The engineer should check TC-8022's links (for example a Blocks link) to see whether a downstream propagation task exists for 2.1.x. If one does, it should be reconciled the same way (Depend link plus label removal).
- TC-8022 is now a standard (non-preemptive) remediation task. Once Step 7.5 finds or creates the 2.1.x release Task, TC-8022 should be linked to it (Blocks) and TC-8021 should be linked to it (Related).
