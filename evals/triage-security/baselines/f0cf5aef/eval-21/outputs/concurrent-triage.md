# Step 7 -- Concurrent Triage Detection

## Context

Step 7 runs **after** Steps 3-6 (Affects Versions correction, duplicate/sibling/overlap check, lifecycle check, already-fixed check) and **before** Case A/B/C branching in Step 8 (Remediation). Its purpose is to prevent duplicate remediation tasks when two engineers triage different CVEs that affect the same upstream component at the same time.

## Prerequisite Check

- **Upstream Affected Component custom field**: configured as `customfield_10632`
- **Current issue's component value**: `quinn-proto` (from TC-8020's `customfield_10632`)

Both prerequisites are satisfied. Step 7 proceeds.

## JQL Search for Concurrent Triages

Query executed:

```
project = TC
  AND issuetype = 10024
  AND cf[10632] ~ 'quinn-proto'
  AND status IN ('In Progress', 'Code Review')
  AND key != TC-8020
```

### Search Results

The search returned **1 result**:

| CVE Issue | Status | Assignee |
|-----------|--------|----------|
| TC-8019 | In Progress | engineer-b@example.com |

## Concurrent Triage Warning

A concurrent triage was detected. The following warning is presented to the engineer:

---

**Concurrent triage detected on the same upstream component (quinn-proto):**

| CVE Issue | Status | Assignee |
|-----------|--------|----------|
| TC-8019 | In Progress | engineer-b@example.com |

Another engineer is actively triaging a related CVE that affects the same upstream component (`quinn-proto`). Creating remediation tasks now may produce duplicates if both triages create tasks that bump the same library.

**Options:**

1. **Wait** -- pause until TC-8019's triage completes, then re-run Step 4.3 to detect any overlap. This is the safest option to avoid duplicate remediation work.

2. **Skip** -- skip remediation task creation for TC-8020 entirely. A Jira comment will be added to TC-8020 explaining why task creation was skipped. Appropriate when the other triage (TC-8019) is expected to produce remediation that covers this CVE's fix threshold.

3. **Proceed** -- create remediation tasks now with a `concurrent-triage-overlap` label added to TC-8020, so that TC-8019's Step 4.3 cross-CVE overlap detection will catch the overlap and reconcile. This is appropriate when the fix thresholds differ and both CVEs genuinely need separate remediation.

---

## Analysis

- **TC-8019** is currently In Progress, meaning engineer-b@example.com is actively triaging a different CVE that also affects `quinn-proto`.
- Both TC-8019 and TC-8020 target the same upstream library. If both triages create remediation tasks to bump `quinn-proto`, the project could end up with duplicate work.
- The concurrent triage detection fires **before** Case A/B/C branching, so no remediation tasks or cross-stream impact comments are posted until the user makes a choice.

## User Decision Required

The skill pauses here and waits for the engineer's choice before proceeding:

- If **Wait**: execution stops. The engineer should re-run `/triage-security TC-8020` after TC-8019's triage is complete. At that point, Step 4.3's cross-CVE overlap detection will determine whether TC-8019's remediation already covers TC-8020's fix threshold (0.11.14).

- If **Skip**: Step 8 is skipped entirely. A Jira comment is added to TC-8020:
  > "Remediation task creation skipped due to concurrent triage on quinn-proto (TC-8019 is In Progress, assigned to engineer-b@example.com). Re-run triage after TC-8019 completes to check overlap coverage."
  The `ai-cve-triaged` label is still added and the post-triage summary is still posted.

- If **Proceed**: the `concurrent-triage-overlap` label is added to TC-8020 and the skill continues to Case A/B/C branching. When engineer-b@example.com's triage of TC-8019 reaches Step 4.3, the cross-CVE overlap search on `quinn-proto` will find TC-8020 and its remediation tasks, enabling reconciliation.

## Ordering Rationale

Step 7 is positioned after Steps 3-6 and before Case A/B/C for the following reasons:

1. Steps 3-6 are non-destructive (they correct Affects Versions, detect duplicates, check lifecycle, check already-fixed). These should complete regardless of concurrent triage.
2. Case A/B/C creates remediation tasks (Jira mutations). This is where duplicate work risk exists, so the concurrent triage gate must fire before task creation.
3. By the time Step 7 runs, the full version impact analysis is complete, giving the engineer full context to decide whether to wait, skip, or proceed.
