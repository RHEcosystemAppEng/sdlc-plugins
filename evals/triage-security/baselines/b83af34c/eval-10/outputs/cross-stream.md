# Cross-Stream Impact — CVE-2026-55123 (tokio)

## Cross-Stream Impact Comment (posted to TC-8020)

Cross-stream impact: tokio versions before 1.42.0 also affects stream rhtpa-2.1 based on lock file analysis.
These streams are tracked by companion issues (see Related links) or may require separate PSIRT triage.

## Sibling CVE Jira Search Results

JQL: `project = TC AND labels = 'CVE-2026-55123' AND issuetype = 10024 AND key != TC-8020`

| Stream | CVE Jira Found? | Action |
|--------|----------------|--------|
| rhtpa-2.1 | NO | Create preemptive remediation tasks |
| rhtpa-2.2 | TC-8020 (current) | Standard remediation tasks (Case A) |

## Preemptive Task Details (rhtpa-2.1)

Stream rhtpa-2.1 is affected (tokio 1.40.0 in versions RHTPA 2.1.0 and 2.1.1, fix threshold 1.42.0) but no CVE Jira exists for this stream. Per SKILL.md Step 8 Case A (section 3 -- "For each affected stream without its own CVE Jira"), preemptive remediation tasks are created.

### Preemptive Task Variant Properties (per remediation-templates.md)

**Labels**: Standard labels plus `security-preemptive`:
```
["ai-generated-jira", "Security", "CVE-2026-55123", "security-preemptive"]
```

**Link type**: "Related" (not "Depend") to originating CVE Jira TC-8020, because the originating CVE belongs to a different stream (rhtpa-2.2, not rhtpa-2.1).

**Description prefix**: Each preemptive task description is prepended with:
```
> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8020 (stream rhtpa-2.2).
> No stream-specific CVE Jira exists yet for this stream. When PSIRT creates one,
> this task will be linked and the `security-preemptive` label removed.
```

### Tasks Created for rhtpa-2.1

Since tokio is a Cargo ecosystem (source dependency), 2 tasks are created per stream:

1. **Upstream backport (preemptive)**: "Remediate CVE-2026-55123: bump tokio to 1.42.0 (rhtpa-2.1)"
   - Labels: `["ai-generated-jira", "Security", "CVE-2026-55123", "security-preemptive"]`
   - Link: `Related` to TC-8020
   - Repository: backend
   - Target branch: release/0.3.z
   - Description includes preemptive prefix referencing TC-8020 (stream rhtpa-2.2)

2. **Downstream propagation (preemptive)**: "Propagate CVE-2026-55123 fix: update backend ref in rhtpa-release.0.3.z (rhtpa-2.1)"
   - Labels: `["ai-generated-jira", "Security", "CVE-2026-55123", "security-preemptive"]`
   - Link: `Related` to TC-8020
   - Repository: rhtpa-release.0.3.z
   - Target branch: main
   - Description includes preemptive prefix referencing TC-8020 (stream rhtpa-2.2)

### Comment Posted to TC-8020

```
Preemptive remediation tasks created for streams without CVE Jiras:
- rhtpa-2.1: <preemptive-upstream-task-key> (upstream backport, security-preemptive)
- rhtpa-2.1: <preemptive-downstream-task-key> (downstream propagation, security-preemptive)

These tasks use the "Related" link type and carry the security-preemptive
label. When PSIRT creates stream-specific CVE Jiras, Step 4.4
reconciliation will link them and remove the label.
```

### Reconciliation Flow (Step 4.4)

When PSIRT later creates a CVE Jira for rhtpa-2.1 and it is triaged:
1. Step 4.4 searches for preemptive tasks: `labels = 'security-preemptive' AND labels = 'CVE-2026-55123'`
2. Finds the preemptive tasks for rhtpa-2.1
3. Links the new CVE Jira to the preemptive tasks with "Depend" (standard remediation linkage)
4. Removes the `security-preemptive` label
5. Skips new task creation for rhtpa-2.1 (tasks already exist)
