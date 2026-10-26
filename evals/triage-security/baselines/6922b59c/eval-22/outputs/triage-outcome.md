# Triage Outcome -- TC-8021 (CVE-2026-31812 / quinn-proto)

## Summary

CVE-2026-31812 affects quinn-proto versions before 0.11.14. The issue TC-8021 is
scoped to stream **2.2.x** (per the `[rhtpa-2.2]` suffix in the summary). The
Upstream Affected Component (`customfield_10632`) is `quinn-proto`.

## Version Impact Summary

### In-scope stream (2.2.x)

| Version | quinn-proto | Affected? |
|---------|-------------|-----------|
| 2.2.0 | 0.11.9 | YES |
| 2.2.1 | 0.11.12 | YES |
| 2.2.2 | (retag of 2.2.1) | YES |
| 2.2.3 | 0.11.14 | NO |
| 2.2.4 | 0.11.14 | NO |

Three out of five versions in the 2.2.x stream are affected. The fix was
introduced in version 2.2.3 (build 0.4.11), which ships quinn-proto 0.11.14.

### Cross-stream impact (2.1.x -- outside issue scope)

| Version | quinn-proto | Affected? |
|---------|-------------|-----------|
| 2.1.0 | 0.11.9 | YES |
| 2.1.1 | 0.11.9 | YES |

All versions in the 2.1.x stream are also affected, but that stream is outside
this issue's scope.

## Triage Decision: Case A + Case B

Since the issue is **stream-scoped** to 2.2.x and supported versions within that
stream are affected, this is **Case B** (affected -- create remediation tasks).

Additionally, since the 2.1.x stream is also affected but outside this issue's
scope, **Case A** (cross-stream impact) applies. A cross-stream impact comment
would be posted to TC-8021 identifying that 2.1.x is also affected.

### Case A: Cross-stream Impact

The version impact analysis reveals that stream 2.1.x (versions 2.1.0, 2.1.1)
is also affected by this vulnerability. Both 2.1.x versions ship quinn-proto
0.11.9, which is below the 0.11.14 fix threshold.

Action: Post a cross-stream impact comment on TC-8021:

> Cross-stream impact: quinn-proto < 0.11.14 also affects stream 2.1.x based
> on lock file analysis. Stream 2.1.x is tracked by companion issues (see
> Related links) or may require separate PSIRT triage.

If no sibling CVE Jira exists for 2.1.x, preemptive remediation tasks would
be created with the `security-preemptive` label and `Related` link type.

### Case B: Remediation for 2.2.x stream

**Ecosystem:** Cargo (source dependency)
**Upstream fix status:** The upstream branch `release/0.4.z` already ships
quinn-proto 0.11.14 at its latest tag (v0.4.12). This means the remediation
uses the **dependency bump** variant rather than an upstream backport.

**Remediation tasks for 2.2.x (2 tasks):**

1. **Dependency bump task:**
   - Summary: "Remediate CVE-2026-31812: update quinn-proto to 0.11.14 (rhtpa-2.2)"
   - Repository: backend (source repo from Ecosystem Mappings)
   - Target branch: release/0.4.z
   - Action: `cargo update -p quinn-proto` to pull in quinn-proto >= 0.11.14
   - Labels: ai-generated-jira, Security, CVE-2026-31812
   - Link: Depend to TC-8021

2. **Downstream propagation task:**
   - Summary: "Propagate CVE-2026-31812 fix: update backend ref in rhtpa-release.0.4.z (rhtpa-2.2)"
   - Repository: rhtpa-release.0.4.z (Konflux release repo)
   - Target branch: main
   - Action: Update the backend source reference in artifacts.lock.yaml to
     the merged commit containing the quinn-proto bump
   - Labels: ai-generated-jira, Security, CVE-2026-31812
   - Link: Depend to TC-8021; Blocks from dependency bump task
   - Blocked by: the dependency bump task (upstream must merge first)

### Affects Versions Correction

- **Current (PSIRT-assigned):** RHTPA 2.0.0 (incorrect -- no 2.0 stream exists)
- **Corrected (scoped to 2.2.x):** RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2

### Concurrent Triage (Step 7)

No concurrent triages detected for quinn-proto. Zero results returned from the
JQL search for in-progress Vulnerability issues with the same Upstream Affected
Component. Safe to proceed with remediation task creation.

## Post-Triage Actions

1. Correct Affects Versions: RHTPA 2.0.0 -> RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2
2. Create 2 remediation tasks for the 2.2.x stream (dependency bump + downstream propagation)
3. Post cross-stream impact comment for 2.1.x
4. Create preemptive remediation tasks for 2.1.x (if no sibling CVE Jira exists)
5. Link remediation tasks to release Task (if release Jira orchestration is active)
6. Add `ai-cve-triaged` label to TC-8021
7. Post triage summary comment with version impact table and task links
8. Transition TC-8021 to In Progress
