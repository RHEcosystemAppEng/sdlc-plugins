# Triage Outcome

## Summary

**Issue**: TC-8021 -- CVE-2026-31812 quinn-proto - Panic on large stream counts [rhtpa-2.2]
**CVE**: CVE-2026-31812
**Library**: quinn-proto
**Fix threshold**: >= 0.11.14
**CVSS**: 7.5 (High)
**Ecosystem**: Cargo (source dependency)
**Stream scope**: 2.2.x

## Version Impact Table

### Stream 2.2.x (in scope)

| Version | quinn-proto | Affected? |
|---------|-------------|-----------|
| 2.2.0 | 0.11.9 | YES |
| 2.2.1 | 0.11.12 | YES |
| 2.2.2 | 0.11.12 (retag of 2.2.1) | YES |
| 2.2.3 | 0.11.14 | NO |
| 2.2.4 | 0.11.14 | NO |

### Stream 2.1.x (out of scope -- cross-stream)

| Version | quinn-proto | Affected? |
|---------|-------------|-----------|
| 2.1.0 | 0.11.9 | YES |
| 2.1.1 | 0.11.9 | YES |

## Step 7 -- Concurrent Triage Detection

No concurrent triages detected for upstream component `quinn-proto`. JQL search returned zero results. Proceeding silently to Case A/B/C branching.

## Triage Decision

### Case A Applies: Cross-Stream Impact

This is a **stream-scoped** issue (scoped to 2.2.x via the `[rhtpa-2.2]` suffix). The version impact analysis reveals that the **2.1.x stream** (outside this issue's scope) is also affected -- all 2.1.x versions (2.1.0, 2.1.1) ship quinn-proto 0.11.9, which is below the fix threshold of 0.11.14.

Actions for Case A:
1. Post a cross-stream impact comment on TC-8021:
   > Cross-stream impact: quinn-proto versions before 0.11.14 also affects stream 2.1.x based on lock file analysis. This stream is tracked by companion issues (see Related links) or may require separate PSIRT triage.

2. Search for existing CVE Jiras for the 2.1.x stream with label CVE-2026-31812 and suffix `[rhtpa-2.1]`.
   - If a sibling CVE Jira exists for 2.1.x: link as Related, skip preemptive task creation for that stream.
   - If no sibling exists for 2.1.x: create preemptive remediation tasks (with `security-preemptive` label, linked via "Related") for 2.1.x.

### Case B Applies: Affected Versions in Scope -- Create Remediation Tasks

Within the 2.2.x stream, versions 2.2.0, 2.2.1, and 2.2.2 are affected. Versions 2.2.3 and 2.2.4 already ship the fixed version (quinn-proto 0.11.14) and are not affected.

Since quinn-proto is a **Cargo** (source dependency) ecosystem, **two remediation tasks** are created for the 2.2.x stream:

1. **Upstream backport task**: Backport the quinn-proto fix (bump to >= 0.11.14) on the `release/0.4.z` branch of the rhtpa-backend source repository. This task targets the upstream source repository.

2. **Downstream propagation task**: Propagate the upstream fix into the Konflux release repo `rhtpa-release.0.4.z` by updating `artifacts.lock.yaml` to reference a backend build tag that includes the bumped quinn-proto dependency. This task is **blocked by** the upstream backport task (link type: "Blocks").

Both tasks are linked to TC-8021 with link type "Depend".

### Affects Versions Correction

- **Current (PSIRT-assigned)**: RHTPA 2.0.0 (incorrect -- no 2.0.x stream exists)
- **Corrected**: RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2

The correction is scoped to the 2.2.x stream per the issue suffix. Versions 2.2.3 and 2.2.4 are excluded because they already ship the fixed version.

### Why Not Case C

Case C (close as Not a Bug) does not apply because supported versions within the issue's scope are affected. Three versions in the 2.2.x stream (2.2.0, 2.2.1, 2.2.2) ship vulnerable versions of quinn-proto (0.11.9 and 0.11.12, both below the fix threshold of 0.11.14).

## Post-Triage Actions

1. **Affects Versions**: Update from `[RHTPA 2.0.0]` to `[RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]`
2. **Remediation tasks**: Create 2 tasks for stream 2.2.x (upstream backport + downstream propagation)
3. **Cross-stream notice**: Post comment about 2.1.x stream impact; create preemptive tasks if no sibling CVE Jira exists for 2.1.x
4. **Label**: Add `ai-cve-triaged` to TC-8021
5. **Summary comment**: Post triage summary with version impact table, Affects Versions correction, remediation task links, and @mention of the issue reporter
