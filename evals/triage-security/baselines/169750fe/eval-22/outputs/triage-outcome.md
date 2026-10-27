# Triage Outcome for TC-8021 (CVE-2026-31812 / quinn-proto)

## Issue Summary

- **Issue**: TC-8021
- **CVE**: CVE-2026-31812
- **Library**: quinn-proto
- **Fix threshold**: 0.11.14
- **CVSS**: 7.5 (High)
- **Scoped stream**: 2.2.x

## Affects Versions Correction (Step 3)

The PSIRT-assigned Affects Versions field is **incorrect**:

- **Current value**: RHTPA 2.0.0
- **Problem**: No 2.0.x version stream exists in the Security Configuration. There is no matching Jira version for a non-existent stream.

Based on lock file evidence, the correct Affects Versions for the scoped 2.2.x stream are:

- **RHTPA 2.2.0** -- ships quinn-proto 0.11.9 (affected)
- **RHTPA 2.2.1** -- ships quinn-proto 0.11.12 (affected)
- **RHTPA 2.2.2** -- ships quinn-proto 0.11.12 (affected, retag of 2.2.1)

Versions RHTPA 2.2.3 and RHTPA 2.2.4 should NOT be in Affects Versions because they already ship quinn-proto 0.11.14 (the fixed version).

**Action**: Remove RHTPA 2.0.0, add RHTPA 2.2.0, RHTPA 2.2.1, and RHTPA 2.2.2.

## Concurrent Triage (Step 7)

No concurrent triages detected for `quinn-proto` (JQL returned zero results). Proceeding directly to remediation branching.

## Triage Decision: Case A + Case B

### Case A: Cross-Stream Impact (applies because issue is stream-scoped)

The issue is scoped to stream **2.2.x**, but the version impact analysis shows that stream **2.1.x** is also affected:

- 2.1.0 ships quinn-proto 0.11.9 (affected)
- 2.1.1 ships quinn-proto 0.11.9 (affected)

**Action**: Post a cross-stream impact comment on TC-8021:

> Cross-stream impact: quinn-proto < 0.11.14 also affects stream 2.1.x based on lock file analysis. All 2.1.x versions (2.1.0, 2.1.1) ship quinn-proto 0.11.9 which is within the affected range. These streams are tracked by companion issues (see Related links) or may require separate PSIRT triage.

If no existing sibling CVE Vulnerability issue exists for the 2.1.x stream, create **preemptive remediation tasks** for 2.1.x with the `security-preemptive` label and "Related" link type back to TC-8021.

### Case B: Remediation Tasks for Affected Stream (2.2.x)

Supported versions in the scoped stream **are affected** (2.2.0, 2.2.1, 2.2.2), so Case B applies. The upstream fix (quinn-proto 0.11.14) is already available -- confirmed by versions 2.2.3 and 2.2.4 already shipping it. Since Step 2.5 would confirm the upstream branch (`release/0.4.z`) already contains the fix, the **dependency bump variant** applies.

**Ecosystem**: Cargo (source dependency, fix available upstream)
**Task count**: 2 tasks for the 2.2.x stream

#### Task 1: Dependency Bump (upstream source repo)

- **Summary**: `CVE-2026-31812: bump quinn-proto to 0.11.14 in rhtpa-backend (release/0.4.z) [2.2.x]`
- **Type**: Task
- **Labels**: `security`, `CVE-2026-31812`, `cargo-bump`
- **Description**: Run `cargo update -p quinn-proto` on the `release/0.4.z` branch of rhtpa-backend to bump quinn-proto from the affected version to >= 0.11.14. The fix is already available upstream (quinn-rs/quinn#2048).
- **Link**: Depend on TC-8021

#### Task 2: Downstream Propagation (Konflux release repo)

- **Summary**: `CVE-2026-31812: propagate quinn-proto fix to rhtpa-release.0.4.z [2.2.x]`
- **Type**: Task
- **Labels**: `security`, `CVE-2026-31812`, `downstream-propagation`
- **Description**: After the upstream dependency bump lands, update the Konflux release repo `rhtpa-release.0.4.z` to pin the new backend build that includes the quinn-proto fix. Update `artifacts.lock.yaml` to reference the new backend tag.
- **Link**: Depend on TC-8021
- **Blocked by**: Task 1 (dependency bump must land first)

### Case C: Not Applicable

Case C (close as Not a Bug) does not apply because supported versions within the scoped stream are affected.

## Post-Triage Actions

1. **Correct Affects Versions**: Remove RHTPA 2.0.0, add RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2
2. **Add label**: `ai-cve-triaged`
3. **Post cross-stream impact comment** noting 2.1.x is also affected
4. **Create remediation tasks** (2 tasks for 2.2.x stream: dependency bump + downstream propagation)
5. **Create preemptive remediation tasks** for 2.1.x if no sibling CVE Jira exists for that stream
6. **Link remediation tasks** to the release Task from Step 7.5 (if active)
7. **Post summary comment** on TC-8021 with version impact table, Affects Versions correction, and links to all created remediation tasks

## Already-Fixed Note

Versions 2.2.3 and 2.2.4 already ship quinn-proto 0.11.14, meaning the fix was incorporated starting with build v0.4.11 (2026-03-23). Users on 2.2.3 or later are not affected. The remediation tasks target rebuilding or re-releasing the earlier affected versions (2.2.0-2.2.2) with the fix, or ensuring users are advised to upgrade to 2.2.3+.
