# Triage Outcome for TC-8020

## Summary

**Issue**: TC-8020 -- CVE-2026-31812 quinn-proto - Panic on large stream counts [rhtpa-2.2]
**CVE**: CVE-2026-31812
**Library**: quinn-proto
**Fix threshold**: >= 0.11.14
**Ecosystem**: Cargo (source dependency)
**Issue stream scope**: 2.2.x

## Triage Decision: Case B (Affected) -- with Step 7 Concurrent Triage Gate

### Version Impact Summary

**Stream 2.2.x (in scope):**

| Version | quinn-proto | Affected? |
|---------|-------------|-----------|
| RHTPA 2.2.0 | 0.11.9 | YES |
| RHTPA 2.2.1 | 0.11.12 | YES |
| RHTPA 2.2.2 | 0.11.12 (retag of 2.2.1) | YES |
| RHTPA 2.2.3 | 0.11.14 | NO (fixed) |
| RHTPA 2.2.4 | 0.11.14 | NO (fixed) |

**Stream 2.1.x (cross-stream, for Case A):**

| Version | quinn-proto | Affected? |
|---------|-------------|-----------|
| RHTPA 2.1.0 | 0.11.9 | YES |
| RHTPA 2.1.1 | 0.11.9 | YES |

### Step 3 -- Affects Versions Correction

The PSIRT-assigned Affects Version is **RHTPA 2.0.0**, which does not correspond to any configured version stream (no 2.0.x stream exists). This is incorrect.

**Correction (scoped to 2.2.x stream):**
- Current: `[RHTPA 2.0.0]`
- Proposed: `[RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]`

Versions 2.2.3 and 2.2.4 are excluded because they ship quinn-proto 0.11.14, which is at or above the fix threshold. The 2.1.x versions are excluded from this issue's Affects Versions because they belong to a different stream (would be handled by a sibling CVE issue or Case A preemptive tasks).

### Steps 4-6 Results

- **Step 4 (Duplicate/Sibling Check)**: No sibling Vulnerability issues assumed for this eval. Proceed.
- **Step 4.3 (Cross-CVE Overlap)**: Would require PS Component and Stream custom fields; assumed not configured beyond Upstream Affected Component for this eval, or no covering remediation found. Proceed.
- **Step 5 (Version Lifecycle)**: All affected versions (2.2.0, 2.2.1, 2.2.2) assumed to be within active support. Proceed.
- **Step 6 (Already Fixed)**: No resolved sibling issues found. The fix exists in 2.2.3+ but the earlier versions still need remediation. Proceed.

### Step 7 -- Concurrent Triage Detection (Key Step)

**This step fires before Case A/B/C branching.**

A JQL search for in-progress triages on the same upstream component (`quinn-proto`) returned:

| CVE Issue | Status | Assignee |
|-----------|--------|----------|
| TC-8019 | In Progress | engineer-b@example.com |

The skill presents a warning with three options:

1. **Wait** -- pause until TC-8019 completes, then re-run to check overlap
2. **Skip** -- skip remediation task creation, add comment explaining why
3. **Proceed** -- create tasks with `concurrent-triage-overlap` label

**The engineer must choose before the skill continues to Case A/B/C.**

### Outcome Depending on User Choice

#### If user chooses "Proceed" (or "Wait"/"Skip"):

**Wait**: Execution halts. No remediation tasks created. Engineer re-runs triage after TC-8019 completes.

**Skip**: No remediation tasks created. Comment added to TC-8020 documenting the skip reason. The `ai-cve-triaged` label is added. Post-triage summary is posted.

**Proceed**: The `concurrent-triage-overlap` label is added to TC-8020, then:

- **Case A (Cross-stream impact)** applies because this issue is scoped to 2.2.x and the 2.1.x stream is also affected:
  - Post cross-stream impact comment on TC-8020:
    > "Cross-stream impact: quinn-proto < 0.11.14 also affects stream 2.1.x based on lock file analysis. These streams are tracked by companion issues (see Related links) or may require separate PSIRT triage."
  - Check for existing CVE Jiras for 2.1.x with same CVE label.
  - If no sibling CVE Jira exists for 2.1.x, create preemptive remediation tasks (with `security-preemptive` label, "Related" link to TC-8020).

- **Case B (Remediation task creation)** applies for the 2.2.x stream:
  - Since quinn-proto is a Cargo (source dependency) ecosystem, create **2 tasks** for the 2.2.x stream:
    1. **Upstream backport task**: Bump quinn-proto to >= 0.11.14 in rhtpa-backend on branch `release/0.4.z`
    2. **Downstream propagation task**: Propagate the updated backend to the Konflux release repo rhtpa-release.0.4.z (blocked by the upstream task)
  - Both tasks linked to TC-8020 with "Depend" link type
  - Downstream task linked to upstream task with "Blocks" link type

### Post-Triage Actions

Regardless of the Step 7 outcome:

1. **Add `ai-cve-triaged` label** to TC-8020
2. **Post summary comment** to TC-8020 documenting:
   - Version impact table
   - Affects Versions correction (RHTPA 2.0.0 -> RHTPA 2.2.0, 2.2.1, 2.2.2)
   - Step 7 concurrent triage finding (TC-8019)
   - Triage outcome and any remediation tasks created
   - @mention of the issue reporter (PSIRT analyst)
   - Comment Footnote per shared/comment-footnote.md

## Key Finding

The critical aspect of this triage is that **Step 7 (Concurrent Triage Detection) must run before Case A/B/C branching** in Step 8. TC-8019 is actively being triaged by engineer-b@example.com and also targets quinn-proto. If both triages create remediation tasks simultaneously, the project could end up with duplicate bump tasks for the same library. The three-option gate (wait/skip/proceed) gives the triaging engineer control over how to handle this situation, and the `concurrent-triage-overlap` label (if "Proceed" is chosen) ensures the other engineer's cross-CVE overlap detection (Step 4.3) can reconcile.
