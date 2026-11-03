# Step 7 – Concurrent Triage Detection: TC-8020

## Prerequisite check

- The Upstream Affected Component custom field is configured (`customfield_10632`,
  per the eval assumption), so the step runs.
- The value on TC-8020 is `quinn-proto` (non-empty), so the step proceeds.

## JQL search (simulated, not executed)

```
project = TC AND issuetype = 10024 AND cf[10632] ~ 'quinn-proto'
  AND status IN ('In Progress', 'Code Review') AND key != TC-8020
fields: summary, status, labels, assignee
```

The field number `10632` is the numeric part of `customfield_10632`.

## Result (as given by the eval)

One result was returned, so a concurrent triage is detected.

## Warning presented to the engineer

```
⚠️ Concurrent triage detected on the same upstream component (quinn-proto):

| CVE Issue | Status      | Assignee               |
|-----------|-------------|------------------------|
| TC-8019   | In Progress | engineer-b@example.com |

Another engineer is actively triaging a related CVE. Creating remediation
tasks now may produce duplicates.

Options:
1. Wait: pause until the other triage completes, then re-run Step 4.3
   to detect any overlap
2. Skip: skip remediation task creation for this CVE
3. Proceed: create tasks anyway with a `concurrent-triage-overlap` label
   so the other engineer's Step 4.3 catches the overlap
```

## Why this matters for TC-8020

- TC-8019 and TC-8020 both target `quinn-proto` in the backend. A remediation for
  either one is a Cargo bump of quinn-proto, possibly in the same 2.2.x (and 2.1.x)
  streams. If both triages reach Step 8 at the same time, the result could be two
  overlapping upstream-bump and downstream-propagation task pairs.
- TC-8019's CVE ID, stream, and fix threshold are not known from the search
  result. Step 4.3 already ran for TC-8020 before TC-8019 had remediation tasks,
  so it found no covering remediation. Nothing yet shows whether TC-8019's eventual
  bump will reach >= 0.11.14.

## Handling of each choice (per protocol)

| Choice | Action |
|---|---|
| Wait | Stop execution. Tell the engineer to re-run triage once TC-8019 leaves In Progress / Code Review; Step 4.3 will then detect whether TC-8019's remediation covers 0.11.14. |
| Skip | Skip Step 8 (no remediation tasks). Post a Jira comment (with Comment Footnote) on TC-8020 explaining that task creation was skipped because of concurrent triage TC-8019 on quinn-proto. |
| Proceed | Add the `concurrent-triage-overlap` label to TC-8020 (after confirmation), then continue to Step 7.5 and Case A/B/C. The label lets TC-8019's Step 4.3 pick up the overlap. |

## Gate status

**Blocking.** The protocol says to continue to Case A/B/C only after the engineer
chooses. No choice was supplied in this eval, so execution stops at this gate and
no Step 7.5 or Step 8 Jira mutations are performed.

**Recommendation:** **Wait** (option 1). TC-8019 is actively in progress on the same
crate. Waiting a short time and then re-running Step 4.3 is the cheapest way to avoid
duplicate quinn-proto bump tasks. If the 2026-07-15 due date (already passed) makes
waiting unacceptable, choose **Proceed** so the `concurrent-triage-overlap` label is
applied.
