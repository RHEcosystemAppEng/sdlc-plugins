# Step 8 -- Remediation

## Triage Outcome

### Stream 2.2.x (issue-scoped)

**Case C: No supported versions affected.**

The version impact analysis using the enriched fix threshold (0.4.8 from Step 1.5) shows that ALL versions in the 2.2.x stream ship h2 >= 0.4.8. No supported versions within this issue's scope are affected.

**Recommendation**: Close TC-8030 as "Not a Bug" (not affected).

- Resolution: Not a Bug
- VEX Justification: Component not Present (the vulnerable version of h2, < 0.4.8, is not shipped in any 2.2.x release)

**Proposed close comment**:

> No supported versions in stream 2.2.x ship a vulnerable version of h2. Version impact analysis (using enriched fix threshold 0.4.8 from MITRE CVE API and OSV.dev cross-validation):
>
> | Version | h2 version | Affected? |
> |---------|------------|-----------|
> | 2.2.0 | 0.4.8 | NO |
> | 2.2.1 | 0.4.8 | NO |
> | 2.2.2 | -- (retag) | NO |
> | 2.2.3 | 0.4.9 | NO |
> | 2.2.4 | 0.4.9 | NO |
>
> All 2.2.x versions ship h2 0.4.8 or later, which is at or above the fix threshold (< 0.4.8).

### Stream 2.1.x (cross-stream impact -- Case A)

The version impact analysis reveals that stream 2.1.x (outside this issue's scope) IS affected:
- 2.1.0 ships h2 0.4.5 (affected, < 0.4.8)
- 2.1.1 ships h2 0.4.5 (affected, < 0.4.8)

**Cross-stream impact comment** (to be posted on TC-8030):

> Cross-stream impact: h2 < 0.4.8 also affects stream 2.1.x based on lock file analysis. Versions 2.1.0 and 2.1.1 ship h2 0.4.5, which is below the fix threshold. These versions are tracked by companion issues (see Related links) or may require separate PSIRT triage.

**Remediation tasks for stream 2.1.x** (preemptive, if no sibling CVE Jira exists for 2.1.x):

Since the ecosystem is Cargo (source dependency), two tasks would be created per stream:

#### Task 1: Upstream backport (2.1.x)

**Summary**: Remediate CVE-2026-48901: bump h2 to 0.4.8 (rhtpa-2.1)

**Description**:

> **Preemptive remediation**: This task was created proactively from cross-stream impact analysis of TC-8030 (stream 2.2.x). No stream-specific CVE Jira exists yet for stream 2.1.x. When PSIRT creates one, this task will be linked and the `security-preemptive` label removed.

Remediate CVE-2026-48901: h2 HTTP/2 CONTINUATION flood vulnerability. The vulnerable dependency (h2 < 0.4.8) must be updated to the fixed version (0.4.8+).

- Repository: backend
- Target branch: release/0.3.z
- Affected versions: 2.1.0, 2.1.1
- Source commits: v0.3.8, v0.3.12
- Upstream fix: https://github.com/hyperium/h2/pull/800
- Advisory: https://github.com/advisories/GHSA-2026-r7f2-kk9p
- Labels: ai-generated-jira, Security, CVE-2026-48901, security-preemptive
- Link type: Related (to TC-8030)

#### Task 2: Downstream propagation (2.1.x)

**Summary**: Propagate CVE-2026-48901 fix: update backend ref in rhtpa-release.0.3.z (rhtpa-2.1)

**Description**:

> **Preemptive remediation**: This task was created proactively from cross-stream impact analysis of TC-8030 (stream 2.2.x). No stream-specific CVE Jira exists yet for stream 2.1.x. When PSIRT creates one, this task will be linked and the `security-preemptive` label removed.

Update backend reference in rhtpa-release.0.3.z to pick up the CVE-2026-48901 fix from the upstream backport task.

- Repository: rhtpa-release.0.3.z
- Target branch: main
- Source pinning method: artifacts.lock.yaml
- Labels: ai-generated-jira, Security, CVE-2026-48901, security-preemptive
- Link type: Related (to TC-8030), Blocks (blocked by upstream task)
