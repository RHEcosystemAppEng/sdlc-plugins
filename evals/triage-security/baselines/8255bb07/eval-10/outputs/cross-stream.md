# Cross-Stream Impact: TC-8020

## Cross-Stream Impact Comment

The following comment would be posted to TC-8020:

```
Cross-stream impact: tokio < 1.42.0 also affects stream rhtpa-2.1 based on lock file analysis.

Version impact across streams:

| Version | Stream | tokio version | Affected? |
|---------|--------|---------------|-----------|
| RHTPA 2.1.0 | rhtpa-2.1 | 1.40.0 | YES |
| RHTPA 2.1.1 | rhtpa-2.1 | 1.40.0 | YES |
| RHTPA 2.2.0 | rhtpa-2.2 | 1.41.1 | YES |
| RHTPA 2.2.1 | rhtpa-2.2 | 1.41.1 | YES |

Stream rhtpa-2.1 has no companion CVE Jira for CVE-2026-55123.
Preemptive remediation tasks have been created (see below).
```

## Sibling CVE Jira Search Results

JQL: `project = TC AND issuetype = 10024 AND labels = "CVE-2026-55123" AND summary ~ "[rhtpa-2.1]"`

**Result**: No issues found.

Stream rhtpa-2.1 has no CVE Jira for CVE-2026-55123, triggering preemptive task creation.

## Preemptive Task Details

### Stream rhtpa-2.1 -- No CVE Jira exists

Since no sibling CVE Jira exists for stream rhtpa-2.1, preemptive remediation tasks
are created per Case B of Step 8.

**Key differences from standard (Case A) remediation:**

| Attribute | Case A (standard) | Case B (preemptive) |
|-----------|-------------------|---------------------|
| Labels | `ai-generated-jira`, `Security`, `CVE-2026-55123` | `ai-generated-jira`, `Security`, `CVE-2026-55123`, **`security-preemptive`** |
| Link type to CVE Jira | **Depend** | **Related** |
| Description prefix | (none) | Preemptive remediation note referencing TC-8020 and stream rhtpa-2.2 |
| Target branch | release/0.4.z (2.2.x stream) | release/0.3.z (2.1.x stream) |
| Konflux repo | rhtpa-release.0.4.z | rhtpa-release.0.3.z |

### Preemptive tasks to create

1. **Upstream backport (rhtpa-2.1)**
   - Summary: `Remediate CVE-2026-55123: bump tokio to 1.42.0 (rhtpa-2.1)`
   - Repository: backend
   - Target branch: `release/0.3.z`
   - Labels: `["ai-generated-jira", "Security", "CVE-2026-55123", "security-preemptive"]`
   - Link to TC-8020: **Related** (not Depend)
   - Description includes preemptive prefix:
     > **Preemptive remediation**: This task was created proactively from cross-stream
     > impact analysis of TC-8020 (stream rhtpa-2.2).
     > No stream-specific CVE Jira exists yet for this stream. When PSIRT creates one,
     > this task will be linked and the `security-preemptive` label removed.

2. **Downstream propagation (rhtpa-2.1)**
   - Summary: `Propagate CVE-2026-55123 fix: update backend ref in rhtpa-release.0.3.z (rhtpa-2.1)`
   - Repository: rhtpa-release.0.3.z
   - Target branch: main
   - Labels: `["ai-generated-jira", "Security", "CVE-2026-55123", "security-preemptive"]`
   - Link to TC-8020: **Related** (not Depend)
   - Blocked by: preemptive upstream task (Blocks link)
   - Description includes preemptive prefix (same as above)

### Comment to post on TC-8020

```
Preemptive remediation tasks created for streams without CVE Jiras:
- rhtpa-2.1: <preemptive-upstream-task-key> (upstream backport, security-preemptive),
  <preemptive-downstream-task-key> (downstream propagation, security-preemptive)

These tasks use the "Related" link type and carry the security-preemptive
label. When PSIRT creates stream-specific CVE Jiras, Step 4.4
reconciliation will link them and remove the label.
```

## Reconciliation Note

When PSIRT eventually creates a CVE Jira for CVE-2026-55123 scoped to stream
rhtpa-2.1, the triage-security skill's Step 4.4 (Preemptive Task Reconciliation)
will:

1. Search for existing tasks with labels `CVE-2026-55123` and `security-preemptive`
2. Find the preemptive tasks created here
3. Link them to the new stream-specific CVE Jira with "Depend" type
4. Remove the `security-preemptive` label
5. Add a "Related" link between the new CVE Jira and TC-8020
