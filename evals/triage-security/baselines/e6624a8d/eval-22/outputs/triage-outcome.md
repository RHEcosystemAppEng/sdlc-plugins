# Triage Outcome: TC-8021

## Summary

**Decision: Case A (Cross-stream impact) + Case B (Affected -- create remediation tasks)**

CVE-2026-31812 affects quinn-proto (versions before 0.11.14) in the 2.2.x stream. The version impact analysis shows that versions 2.2.0, 2.2.1, and 2.2.2 ship vulnerable versions of quinn-proto (0.11.9 and 0.11.12), while versions 2.2.3 and 2.2.4 already ship the fixed version (0.11.14). Additionally, the 2.1.x stream (outside this issue's scope) is also affected -- both 2.1.0 and 2.1.1 ship quinn-proto 0.11.9.

## Step-by-Step Reasoning

### Step 1 -- Data Extraction
- CVE-2026-31812 affects quinn-proto before version 0.11.14
- Fix threshold: **0.11.14**
- Stream scope: **2.2.x** (from summary suffix `[rhtpa-2.2]`)
- Upstream Affected Component (`customfield_10632`): **quinn-proto**
- Ecosystem: **Cargo** (source dependency)
- PSIRT-assigned Affects Versions: RHTPA 2.0.0 (incorrect)

### Step 2 -- Version Impact Analysis
Version impact table built from security-matrix.md pinned commits:

| Stream | Version | Build Tag | quinn-proto | Affected? |
|--------|---------|-----------|-------------|-----------|
| 2.1.x | 2.1.0 | v0.3.8 | 0.11.9 | YES |
| 2.1.x | 2.1.1 | v0.3.12 | 0.11.9 | YES |
| 2.2.x | 2.2.0 | v0.4.5 | 0.11.9 | YES |
| 2.2.x | 2.2.1 | v0.4.8 | 0.11.12 | YES |
| 2.2.x | 2.2.2 | v0.4.9 | (retag of v0.4.8) | YES (same as 2.2.1) |
| 2.2.x | 2.2.3 | v0.4.11 | 0.11.14 | NO |
| 2.2.x | 2.2.4 | v0.4.12 | 0.11.14 | NO |

### Step 3 -- Affects Versions Correction
- Current (PSIRT-assigned): `[RHTPA 2.0.0]`
- Proposed (lock-file-verified, scoped to 2.2.x stream): `[RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]`
- PSIRT assigned "RHTPA 2.0.0" which does not match any configured stream. The correct Affects Versions based on lock file evidence for the 2.2.x stream are versions 2.2.0, 2.2.1, and 2.2.2.
- Proposed action: Update Affects Versions from `[RHTPA 2.0.0]` to `[RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]` (requires engineer confirmation).

### Step 7 -- Concurrent Triage Detection
- Upstream Affected Component: **quinn-proto** (from `customfield_10632`)
- JQL search for in-progress triages with `cf[10632] ~ 'quinn-proto' AND status IN ('In Progress', 'Code Review') AND key != TC-8021` returned **zero results**
- No concurrent triages detected -- proceeding silently to Case A/B/C branching
- No wait/skip/proceed options presented because no conflict exists

### Case A -- Cross-Stream Impact
This issue is scoped to the 2.2.x stream, but the version impact analysis reveals that the 2.1.x stream is also affected (both 2.1.0 and 2.1.1 ship quinn-proto 0.11.9). Cross-stream impact notice would be posted:

> Cross-stream impact: quinn-proto < 0.11.14 also affects stream 2.1.x based on lock file analysis. This stream is tracked by companion issues (see Related links) or may require separate PSIRT triage.

For the 2.1.x stream, the skill would check whether a sibling CVE Jira exists with the same CVE label and a matching stream suffix (`[rhtpa-2.1]`). If no sibling exists, preemptive remediation tasks would be created with the `security-preemptive` label and "Related" link type to TC-8021.

### Case B -- Remediation Tasks (2.2.x stream)
Since versions 2.2.0, 2.2.1, and 2.2.2 in the 2.2.x stream are affected, remediation tasks are proposed. For the Cargo ecosystem (source dependency), two tasks per stream are created:

**Task 1: Upstream Backport**
- Summary: Bump quinn-proto to >= 0.11.14 in rhtpa-backend (rhtpa-2.2)
- Repository: rhtpa-backend
- Target Branch: release/0.4.z
- Labels: CVE-2026-31812, ai-cve-remediation, security
- Link: Depend -> TC-8021
- Description: Bump quinn-proto from current version to >= 0.11.14 to resolve CVE-2026-31812 (denial of service via excessive stream count in QUIC transport frames). The upstream fix is available in quinn-proto 0.11.14 (see quinn-rs/quinn#2048).
- Acceptance Criteria:
  - quinn-proto version in Cargo.lock is >= 0.11.14
  - All existing tests pass
  - No regressions in QUIC transport functionality

**Task 2: Downstream Propagation**
- Summary: Propagate quinn-proto fix to rhtpa-release.0.4.z (rhtpa-2.2)
- Repository: rhtpa-release.0.4.z (Konflux release repo)
- Target Branch: main
- Labels: CVE-2026-31812, ai-cve-remediation, security
- Link: Depend -> TC-8021, Blocks <- Task 1 (blocked by upstream backport)
- Description: Update the backend source reference in artifacts.lock.yaml to pick up the upstream quinn-proto fix from Task 1. The downstream propagation ensures the fix is included in the next product build.
- Acceptance Criteria:
  - artifacts.lock.yaml references a backend tag that includes quinn-proto >= 0.11.14
  - Build pipeline succeeds with the updated reference

## Proposed Jira Actions (Require Engineer Confirmation)

All of the following are proposals, not executed mutations:

1. **Affects Versions correction**: Update from `[RHTPA 2.0.0]` to `[RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]`
2. **Cross-stream impact comment**: Post notice about 2.1.x stream impact
3. **Remediation task creation**: Create 2 tasks for the 2.2.x stream (upstream backport + downstream propagation)
4. **Preemptive task creation** (if no 2.1.x sibling CVE Jira exists): Create 2 preemptive tasks for the 2.1.x stream with `security-preemptive` label
5. **Add `ai-cve-triaged` label** to TC-8021
6. **Post triage summary comment** documenting the version impact table, Affects Versions correction, and remediation task links
