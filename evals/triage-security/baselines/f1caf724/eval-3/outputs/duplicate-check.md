# Duplicate Check -- TC-8003 (Step 4)

## JQL Search Results

A JQL search for sibling Vulnerability issues with the same CVE label was performed:

```
project = TC AND labels = 'CVE-2026-31812' AND issuetype = 10024 AND key != TC-8003
```

**Result: 1 sibling found.**

| Issue | Summary | Status | Labels | Affects Versions | Stream Suffix |
|-------|---------|--------|--------|------------------|---------------|
| TC-7999 | CVE-2026-31812 quinn-proto - Panic on large stream counts [rhtpa-2.2] | In Progress | CVE-2026-31812, pscomponent:org/rhtpa-server | RHTPA 2.2.0, RHTPA 2.2.1 | [rhtpa-2.2] |

## Step 4.1 -- Same-Stream Duplicate Analysis

### Stream comparison

- **TC-8003** stream suffix: `[rhtpa-2.2]` -- maps to stream **2.2.x**
- **TC-7999** stream suffix: `[rhtpa-2.2]` -- maps to stream **2.2.x**

Both issues track the **same CVE** (CVE-2026-31812) for the **same stream** (2.2.x). This is a **same-stream duplicate**.

### Status comparison

- **TC-7999** is in **In Progress** status -- it is already being actively triaged/worked.
- **TC-8003** is in **New** status -- it has not been triaged yet.

### Affects Versions comparison

- **TC-7999** Affects Versions: RHTPA 2.2.0, RHTPA 2.2.1 (more complete)
- **TC-8003** Affects Versions: RHTPA 2.2.0 (incomplete -- missing RHTPA 2.2.1)

TC-7999 already has a more complete Affects Versions set. Per the version impact analysis, the correct Affects Versions for the 2.2.x stream should include RHTPA 2.2.0 and RHTPA 2.2.1 (and 2.2.2 as a retag of 2.2.1, if a corresponding Jira version exists). TC-7999 already covers these.

## Duplicate Determination

**TC-8003 is a duplicate of TC-7999.**

Criteria met for same-stream duplicate (per Step 4.1):
1. Same CVE label: CVE-2026-31812
2. Same stream suffix: [rhtpa-2.2]
3. TC-7999 is open and actively in progress
4. TC-7999's Affects Versions is a superset of TC-8003's Affects Versions

## Recommendation

**Close TC-8003 as Duplicate** of TC-7999.

Proposed actions (pending engineer confirmation):
1. Add comment to TC-8003: "Duplicate of TC-7999 -- same CVE tracked for the same stream [rhtpa-2.2]. Version impact analysis confirms overlap. TC-7999 is already In Progress with Affects Versions [RHTPA 2.2.0, RHTPA 2.2.1]."
2. Transition TC-8003 to Closed with resolution "Duplicate".
3. No remediation tasks needed -- TC-7999 already handles remediation for this CVE in the 2.2.x stream.
