# Step 4 -- Duplicate, Sibling, and Overlap Check

## JQL Search for Sibling Issues

**Query** (simulated):
```
project = TC AND labels = 'CVE-2026-31812' AND issuetype = 10024 AND key != TC-8003
```

**Results**: 1 sibling found.

| Issue | Summary | Status | Labels | Affects Versions | Stream Suffix |
|-------|---------|--------|--------|------------------|---------------|
| TC-7999 | CVE-2026-31812 quinn-proto - Panic on large stream counts [rhtpa-2.2] | In Progress | CVE-2026-31812, pscomponent:org/rhtpa-server | RHTPA 2.2.0, RHTPA 2.2.1 | [rhtpa-2.2] |

## Sibling Classification

- **TC-8003** stream suffix: `[rhtpa-2.2]` --> stream 2.2.x
- **TC-7999** stream suffix: `[rhtpa-2.2]` --> stream 2.2.x
- Classification: **Same-stream sibling**

Both issues track the same CVE (CVE-2026-31812) for the same stream (2.2.x). TC-7999 is already In Progress, meaning it is actively being triaged or remediated.

## Step 4.1 -- Same-Stream Duplicate Detection

**Condition met**: A same-stream sibling (TC-7999) exists and is open/in progress.

Per the SKILL.md procedure (Step 4.1):

> If a same-stream sibling exists and is open or in progress:
> - Recommendation: Close the current issue as Duplicate.
> - Present the sibling issue key and its Affects Versions to the engineer.

**Sibling details**:
- TC-7999 is in status **In Progress** -- actively being worked
- TC-7999 Affects Versions: **RHTPA 2.2.0, RHTPA 2.2.1** -- superset of TC-8003's RHTPA 2.2.0
- Both issues track the identical CVE for the identical stream
- TC-8003 is redundant; all version coverage is handled by TC-7999

## Duplicate Confirmation

**Recommendation**: Close TC-8003 as **Duplicate** of TC-7999.

**Proposed actions** (presented for engineer confirmation, not executed):

1. **Add comment** to TC-8003:
   > "Duplicate of TC-7999 -- same CVE (CVE-2026-31812) tracked for the same stream [rhtpa-2.2]. TC-7999 is already In Progress with Affects Versions [RHTPA 2.2.0, RHTPA 2.2.1]. Version impact analysis confirms overlap."

2. **Transition** TC-8003 to **Closed** with resolution **Duplicate**.

3. **Assign** TC-8003 to the current user.

## Short-Circuit Decision

Because TC-8003 is a same-stream duplicate, the triage procedure **short-circuits** at Step 4.1. The following steps are skipped:

- Step 4.2 (Cross-stream coordination) -- not applicable, sibling is same-stream
- Step 4.3 (Cross-CVE overlap detection) -- skipped; Upstream Affected Component field not configured; also moot because issue is being closed as duplicate
- Step 4.4 (Preemptive task reconciliation) -- not applicable, issue is being closed
- Step 5 (Version Lifecycle Check) -- not applicable, issue is being closed as duplicate
- Step 6 (Already Fixed Check) -- not applicable, issue is being closed as duplicate
- Step 7 (Concurrent Triage Detection) -- not applicable, no remediation tasks to create
- Step 7.5 (Release Jira Orchestration) -- not applicable, no remediation tasks to create
- Step 8 (Remediation) -- not applicable, no remediation tasks to create

No remediation tasks are created. The duplicate detection at Step 4.1 is the terminal action.
