# Cross-Stream Impact -- CVE-2026-55123

## Cross-Stream Impact Comment (posted to TC-8020)

Cross-stream impact: tokio < 1.42.0 also affects stream rhtpa-2.1 based on
lock file analysis.

| Version | Stream | tokio version | Affected? |
|---------|--------|---------------|-----------|
| RHTPA 2.1.0 | rhtpa-2.1 | 1.40.0 | YES |
| RHTPA 2.1.1 | rhtpa-2.1 | 1.40.0 | YES |

Stream rhtpa-2.1 does not have its own CVE Jira for CVE-2026-55123.
Preemptive remediation tasks have been created (see below).

## Sibling CVE Jira Search

JQL used:
```
project = TC AND labels = 'CVE-2026-55123' AND issuetype = 10024 AND key != TC-8020
```

Results filtered by stream suffix `[rhtpa-2.1]`: **No results found.**

No sibling Vulnerability issue exists for CVE-2026-55123 in stream rhtpa-2.1.
This triggers preemptive remediation task creation per Case A of the triage-security
skill (Step 8).

## Preemptive Task Creation Details

Since stream rhtpa-2.1 has no CVE Jira, preemptive remediation tasks are created
using the Preemptive Task Variant from remediation-templates.md:

### Preemptive Task Variant Differences

| Property | Standard Task | Preemptive Task |
|----------|---------------|-----------------|
| Labels | ai-generated-jira, Security, CVE-2026-55123 | ai-generated-jira, Security, CVE-2026-55123, **security-preemptive** |
| Link type to CVE Jira | Depend | **Related** |
| Description prefix | (none) | **Preemptive remediation note** referencing TC-8020 and stream rhtpa-2.2 |

### Tasks Created for Stream rhtpa-2.1

**Upstream Backport (preemptive)**:
- Summary: Remediate CVE-2026-55123: bump tokio to 1.42.0 (rhtpa-2.1)
- Repository: rhtpa-backend
- Target branch: release/0.3.z
- Labels: ai-generated-jira, Security, CVE-2026-55123, security-preemptive
- Link: Related to TC-8020

**Downstream Propagation (preemptive)**:
- Summary: Propagate CVE-2026-55123 fix: update rhtpa-backend ref in rhtpa-release.0.3.z (rhtpa-2.1)
- Repository: rhtpa-release.0.3.z
- Target branch: main
- Labels: ai-generated-jira, Security, CVE-2026-55123, security-preemptive
- Link: Related to TC-8020
- Blocked by: preemptive upstream backport task

### Jira API Calls (pseudocode)

```
# 1. Preemptive upstream backport task
preemptive_upstream = jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Remediate CVE-2026-55123: bump tokio to 1.42.0 (rhtpa-2.1)",
  description: <upstream-task-description-with-preemptive-prefix>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-55123", "security-preemptive"]
)

# 1a. Post description digest comment
jira.add_comment(<preemptive-upstream-key>, "[sdlc-workflow] Description digest: <tagged-digest>")

# 2. Preemptive downstream propagation subtask
preemptive_downstream = jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Propagate CVE-2026-55123 fix: update rhtpa-backend ref in rhtpa-release.0.3.z (rhtpa-2.1)",
  description: <downstream-task-description-with-preemptive-prefix>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-55123", "security-preemptive"]
)

# 2a. Post description digest comment
jira.add_comment(<preemptive-downstream-key>, "[sdlc-workflow] Description digest: <tagged-digest>")

# 3. Link preemptive tasks to originating CVE with "Related"
jira.create_link(
  inwardIssue: "TC-8020",
  outwardIssue: <preemptive-upstream-key>,
  type: "Related"
)

jira.create_link(
  inwardIssue: "TC-8020",
  outwardIssue: <preemptive-downstream-key>,
  type: "Related"
)

# 4. Link downstream blocked by upstream
jira.create_link(
  inwardIssue: <preemptive-upstream-key>,
  outwardIssue: <preemptive-downstream-key>,
  type: "Blocks"
)
```

## Comment Posted to TC-8020 (Preemptive Task Summary)

```
Preemptive remediation tasks created for streams without CVE Jiras:
- rhtpa-2.1: <preemptive-upstream-key> (upstream backport, security-preemptive),
  <preemptive-downstream-key> (downstream propagation, security-preemptive)

These tasks use the "Related" link type and carry the security-preemptive
label. When PSIRT creates stream-specific CVE Jiras, Step 4.4
reconciliation will link them and remove the label.
```

## Reconciliation (Step 4.4)

When PSIRT later creates a CVE Jira for CVE-2026-55123 scoped to stream rhtpa-2.1,
the triage-security skill's Step 4.4 (Preemptive Task Reconciliation) will:

1. Search for tasks with labels `security-preemptive` and `CVE-2026-55123`
2. Filter to tasks whose summary contains `(rhtpa-2.1)`
3. Link the new CVE Jira to the preemptive tasks with "Depend"
4. Remove the `security-preemptive` label from the preemptive tasks
5. Skip new remediation task creation since tasks already exist
