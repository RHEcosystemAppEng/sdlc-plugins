# Cross-Stream Impact Analysis

## Cross-Stream Impact Comment

**Proposed comment on TC-8020 (not executed — eval mode):**

> Cross-stream impact: tokio < 1.42.0 also affects stream rhtpa-2.1 based on lock file analysis.
>
> | Stream | Versions Affected | tokio Version | Has CVE Jira? |
> |--------|-------------------|---------------|---------------|
> | rhtpa-2.2 | 2.2.0, 2.2.1 | 1.41.1 | **YES** (TC-8020 — this issue) |
> | rhtpa-2.1 | 2.1.0, 2.1.1 | 1.40.0 | **NO** |
>
> Stream rhtpa-2.1 has no companion CVE Jira. Preemptive remediation tasks have been created.

## Preemptive Remediation Tasks Created

**Proposed comment on TC-8020 (not executed — eval mode):**

> Preemptive remediation tasks created for streams without CVE Jiras:
> - rhtpa-2.1: [upstream-task-key] (security-preemptive) — bump tokio to 1.42.0 on release/0.3.z
> - rhtpa-2.1: [downstream-task-key] (security-preemptive) — propagate fix to rhtpa-release.0.3.z
>
> These tasks use the "Related" link type and carry the security-preemptive label.
> When PSIRT creates stream-specific CVE Jiras, Step 4.4 reconciliation will link
> them and remove the label.

## Summary of Actions

### Standard remediation (rhtpa-2.2 — within issue scope):
1. Upstream backport task: bump tokio to 1.42.0 on release/0.4.z
2. Downstream propagation task: update rhtpa-backend ref in rhtpa-release.0.4.z
3. Link type: **Depend** (standard remediation → CVE linkage)
4. Labels: `["ai-generated-jira", "Security", "CVE-2026-55123"]`

### Preemptive remediation (rhtpa-2.1 — no CVE Jira):
1. Preemptive upstream backport task: bump tokio to 1.42.0 on release/0.3.z
2. Preemptive downstream propagation task: update rhtpa-backend ref in rhtpa-release.0.3.z
3. Link type: **Related** (preemptive → originating CVE linkage, not Depend)
4. Labels: `["ai-generated-jira", "Security", "CVE-2026-55123", "security-preemptive"]`
5. Description includes preemptive remediation prefix noting TC-8020 (stream rhtpa-2.2) as the originating CVE

## Reconciliation Note

When PSIRT creates a CVE Jira for stream rhtpa-2.1 (e.g., TC-XXXX with suffix [rhtpa-2.1]), Step 4.4 preemptive task reconciliation will:
1. Search for tasks with labels `security-preemptive` and `CVE-2026-55123`
2. Filter by stream rhtpa-2.1 in the task summary
3. Link the new CVE Jira to the preemptive tasks with `Depend`
4. Remove the `security-preemptive` label
5. Skip new remediation task creation in Step 8 for that stream
