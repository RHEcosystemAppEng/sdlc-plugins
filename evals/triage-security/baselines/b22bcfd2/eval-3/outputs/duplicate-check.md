# Step 4 -- Duplicate, Sibling, and Overlap Check

## 4.0 -- JQL Search for Sibling Issues

To find sibling Vulnerability issues with the same CVE label, the following JQL query is constructed using the project key and vulnerability issue type ID from Security Configuration:

```
project = TC
  AND labels = 'CVE-2026-31812'
  AND issuetype = 10024
  AND key != TC-8003
```

This query:
- Uses project key **TC** from Jira Configuration
- Filters by the CVE label **CVE-2026-31812** (extracted from TC-8003's labels in Step 1)
- Restricts to vulnerability issue type ID **10024** from Security Configuration
- **Excludes the current issue key TC-8003** to avoid self-matching

### Search Results

The JQL search returns **1 result**:

| Issue | Summary | Status | Labels | Affects Versions |
|-------|---------|--------|--------|------------------|
| TC-7999 | CVE-2026-31812 quinn-proto - Panic on large stream counts [rhtpa-2.2] | In Progress | CVE-2026-31812, pscomponent:org/rhtpa-server | RHTPA 2.2.0, RHTPA 2.2.1 |

## 4.1 -- Sibling Classification

For each sibling found, parse its summary stream suffix to determine its stream scope:

### TC-7999 Analysis

- **TC-7999 stream suffix**: `[rhtpa-2.2]` --> stream **2.2.x**
- **TC-8003 stream suffix** (current issue): `[rhtpa-2.2]` --> stream **2.2.x**

**Classification: Same-stream sibling**

Both TC-7999 and TC-8003 have the stream suffix `[rhtpa-2.2]`, mapping to the same stream (2.2.x). They track the same CVE (CVE-2026-31812) for the same stream. This is a **duplicate**, not a companion tracker.

### Sibling Classification Summary

| Sibling Issue | Sibling Stream | Current Issue Stream | Classification |
|---------------|---------------|---------------------|----------------|
| TC-7999 | 2.2.x (`[rhtpa-2.2]`) | 2.2.x (`[rhtpa-2.2]`) | **Same-stream duplicate** |

## 4.1 -- Same-Stream Duplicate Detection

TC-7999 is a same-stream sibling that is currently open (status: **In Progress**). Per the triage-security skill's Step 4.1 rules:

- TC-7999 tracks the **same CVE** (CVE-2026-31812) for the **same stream** (2.2.x)
- TC-7999 is already **In Progress**, meaning it has been triaged and is being actively worked on
- TC-7999 has **Affects Versions**: RHTPA 2.2.0, RHTPA 2.2.1 -- covering the versions relevant to the 2.2.x stream
- TC-8003 is redundant -- the same CVE is already being tracked and remediated via TC-7999

**Proposed action**: Close TC-8003 as **Duplicate** of TC-7999.

This is presented as a recommendation for engineer confirmation before any Jira mutation is executed.

## Duplicate Detection Short-Circuit

Because a same-stream duplicate was detected, the triage flow **short-circuits** at this point. The following steps are **NOT performed**:

- Step 2 (Version Impact Analysis) -- skipped
- Step 3 (Affects Versions Correction) -- skipped
- Step 4.2 (Cross-stream coordination) -- not applicable (same-stream case)
- Step 4.3 (Cross-CVE overlap detection) -- skipped
- Step 4.4 (Preemptive task reconciliation) -- skipped
- Step 5 (Version Lifecycle Check) -- skipped
- Step 6 (Already Fixed Check) -- skipped
- Step 7 (Concurrent Triage Detection) -- skipped
- Step 8 (Remediation task creation) -- skipped

No remediation tasks are created for TC-8003. The existing remediation tracked under TC-7999 covers this CVE for stream 2.2.x.
