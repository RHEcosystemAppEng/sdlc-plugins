# Triage Outcome: TC-8021 (CVE-2026-31812 / quinn-proto)

## Version Impact Summary

| Stream | Product Version | quinn-proto | Affected? |
|--------|-----------------|-------------|-----------|
| 2.1.x | 2.1.0 | 0.11.9 | YES |
| 2.1.x | 2.1.1 | 0.11.9 | YES |
| 2.2.x | 2.2.0 | 0.11.9 | YES |
| 2.2.x | 2.2.1 | 0.11.12 | YES |
| 2.2.x | 2.2.2 | 0.11.12 | YES (retag of 2.2.1) |
| 2.2.x | 2.2.3 | 0.11.14 | NO (fixed) |
| 2.2.x | 2.2.4 | 0.11.14 | NO (fixed) |

## Triage Decision Path

### Step 7 -- Concurrent Triage Detection

No concurrent triages detected for `quinn-proto`. Proceeding to Case A/B/C branching.

### Case A: Cross-Stream Impact (Applies)

This issue is **scoped** to stream 2.2.x (summary suffix `[rhtpa-2.2]`). The version impact analysis reveals that stream **2.1.x** (outside this issue's scope) is also affected -- all 2.1.x versions ship quinn-proto 0.11.9, which is below the fix threshold of 0.11.14.

**Cross-stream impact action:**

1. Post a cross-stream impact comment on TC-8021:
   > Cross-stream impact: quinn-proto versions before 0.11.14 also affects stream 2.1.x based on lock file analysis. Stream 2.1.x versions (2.1.0, 2.1.1) ship quinn-proto 0.11.9. These streams are tracked by companion issues (see Related links) or may require separate PSIRT triage.

2. Search for existing CVE Jiras for stream 2.1.x with label CVE-2026-31812. If no companion issue exists for 2.1.x, create **preemptive remediation tasks** for that stream with the `security-preemptive` label and "Related" link type back to TC-8021.

### Case B: Affected -- Create Remediation Tasks (Applies)

Supported versions within the issue's scope (stream 2.2.x) are affected: **RHTPA 2.2.0, 2.2.1, 2.2.2**. The fix is already present in versions 2.2.3 and 2.2.4 (quinn-proto 0.11.14).

Since quinn-proto is a **Cargo** (source dependency) ecosystem library, the ecosystem classification table specifies **2 tasks per affected stream**:

#### Task 1: Upstream Backport (stream 2.2.x)

- **Type**: Task
- **Summary**: Backport quinn-proto fix for CVE-2026-31812 to release/0.4.z (rhtpa-2.2)
- **Description**: Bump quinn-proto to >= 0.11.14 in the rhtpa-backend repository on the `release/0.4.z` branch. The upstream fix is available in [quinn-rs/quinn#2048](https://github.com/quinn-rs/quinn/pull/2048). quinn-proto 0.11.14 resolves a denial-of-service vulnerability (CVSS 7.5) where a remote attacker could cause a panic by sending a QUIC transport frame that creates an excessive number of streams.
- **Labels**: CVE-2026-31812, security, upstream-backport
- **Link to TC-8021**: Depend
- **Affects Versions**: RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2

#### Task 2: Downstream Propagation (stream 2.2.x)

- **Type**: Task
- **Summary**: Propagate quinn-proto fix for CVE-2026-31812 to rhtpa-release.0.4.z (rhtpa-2.2)
- **Description**: After the upstream backport lands, update the Konflux release repo `rhtpa-release.0.4.z` to reference the new backend build that includes quinn-proto >= 0.11.14. Update the `artifacts.lock.yaml` to point to the new backend tag.
- **Labels**: CVE-2026-31812, security, downstream-propagation
- **Link to TC-8021**: Depend
- **Blocked by**: Task 1 (upstream backport) -- link type "Blocks"
- **Affects Versions**: RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2

### Case C: Not Applicable

Case C (no supported versions affected) does not apply. Versions 2.2.0, 2.2.1, and 2.2.2 are affected within the issue's scoped stream.

## Affects Versions Correction

- **Current (PSIRT-assigned)**: RHTPA 2.0.0
- **Corrected**: RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2

The PSIRT-assigned value `RHTPA 2.0.0` is incorrect -- there is no 2.0.x version stream in the project configuration. The corrected values reflect the actual affected versions in the 2.2.x stream, verified via lock file analysis at pinned commits from the security matrix.

## Post-Triage Actions

1. **Assign** TC-8021 to the current user and transition to Assigned status.
2. **Correct Affects Versions** from `[RHTPA 2.0.0]` to `[RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]`.
3. **Create 2 remediation tasks** for stream 2.2.x (upstream backport + downstream propagation), linked to TC-8021 with "Depend" link type.
4. **Post cross-stream impact comment** noting that stream 2.1.x is also affected.
5. **Create preemptive remediation tasks** for stream 2.1.x if no companion CVE Jira exists (with `security-preemptive` label and "Related" link).
6. **Add `ai-cve-triaged` label** to TC-8021.
7. **Post summary comment** to TC-8021 with the version impact table, Affects Versions correction, triage outcome, and links to all created remediation tasks.

## Key Observations

- The vulnerability was already fixed in the 2.2.x stream starting from version 2.2.3 (build v0.4.11), which introduced quinn-proto 0.11.14. Versions 2.2.0 through 2.2.2 remain vulnerable.
- The PSIRT-assigned Affects Versions (`RHTPA 2.0.0`) is incorrect and requires correction. There is no 2.0.x stream in the configuration.
- The 2.1.x stream is entirely affected (both versions ship quinn-proto 0.11.9), requiring cross-stream impact notification (Case A).
- No concurrent triages were detected for the quinn-proto component (Step 7), so remediation task creation can proceed without risk of duplication.
