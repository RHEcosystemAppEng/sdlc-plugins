# Step 4 -- Duplicate and Sibling Check: TC-8003

## JQL Search

The following JQL query was used to search for sibling issues:

```
project = TC AND labels = 'CVE-2026-31812' AND issuetype = 10024 AND key != TC-8003
```

## Search Results

| Issue | Summary | Status | Labels | Affects Versions | Stream Suffix |
|-------|---------|--------|--------|------------------|---------------|
| TC-7999 | CVE-2026-31812 quinn-proto - Panic on large stream counts [rhtpa-2.2] | In Progress | CVE-2026-31812, pscomponent:org/rhtpa-server | RHTPA 2.2.0, RHTPA 2.2.1 | [rhtpa-2.2] |

## Classification

### TC-7999 vs TC-8003

- **TC-7999 stream suffix**: [rhtpa-2.2] --> stream 2.2.x
- **TC-8003 stream suffix**: [rhtpa-2.2] --> stream 2.2.x
- **Classification**: **Same-stream sibling** (duplicate)

Both issues track the same CVE (CVE-2026-31812) for the same version stream
(2.2.x). TC-7999 is already **In Progress**, meaning active remediation work
has begun on the existing issue.

### Affects Versions Comparison

- **TC-7999**: RHTPA 2.2.0, RHTPA 2.2.1
- **TC-8003**: RHTPA 2.2.0 (current, incomplete)

TC-7999 already has the correct and more complete Affects Versions set. The
versions affected by this CVE in the 2.2.x stream (RHTPA 2.2.0 and RHTPA 2.2.1)
are already tracked by TC-7999.

## Duplicate Detection Result

**TC-8003 is a duplicate of TC-7999.**

Per Step 4.1 of the triage-security methodology, when a same-stream sibling
exists and is open or in progress, the recommendation is to close the current
issue as Duplicate.

TC-7999 is the authoritative tracker for CVE-2026-31812 in the 2.2.x stream:
- It is already In Progress (active work underway)
- It has the correct Affects Versions (RHTPA 2.2.0, RHTPA 2.2.1)
- It covers the same CVE, same component, and same stream as TC-8003

There is no additional value in keeping TC-8003 open.
