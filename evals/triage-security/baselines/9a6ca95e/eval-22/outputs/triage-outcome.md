# Triage Outcome for TC-8021 (CVE-2026-31812)

## Version Impact Summary

| Version | Stream | quinn-proto | Affected? | Notes |
|---|---|---|---|---|
| 2.1.0 | 2.1.x | 0.11.9 | YES | |
| 2.1.1 | 2.1.x | 0.11.9 | YES | |
| 2.2.0 | 2.2.x | 0.11.9 | YES | |
| 2.2.1 | 2.2.x | 0.11.12 | YES | |
| 2.2.2 | 2.2.x | -- | YES | retag of 2.2.1 |
| 2.2.3 | 2.2.x | 0.11.14 | NO | ships fixed version |
| 2.2.4 | 2.2.x | 0.11.14 | NO | ships fixed version |

## Triage Decision: Case A + Case B (Affected with Cross-Stream Impact)

### Rationale

TC-8021 is scoped to stream **2.2.x** (per the summary suffix `[rhtpa-2.2]`). Within that stream, versions 2.2.0, 2.2.1, and 2.2.2 ship quinn-proto versions below the fix threshold of 0.11.14, so they are **affected**. Versions 2.2.3 and 2.2.4 ship the fixed version 0.11.14 and are **not affected**.

Because at least one version in the scoped stream is affected, this is **Case A** -- remediation tasks are required.

Additionally, the version impact analysis reveals that stream **2.1.x** (versions 2.1.0, 2.1.1) is also affected -- both ship quinn-proto 0.11.9. Since 2.1.x is outside this issue's stream scope, this triggers **Case B** -- cross-stream impact with proactive remediation.

### Step 3 -- Affects Versions Correction

- **Current**: `[RHTPA 2.0.0]` -- incorrect, no 2.0.x stream exists in the supportability matrix
- **Corrected**: `[RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]` -- the affected versions within the 2.2.x stream scope, based on lock file analysis at pinned commits

RHTPA 2.0.0 is removed because it does not correspond to any real version. RHTPA 2.2.3 and 2.2.4 are excluded because they ship the fixed version.

### Step 7 -- Concurrent Triage Detection

No concurrent triages detected for upstream component `quinn-proto`. The JQL query for in-progress CVE triages with `cf[10632] ~ 'quinn-proto'` returned zero results. Proceeding with remediation task creation.

### Case A -- Remediation Tasks for Stream 2.2.x

Since the ecosystem is **Cargo** (source dependency), two remediation tasks are created:

**Task 1: Upstream Backport**
- Summary: `Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (rhtpa-2.2)`
- Repository: backend (rhtpa-backend)
- Target Branch: `release/0.4.z`
- Action: Update quinn-proto dependency to >= 0.11.14 in Cargo.lock
- Labels: `ai-generated-jira`, `Security`, `CVE-2026-31812`
- Linked to TC-8021 with link type "Depend"
- Upstream fix PR: https://github.com/quinn-rs/quinn/pull/2048

**Task 2: Downstream Propagation (blocked by Task 1)**
- Summary: `Propagate CVE-2026-31812 fix: update backend ref in rhtpa-release.0.4.z (rhtpa-2.2)`
- Repository: rhtpa-release.0.4.z
- Target Branch: main
- Source Pinning Method: `artifacts.lock.yaml` (download URL contains tag)
- Action: Update the backend reference to the merged commit/tag that includes the quinn-proto fix
- Labels: `ai-generated-jira`, `Security`, `CVE-2026-31812`
- Linked to upstream task with link type "Blocks"
- Linked to TC-8021 with link type "Depend"

### Case B -- Cross-Stream Impact (Stream 2.1.x)

The version impact analysis shows that stream **2.1.x** is also affected:
- 2.1.0 ships quinn-proto 0.11.9 (affected)
- 2.1.1 ships quinn-proto 0.11.9 (affected)

**Cross-stream impact comment** (posted to TC-8021):

> Cross-stream impact: quinn-proto < 0.11.14 also affects stream 2.1.x based on lock file analysis. This stream is tracked by companion issues (see Related links) or may require separate PSIRT triage.

A search for sibling Vulnerability issues with label `CVE-2026-31812` and stream suffix `[rhtpa-2.1]` would determine whether a companion CVE Jira already exists for the 2.1.x stream. If no companion exists, preemptive remediation tasks would be created for 2.1.x:

**Preemptive Task 1: Upstream Backport (2.1.x)**
- Summary: `Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (rhtpa-2.1)`
- Repository: backend (rhtpa-backend)
- Target Branch: `release/0.3.z`
- Labels: `ai-generated-jira`, `Security`, `CVE-2026-31812`, `security-preemptive`
- Linked to TC-8021 with link type "Related" (preemptive, not "Depend")

**Preemptive Task 2: Downstream Propagation (2.1.x, blocked by Preemptive Task 1)**
- Summary: `Propagate CVE-2026-31812 fix: update backend ref in rhtpa-release.0.3.z (rhtpa-2.1)`
- Repository: rhtpa-release.0.3.z
- Target Branch: main
- Labels: `ai-generated-jira`, `Security`, `CVE-2026-31812`, `security-preemptive`
- Linked to TC-8021 with link type "Related"

### Post-Triage Summary

After all actions are complete:

1. **Label**: Add `ai-cve-triaged` label to TC-8021
2. **Transition**: Move TC-8021 to "In Progress" status
3. **Summary comment**: Post to TC-8021 documenting:
   - Version impact table (all streams)
   - Affects Versions correction: `[RHTPA 2.0.0]` changed to `[RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]`
   - Remediation tasks created for 2.2.x (upstream + downstream)
   - Cross-stream impact on 2.1.x with preemptive remediation tasks (if no companion CVE Jira exists)
   - @mention of the issue reporter (PSIRT analyst)
   - Comment Footnote per shared/comment-footnote.md (skill: triage-security)
