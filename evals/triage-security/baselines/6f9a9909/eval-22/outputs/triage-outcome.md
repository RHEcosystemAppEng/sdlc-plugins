# Triage Outcome -- TC-8021 (CVE-2026-31812)

## Summary

CVE-2026-31812 affects quinn-proto versions before 0.11.14. The issue is scoped
to stream 2.2.x (per the `[rhtpa-2.2]` suffix in the summary). Triage outcome
is **Case A + Case B**: cross-stream impact detected and remediation tasks needed.

## Triage Decision: Case B -- Affected (create remediation tasks)

### Affected versions within scope (2.2.x)

| Version | quinn-proto | Affected? |
|---------|-------------|-----------|
| 2.2.0 | 0.11.9 | YES |
| 2.2.1 | 0.11.12 | YES |
| 2.2.2 | (retag of 2.2.1) | YES |
| 2.2.3 | 0.11.14 | NO (fixed) |
| 2.2.4 | 0.11.14 | NO (fixed) |

Three versions in the 2.2.x stream (2.2.0, 2.2.1, 2.2.2) ship a vulnerable
version of quinn-proto. Versions 2.2.3 and 2.2.4 already ship the fixed version
(0.11.14) and are not affected.

### Remediation tasks for 2.2.x stream

Since quinn-proto is a Cargo (source dependency) ecosystem, two tasks are
created per stream:

1. **Upstream backport task**: Bump quinn-proto to >= 0.11.14 on branch
   `release/0.4.z` in the `backend` source repository.
   - Labels: `ai-generated-jira`, `Security`, `CVE-2026-31812`
   - Linked to TC-8021 with "Depend"
   - Note: Upstream fix already available at v0.4.11+ (quinn-proto 0.11.14),
     so the backport may already be on the branch. Verify branch HEAD.

2. **Downstream propagation subtask**: Update backend reference in
   `rhtpa-release.0.4.z` Konflux release repo to pick up the upstream fix.
   - Labels: `ai-generated-jira`, `Security`, `CVE-2026-31812`
   - Linked to TC-8021 with "Depend"
   - Blocked by the upstream backport task (link type: "Blocks")
   - Source pinning method: `artifacts.lock.yaml` (download URL contains tag)

## Case A -- Cross-Stream Impact

The issue is scoped to the 2.2.x stream, but the version impact analysis reveals
that the **2.1.x** stream is also affected:

| Version | Stream | quinn-proto | Affected? |
|---------|--------|-------------|-----------|
| 2.1.0 | 2.1.x | 0.11.9 | YES |
| 2.1.1 | 2.1.x | 0.11.9 | YES |

### Cross-stream actions

1. **Post cross-stream impact comment** on TC-8021:
   > Cross-stream impact: quinn-proto < 0.11.14 also affects stream 2.1.x
   > based on lock file analysis. These streams are tracked by companion
   > issues (see Related links) or may require separate PSIRT triage.

2. **Check for existing CVE Jiras** for the 2.1.x stream: search for sibling
   Vulnerability issues with the CVE-2026-31812 label and a `[rhtpa-2.1]`
   stream suffix.

3. **If no CVE Jira exists for 2.1.x**: create preemptive remediation tasks
   (with `security-preemptive` label, "Related" link type) for the 2.1.x
   stream:
   - Upstream backport: bump quinn-proto to >= 0.11.14 on `release/0.3.z`
   - Downstream propagation: update backend ref in `rhtpa-release.0.3.z`

4. **If a CVE Jira already exists for 2.1.x**: skip task creation -- that
   stream will be triaged through its own CVE issue.

## Affects Versions Correction (Step 3)

- **Current**: RHTPA 2.0.0 (incorrect -- PSIRT assigned a version that does not
  correspond to any configured stream)
- **Proposed**: RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2
- **Rationale**: Lock file analysis shows quinn-proto < 0.11.14 in versions
  2.2.0 (0.11.9), 2.2.1 (0.11.12), and 2.2.2 (retag of 2.2.1). Versions
  2.2.3+ ship 0.11.14 (fixed). Correction is scoped to the 2.2.x stream
  per the issue's `[rhtpa-2.2]` suffix.

## Step 7 -- Concurrent Triage Detection

No concurrent triages detected for quinn-proto. JQL query for in-progress
Vulnerability issues with `cf[10632] ~ 'quinn-proto'` returned zero results.
Proceeding with remediation task creation.

## Post-Triage Actions

1. Add `ai-cve-triaged` label to TC-8021
2. Post summary comment on TC-8021 with:
   - Version impact table
   - Affects Versions correction (RHTPA 2.0.0 -> RHTPA 2.2.0, 2.2.1, 2.2.2)
   - Links to all remediation tasks created
   - Cross-stream impact note for 2.1.x
   - @mention of the issue reporter
3. Transition TC-8021 to In Progress
