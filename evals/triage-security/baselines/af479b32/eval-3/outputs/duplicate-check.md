# Duplicate Check -- TC-8003

## Step 4 -- Duplicate, Sibling, Overlap, and Reconciliation Check

### JQL Search

Simulated JQL query:
```
project = TC AND labels = 'CVE-2026-31812' AND issuetype = 10024 AND key != TC-8003
```

Results: 1 issue found.

### Sibling Issue

| Field | Value |
|-------|-------|
| Issue key | TC-7999 |
| Summary | CVE-2026-31812 quinn-proto - Panic on large stream counts [rhtpa-2.2] |
| Status | In Progress |
| Labels | CVE-2026-31812, pscomponent:org/rhtpa-server |
| Affects Versions | RHTPA 2.2.0, RHTPA 2.2.1 |
| Stream suffix | [rhtpa-2.2] |

### Stream Scope Classification

- **TC-8003** (current issue): stream suffix `[rhtpa-2.2]` -> stream **2.2.x**
- **TC-7999** (sibling): stream suffix `[rhtpa-2.2]` -> stream **2.2.x**

Both issues have the **same stream suffix** `[rhtpa-2.2]`, mapping to the same stream **2.2.x**.

Classification: **Same-stream sibling** (duplicate).

### Step 4.1 -- Same-Stream Duplicate Analysis

TC-7999 is a same-stream sibling with:
- Same CVE: CVE-2026-31812
- Same stream: 2.2.x (both carry suffix `[rhtpa-2.2]`)
- Status: **In Progress** (actively being worked on)
- Broader Affects Versions: RHTPA 2.2.0, RHTPA 2.2.1 (superset of TC-8003's RHTPA 2.2.0)

Per Step 4.1 of the triage-security skill: when a same-stream sibling exists and is open or in progress, the recommendation is to **close the current issue (TC-8003) as Duplicate**.

### Duplicate Determination

TC-8003 is a duplicate of TC-7999 because:

1. **Same CVE**: Both issues track CVE-2026-31812 for quinn-proto.
2. **Same stream**: Both are scoped to stream 2.2.x via the `[rhtpa-2.2]` suffix.
3. **TC-7999 is already In Progress**: The sibling is actively being triaged/remediated, meaning work is already underway for this CVE in this stream.
4. **TC-7999 has broader coverage**: TC-7999 already lists Affects Versions RHTPA 2.2.0 and RHTPA 2.2.1, which is a superset of TC-8003's RHTPA 2.2.0.

There is no reason to keep TC-8003 open -- all triage and remediation for CVE-2026-31812 in stream 2.2.x is already tracked by TC-7999.

### CVE-2026-31812 Companion Issues Landscape

| Issue | Stream | Status | Affects Versions |
|-------|--------|--------|------------------|
| TC-7999 | 2.2.x | In Progress | RHTPA 2.2.0, RHTPA 2.2.1 |
| TC-8003 (current, duplicate) | 2.2.x | New | RHTPA 2.2.0 |

### Step 4.3 -- Cross-CVE Overlap Detection

Skipped. The Upstream Affected Component custom field, PS Component custom field, and Stream custom field are not configured in Security Configuration.

### Step 4.4 -- Preemptive Task Reconciliation

Not applicable. TC-8003 is being closed as a duplicate, so no remediation tasks will be created. Preemptive task reconciliation is not needed.
