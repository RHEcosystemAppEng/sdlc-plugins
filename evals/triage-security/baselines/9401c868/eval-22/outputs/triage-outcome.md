# Triage Outcome for TC-8021 (CVE-2026-31812 / quinn-proto)

## Summary

CVE-2026-31812 affects the `quinn-proto` crate (versions before 0.11.14). The vulnerability allows a remote attacker to cause a denial of service (panic) by sending a QUIC transport frame that creates an excessive number of streams. CVSS score is 7.5 (High).

## Triage Decision: Case A + Case B (Affected, with cross-stream impact)

### Stream Scope

The issue TC-8021 is **scoped to stream 2.2.x** (from summary suffix `[rhtpa-2.2]`).

### Affected Versions Within Scope (2.2.x)

| Version | quinn-proto | Affected? |
|---------|-------------|-----------|
| 2.2.0 | 0.11.9 | YES |
| 2.2.1 | 0.11.12 | YES |
| 2.2.2 | (retag of 2.2.1) | YES |
| 2.2.3 | 0.11.14 | NO |
| 2.2.4 | 0.11.14 | NO |

Three versions in the 2.2.x stream are affected. Since at least one supported version is affected, this is **not** Case C (close as Not a Bug). Remediation is required.

### Cross-Stream Impact (Case A)

The version impact analysis reveals that **stream 2.1.x** (outside this issue's scope) is also affected:

| Version | quinn-proto | Affected? |
|---------|-------------|-----------|
| 2.1.0 | 0.11.9 | YES |
| 2.1.1 | 0.11.9 | YES |

**Case A applies.** The skill would:

1. Post a cross-stream impact comment on TC-8021:
   > Cross-stream impact: quinn-proto versions before 0.11.14 also affects stream 2.1.x based on lock file analysis. This stream is tracked by companion issues (see Related links) or may require separate PSIRT triage.

2. Search for existing CVE Jiras for CVE-2026-31812 in the 2.1.x stream (sibling issues with suffix `[rhtpa-2.1]`).

3. If no sibling CVE Jira exists for 2.1.x, create **preemptive remediation tasks** for 2.1.x with the `security-preemptive` label and "Related" link type to TC-8021.

### Remediation Tasks (Case B) -- Stream 2.2.x

**Ecosystem**: Cargo (source dependency)
**Upstream fix status for 2.2.x**: Fix IS available on release/0.4.z (v0.4.11+ ships quinn-proto 0.11.14)

Since the upstream branch for 2.2.x already ships the fixed version, the remediation uses the **dependency bump** variant (not upstream backport):

#### Task 1: Dependency Bump (2.2.x)

- **Summary**: Remediate CVE-2026-31812: update quinn-proto to 0.11.14 (rhtpa-2.2)
- **Repository**: backend (rhtpa-backend)
- **Target Branch**: release/0.4.z
- **Labels**: ai-generated-jira, Security, CVE-2026-31812
- **Description**: Bump quinn-proto to >= 0.11.14 via `cargo update -p quinn-proto`. The fix is already available on the upstream branch. Verify the lock file reflects >= 0.11.14 after the update.
- **Acceptance Criteria**: quinn-proto >= 0.11.14, no dependency conflicts, existing tests pass

#### Task 2: Downstream Propagation (2.2.x)

- **Summary**: Propagate CVE-2026-31812 fix: update backend ref in rhtpa-release.0.4.z (rhtpa-2.2)
- **Repository**: rhtpa-release.0.4.z
- **Target Branch**: main
- **Labels**: ai-generated-jira, Security, CVE-2026-31812
- **Blocked by**: Task 1 (dependency bump must merge first)
- **Description**: Update the backend source reference in rhtpa-release.0.4.z to pick up the quinn-proto 0.11.14 fix. Source pinning method: artifacts.lock.yaml (download URL contains tag).
- **Acceptance Criteria**: backend reference updated, Konflux rebuild triggers new container image

### Preemptive Remediation Tasks (Case A) -- Stream 2.1.x (if no sibling CVE exists)

If no existing CVE Jira for CVE-2026-31812 exists for the 2.1.x stream:

**Upstream fix status for 2.1.x**: Fix is NOT available on release/0.3.z (v0.3.12 still ships quinn-proto 0.11.9). This means the **upstream backport** variant is used (not dependency bump).

#### Preemptive Task 1: Upstream Backport (2.1.x)

- **Summary**: Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (rhtpa-2.1)
- **Repository**: backend (rhtpa-backend)
- **Target Branch**: release/0.3.z
- **Labels**: ai-generated-jira, Security, CVE-2026-31812, security-preemptive
- **Link Type**: Related (to TC-8021, not Depend)
- **Description**: Backport the quinn-proto fix to the release/0.3.z branch. Upstream fix PR: quinn-rs/quinn#2048.

#### Preemptive Task 2: Downstream Propagation (2.1.x)

- **Summary**: Propagate CVE-2026-31812 fix: update backend ref in rhtpa-release.0.3.z (rhtpa-2.1)
- **Repository**: rhtpa-release.0.3.z
- **Target Branch**: main
- **Labels**: ai-generated-jira, Security, CVE-2026-31812, security-preemptive
- **Blocked by**: Preemptive Task 1
- **Link Type**: Related (to TC-8021)

### Affects Versions Correction

- **Current (PSIRT-assigned)**: RHTPA 2.0.0
- **Proposed (corrected)**: RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2
- **Rationale**: RHTPA 2.0.0 does not correspond to any configured version stream. The issue is scoped to 2.2.x per the summary suffix. Lock file analysis confirms versions 2.2.0, 2.2.1, and 2.2.2 ship vulnerable quinn-proto (< 0.11.14). Versions 2.2.3 and 2.2.4 ship the fixed version (0.11.14) and are excluded.

### Concurrent Triage Detection (Step 7)

No concurrent triages detected. JQL search for Vulnerability issues with Upstream Affected Component `quinn-proto` in status "In Progress" or "Code Review" returned zero results. Proceeding without warnings.

### Post-Triage Actions

1. Add `ai-cve-triaged` label to TC-8021
2. Correct Affects Versions from [RHTPA 2.0.0] to [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]
3. Create remediation tasks (2 for 2.2.x scope, 2 preemptive for 2.1.x if no sibling CVE exists)
4. Link remediation tasks to release Tasks (from Step 7.5)
5. Post summary comment on TC-8021 with version impact table, Affects Versions correction, and links to all created tasks
6. Transition TC-8021 to In Progress
