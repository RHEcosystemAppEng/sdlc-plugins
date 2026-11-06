# Step 4 – Duplicate, Sibling, Overlap, and Reconciliation Check: TC-8003

## Sibling Search (simulated)

JQL that would run:

```
project = TC AND labels = 'CVE-2026-31812' AND issuetype = 10024 AND key != TC-8003
```

Simulated result: 1 issue.

| Issue | Summary | Stream suffix | Stream | Status | Affects Versions |
|-------|---------|---------------|--------|--------|------------------|
| TC-7999 | CVE-2026-31812 quinn-proto - Panic on large stream counts [rhtpa-2.2] | [rhtpa-2.2] | 2.2.x | In Progress | RHTPA 2.2.0, RHTPA 2.2.1 |
| TC-8003 (current) | CVE-2026-31812 quinn-proto - Panic on large stream counts [rhtpa-2.2] | [rhtpa-2.2] | 2.2.x | New | RHTPA 2.2.0 |

## Classification

- **TC-7999 is a same-stream sibling.** Both issues have the stream suffix `[rhtpa-2.2]`, which maps to stream 2.2.x. They share the same CVE label (CVE-2026-31812), the same component label (`pscomponent:org/rhtpa-server`), and the same library (quinn-proto).
- No different-stream siblings were found, so Step 4.2 does not apply and no Related links are created.

## Step 4.1 – Same-stream Duplicate

Condition: a same-stream sibling exists and is open or in progress. TC-7999 is **In Progress**, so the condition is met.

**Recommendation: close TC-8003 as Duplicate of TC-7999.**

Overlap evidence:
- Every Affects Version on TC-8003 (RHTPA 2.2.0) is already on TC-7999 (RHTPA 2.2.0, RHTPA 2.2.1).
- The version impact analysis confirms 2.2.0 is affected (quinn-proto 0.11.9 < 0.11.14), so both issues track the same real exposure in the same stream.
- TC-7999 is older (lower key) and already being worked on, so it is the canonical tracker.

Proposed actions (each needs engineer confirmation; none executed in this eval):

1. **Comment on TC-8003:**
   > Duplicate of TC-7999: same CVE (CVE-2026-31812) tracked for the same stream [rhtpa-2.2] (2.2.x). Version impact analysis confirms overlap: RHTPA 2.2.0 (quinn-proto 0.11.9), 2.2.1 (0.11.12), and 2.2.2 (retag of 2.2.1) are affected; 2.2.3 and 2.2.4 ship 0.11.14 (fixed).
   >
   > [Comment Footnote per shared/comment-footnote.md, skill name `triage-security`]
2. **Transition TC-8003 to Closed** with resolution **Duplicate**.
3. **Assign TC-8003** to the current user.
4. Optional link: a Duplicate/Related link from TC-8003 to TC-7999 for traceability. The procedure does not require it, so it is offered and only created if the engineer approves.

## Problem Found on the Canonical Issue TC-7999

The lock-file evidence shows **RHTPA 2.2.2 is also affected**. It is a backend retag of 2.2.1 (v0.4.8, quinn-proto 0.11.12). TC-7999's Affects Versions [RHTPA 2.2.0, RHTPA 2.2.1] **leave out 2.2.2**.

- Recommendation, outside this skill's automatic scope for TC-8003: tell the TC-7999 owner, or re-run `/triage-security TC-7999`, so its Affects Versions become [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]. This should not be changed silently on an issue that is In Progress.
- No other version overlap problems: both issues only claim 2.2.x versions, which is correct for a same-stream duplicate.

## Step 4.3 – Cross-CVE Overlap Detection

**Skipped.** The Upstream Affected Component, PS Component, and Stream custom fields are not configured in Security Configuration.

## Step 4.4 – Preemptive Task Reconciliation

Simulated JQL:

```
project = TC AND issuetype = Task AND labels = 'security-preemptive' AND labels = 'CVE-2026-31812' ORDER BY created DESC
```

The eval provides no result for this search, so I assume no preemptive tasks exist and no reconciliation is needed. Either way, remediation for 2.2.x belongs to TC-7999.

## Result

**Duplicate found.** TC-8003 is a same-stream duplicate of TC-7999 (In Progress). The triage path ends with a Duplicate closure, and TC-8003 gets no remediation tasks.
