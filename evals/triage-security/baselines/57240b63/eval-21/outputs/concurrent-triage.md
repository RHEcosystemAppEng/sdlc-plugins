# Step 7 -- Concurrent Triage Detection for TC-8020

## Prerequisite Check

The Upstream Affected Component custom field (`customfield_10632`) is configured in Security Configuration. The field is populated on TC-8020 with value `quinn-proto`. Step 7 proceeds.

## JQL Search for In-Progress Triages

**Query executed:**

```
project = TC
  AND issuetype = 10024
  AND cf[10632] ~ 'quinn-proto'
  AND status IN ('In Progress', 'Code Review')
  AND key != TC-8020
```

**Result:** 1 issue returned.

| CVE Issue | Status | Assignee |
|-----------|--------|----------|
| TC-8019 | In Progress | engineer-b@example.com |

## Concurrent Triage Warning

**CONCURRENT TRIAGE DETECTED** on the same upstream component (quinn-proto):

| CVE Issue | Status | Assignee |
|-----------|--------|----------|
| TC-8019 | In Progress | engineer-b@example.com |

Another engineer (engineer-b@example.com) is actively triaging a related CVE (TC-8019) that also affects the `quinn-proto` upstream component. Creating remediation tasks now may produce duplicates if both triages reach Step 8 simultaneously -- the upstream backport task and downstream propagation subtask for quinn-proto would overlap.

## Risk Analysis

The risk is specifically about **duplicate remediation tasks**:

1. TC-8019 is in "In Progress" status, meaning engineer-b is actively performing triage and may be about to create remediation tasks for quinn-proto.
2. TC-8020 (this issue, CVE-2026-31812) also requires remediation for quinn-proto in the 2.2.x stream.
3. If both triages create upstream backport tasks independently, the result would be two tasks targeting the same Cargo.lock update in the same source repository (rhtpa-backend), potentially conflicting or duplicating effort.
4. The Cargo ecosystem remediation pattern creates two tasks (upstream backport + downstream propagation), so the duplication risk spans both tasks.

## Options Presented to Engineer

The following three options are available per the Step 7 protocol:

### Option 1: Wait

Pause execution until TC-8019's triage completes. Once TC-8019 reaches a terminal state (its remediation tasks are created or it is closed), re-run from Step 4.3 to detect any cross-CVE overlap. This is the **safest option** -- it avoids duplicate work entirely and allows Step 4.3's overlap detection to identify if TC-8019's remediation already covers CVE-2026-31812's fix threshold (quinn-proto >= 0.11.14).

**Trade-off:** Delays remediation for TC-8020 until engineer-b finishes TC-8019.

### Option 2: Skip

Skip Step 8 (remediation task creation) entirely for TC-8020. A Jira comment would be posted explaining that task creation was skipped due to concurrent triage on the same component.

**PROPOSAL -- Jira comment (if Skip chosen):**

```
Remediation task creation skipped for CVE-2026-31812.

Reason: Concurrent triage detected -- TC-8019 (In Progress, assigned to
engineer-b@example.com) is actively triaging a different CVE affecting the
same upstream component (quinn-proto). Task creation deferred to avoid
duplicate remediation tasks.

Re-run triage after TC-8019 completes to create tasks or detect cross-CVE
overlap coverage.
```

**Trade-off:** Remediation is deferred indefinitely -- requires manual follow-up.

### Option 3: Proceed

Create remediation tasks for TC-8020 as normal but add the `concurrent-triage-overlap` label to TC-8020. This label ensures that when engineer-b's triage of TC-8019 reaches Step 4.3 (Cross-CVE Overlap Detection), it will find TC-8020 and its remediation tasks, allowing overlap reconciliation.

**PROPOSAL -- Jira mutation (if Proceed chosen):**

```
jira.edit_issue(TC-8020, fields={
  "labels": ["CVE-2026-31812", "pscomponent:org/rhtpa-server", "concurrent-triage-overlap"]
})
```

Then continue to Case A/B/C branching in Step 8 to create remediation tasks.

**Trade-off:** May create duplicate tasks, but the `concurrent-triage-overlap` label provides a mechanism for deduplication during TC-8019's Step 4.3 overlap check.

## Recommendation

**Option 1 (Wait)** is recommended when the other triage is expected to complete soon, as it avoids duplicate work entirely. If timelines are uncertain or the due date (2026-07-15) is approaching, **Option 3 (Proceed)** is the pragmatic choice -- the `concurrent-triage-overlap` label provides a safety net for deduplication.

## Awaiting Engineer Decision

No remediation tasks will be created until the engineer chooses one of the three options above. This is consistent with the skill's guardrail: "Every Jira mutation requires explicit confirmation."
