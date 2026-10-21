# Triage Outcome for TC-8020

## Issue Summary

- **Issue**: TC-8020
- **CVE**: CVE-2026-31812
- **Library**: quinn-proto
- **Fix threshold**: 0.11.14
- **Stream scope**: 2.2.x (from summary suffix `[rhtpa-2.2]`)
- **Ecosystem**: Cargo (source dependency)
- **CVSS**: 7.5 (High)

## Version Impact Summary

### 2.2.x Stream (in scope)

| Version | quinn-proto | Affected? |
|---------|-------------|-----------|
| RHTPA 2.2.0 | 0.11.9 | YES |
| RHTPA 2.2.1 | 0.11.12 | YES |
| RHTPA 2.2.2 | 0.11.12 (retag) | YES |
| RHTPA 2.2.3 | 0.11.14 | NO (fixed) |
| RHTPA 2.2.4 | 0.11.14 | NO (fixed) |

### 2.1.x Stream (cross-stream, out of scope)

| Version | quinn-proto | Affected? |
|---------|-------------|-----------|
| RHTPA 2.1.0 | 0.11.9 | YES |
| RHTPA 2.1.1 | 0.11.9 | YES |

## Step 3 -- Affects Versions Correction

- **Current (PSIRT-assigned)**: `[RHTPA 2.0.0]`
- **Proposed (corrected)**: `[RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]`
- **Rationale**: RHTPA 2.0.0 does not correspond to any configured version stream. Lock file analysis at pinned commits confirms that versions 2.2.0, 2.2.1, and 2.2.2 ship quinn-proto < 0.11.14. Versions 2.2.3 and 2.2.4 are excluded because they ship the fixed version (0.11.14). The correction is scoped to the 2.2.x stream per the issue's `[rhtpa-2.2]` suffix.

## Step 4 -- Duplicate/Sibling/Overlap Check

- **Sibling issues**: Would search for issues with label `CVE-2026-31812` in project TC. No sibling information provided in mock data, so assumed none found.
- **Cross-CVE overlap (Step 4.3)**: Upstream Affected Component (`quinn-proto`) is configured via `customfield_10632`. Would search for other Vulnerability issues with the same component value to check if existing remediation already covers this CVE's fix threshold. No overlap data provided in mock; assumed no covering remediation found.
- **Preemptive task reconciliation (Step 4.4)**: Would search for tasks with `security-preemptive` and `CVE-2026-31812` labels. No preemptive tasks provided in mock; assumed none found.

## Step 5 -- Version Lifecycle Check

Would verify affected versions (2.2.0, 2.2.1, 2.2.2) against the product lifecycle page at `https://access.example.com/product-life-cycle/rhtpa`. Not queried in this eval; assuming all versions are within support lifecycle.

## Step 6 -- Already Fixed Check

The fix is already present in versions 2.2.3 and 2.2.4 within the 2.2.x stream (they ship quinn-proto 0.11.14). However, the "already fixed" check in Step 6 looks specifically for resolved sibling Vulnerability issues, not for fixed versions within the current stream. Since no resolved sibling issues were identified in Step 4, the already-fixed scenario from Step 6 does not apply.

The fact that 2.2.3+ ships the fix is captured by the version impact table and reflected in the corrected Affects Versions (which exclude 2.2.3 and 2.2.4).

## Step 7 -- Concurrent Triage Detection

**Concurrent triage detected.** TC-8019 is In Progress, assigned to `engineer-b@example.com`, and affects the same upstream component (`quinn-proto`). See `concurrent-triage.md` for the full analysis.

The engineer must choose one of three options before proceeding:
1. **Wait** -- pause until TC-8019 completes
2. **Skip** -- skip remediation task creation
3. **Proceed** -- create tasks with `concurrent-triage-overlap` label

**This is a blocking gate.** The triage cannot proceed to Step 7.5 or Step 8 until the engineer makes a choice.

## Triage Decision (contingent on Step 7 resolution)

### If the engineer chooses to Proceed (Option 3):

**Case A applies** (cross-stream impact on a scoped issue):

The issue is scoped to 2.2.x, but the 2.1.x stream is also affected (both 2.1.0 and 2.1.1 ship quinn-proto 0.11.9). A cross-stream impact comment would be posted:

> Cross-stream impact: quinn-proto < 0.11.14 also affects stream 2.1.x based on lock file analysis. This stream is tracked by companion issues (see Related links) or may require separate PSIRT triage.

For the 2.1.x stream, if no sibling CVE Jira exists, proactive (preemptive) remediation tasks would be created with the `security-preemptive` label and linked to TC-8020 via "Related" link type.

**Case B applies** for the 2.2.x stream:

Affected versions exist (2.2.0, 2.2.1, 2.2.2), so remediation is needed. Since this is a Cargo (source dependency) ecosystem and the fix is already available upstream (Step 2.5 would confirm that 2.2.3+ already ships 0.11.14, meaning the upstream source repo's `release/0.4.z` branch already has the fix), the remediation would follow the **"fix available"** variant:

- **Task 1**: Dependency bump -- `cargo update -p quinn-proto` to bump quinn-proto to >= 0.11.14 on the upstream `release/0.4.z` branch (for the 2.2.x stream)
- **Task 2**: Downstream propagation -- update the Konflux release repo `rhtpa-release.0.4.z` to pick up the upstream fix

Each task would be linked to TC-8020 with "Depend" link type. The `concurrent-triage-overlap` label would be added to TC-8020.

### If the engineer chooses to Wait (Option 1):

Triage pauses. When TC-8019's triage completes, re-running triage on TC-8020 would allow Step 4.3 to detect any remediation tasks already created by TC-8019 that cover quinn-proto. If TC-8019's remediation already bumps quinn-proto to >= 0.11.14, no new tasks would be needed for TC-8020 (cross-CVE overlap detection would identify the covering remediation).

### If the engineer chooses to Skip (Option 2):

No remediation tasks are created. A Jira comment would be posted on TC-8020 explaining that task creation was skipped due to concurrent triage on quinn-proto (TC-8019 In Progress). The Affects Versions correction and `ai-cve-triaged` label would still be applied.

## Post-Triage Actions (after Step 7 resolution)

Regardless of the engineer's Step 7 choice, the following actions apply:

1. **Affects Versions correction**: `RHTPA 2.0.0` -> `RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2`
2. **Add label**: `ai-cve-triaged` to TC-8020
3. **Post summary comment**: Documenting version impact table, Affects Versions correction, triage outcome, and links to any remediation tasks created
4. **Release Jira orchestration** (Step 7.5, if proceeding): Find or create release Epic/Task for the 2.2.x stream before remediation task creation

## Key Findings

1. **PSIRT Affects Versions is wrong**: RHTPA 2.0.0 does not correspond to any configured stream. Must be corrected to RHTPA 2.2.0, 2.2.1, 2.2.2.
2. **Partial fix in-stream**: The 2.2.x stream already has the fix in versions 2.2.3 and 2.2.4 (quinn-proto 0.11.14). Older versions 2.2.0-2.2.2 remain affected.
3. **Cross-stream impact**: The 2.1.x stream is also affected (both versions ship quinn-proto 0.11.9), requiring Case A cross-stream notification and potential preemptive remediation.
4. **Concurrent triage blocks Step 8**: TC-8019 is actively being triaged on the same component (quinn-proto). The engineer must decide whether to wait, skip, or proceed before remediation tasks can be created.
5. **Ecosystem**: Cargo source dependency with fix available upstream, leading to 2 remediation tasks per affected stream (dependency bump + downstream propagation).
