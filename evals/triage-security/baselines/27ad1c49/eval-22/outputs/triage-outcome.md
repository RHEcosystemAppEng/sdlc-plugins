# Triage Outcome (Step 8 Decision) -- TC-8021

## Summary

**Issue**: TC-8021 -- CVE-2026-31812 quinn-proto - Panic on large stream counts [rhtpa-2.2]
**CVE**: CVE-2026-31812
**Library**: quinn-proto
**Fix threshold**: >= 0.11.14
**Ecosystem**: Cargo (source dependency)
**Issue stream scope**: 2.2.x (from summary suffix `[rhtpa-2.2]`)

## Triage Decision: Case B (Affected) + Case A (Cross-Stream Impact)

### Case B -- Affected versions within scope (2.2.x stream)

Supported versions within the issue's scoped stream (2.2.x) are affected:

| Version | quinn-proto | Affected? |
|---------|-------------|-----------|
| 2.2.0 | 0.11.9 | YES |
| 2.2.1 | 0.11.12 | YES |
| 2.2.2 | (retag of 2.2.1) | YES |
| 2.2.3 | 0.11.14 | NO |
| 2.2.4 | 0.11.14 | NO |

Since versions 2.2.0, 2.2.1, and 2.2.2 are affected, remediation is required.

**Remediation tasks for 2.2.x stream** (Cargo = source dependency, 2 tasks):

1. **Upstream backport/dependency bump task**: Bump quinn-proto to >= 0.11.14 in the backend source repository on branch `release/0.4.z`. If the upstream branch already ships the fix (Step 2.5 would confirm), this becomes a dependency bump task (`cargo update -p quinn-proto`). Otherwise, an upstream backport task is created.
   - Summary: `Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (rhtpa-2.2)`
   - Labels: `ai-generated-jira`, `Security`, `CVE-2026-31812`
   - Link: Depend from TC-8021 to this task

2. **Downstream propagation task**: Update the backend source reference in the Konflux release repo (`rhtpa-release.0.4.z`) to pick up the upstream fix once merged.
   - Summary: `Propagate CVE-2026-31812 fix: update backend ref in rhtpa-release.0.4.z (rhtpa-2.2)`
   - Labels: `ai-generated-jira`, `Security`, `CVE-2026-31812`
   - Link: Blocked by the upstream task (Blocks link)
   - Link: Depend from TC-8021 to this task

### Case A -- Cross-Stream Impact (scoped issue)

Because TC-8021 is scoped to the 2.2.x stream and the version impact analysis reveals that the 2.1.x stream is also affected (both 2.1.0 and 2.1.1 ship quinn-proto 0.11.9), Case A applies.

**Cross-stream impact comment** would be posted on TC-8021:

> Cross-stream impact: quinn-proto < 0.11.14 also affects stream 2.1.x based on lock file analysis. This stream is tracked by companion issues (see Related links) or may require separate PSIRT triage.

**For stream 2.1.x:**
- Check for existing sibling CVE Jiras with label CVE-2026-31812 and summary suffix `[rhtpa-2.1]` (Step 4 sibling search).
- If a sibling CVE Jira exists for 2.1.x: skip preemptive task creation for that stream (it will be triaged through its own issue).
- If no sibling CVE Jira exists for 2.1.x: create **preemptive** remediation tasks with the `security-preemptive` label and "Related" link type (not "Depend") to TC-8021:
  1. Upstream backport/bump task for 2.1.x on branch `release/0.3.z`
  2. Downstream propagation task for `rhtpa-release.0.3.z`

### Affects Versions Correction (Step 3)

The PSIRT-assigned Affects Versions (`RHTPA 2.0.0`) is incorrect. Proposed correction:

```
Current: [RHTPA 2.0.0]
Proposed: [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]
```

This correction is scoped to the 2.2.x stream per the issue's stream scope. The 2.1.x versions (2.1.0, 2.1.1) are NOT included because they belong to a different stream and should be tracked by a sibling CVE Jira.

### Step 7 -- Concurrent Triage Detection

No concurrent triages detected for upstream component `quinn-proto`. Proceeding with remediation task creation without risk of duplicates.

### Release Jira Orchestration (Step 7.5)

Before creating remediation tasks, the release Jira structure for the 2.2.x stream would be resolved:
- Search for an existing release Epic matching `RHTPA 2.2.* Release Tasks`
- If found, search for a child release Task matching `RHTPA 2.2.* CVE triage`
- Link remediation tasks to the release Task (Blocks) and link TC-8021 to the release Task (Related)
- Run cross-CVE dedup check (Step 7.5.3) against existing remediation tasks linked to the release Task

### Post-Triage Actions

1. **Add label**: `ai-cve-triaged` to TC-8021
2. **Post summary comment** on TC-8021 documenting:
   - Version impact table
   - Affects Versions correction (RHTPA 2.0.0 -> RHTPA 2.2.0, 2.2.1, 2.2.2)
   - Remediation tasks created (upstream + downstream for 2.2.x)
   - Cross-stream impact notice (2.1.x also affected)
   - Preemptive tasks created for 2.1.x (if applicable)
   - Release Jira references (if created)
   - @mention of the issue's reporter

## Decision Rationale

- **Not Case C** (close as Not a Bug): Supported versions within the issue's scoped stream ARE affected (2.2.0, 2.2.1, 2.2.2 all ship quinn-proto versions below the 0.11.14 fix threshold).
- **Case B applies**: Remediation tasks are needed for the affected versions in the 2.2.x stream.
- **Case A applies**: The issue is stream-scoped and other streams (2.1.x) are also affected, requiring cross-stream impact notification and potentially preemptive remediation tasks.
- **Ecosystem**: Cargo (source dependency) produces 2 tasks per stream -- upstream fix + downstream propagation.
- **Concurrent triage**: No concurrent triages detected on quinn-proto (Step 7 cleared).
