# Step 4.3 -- Cross-CVE Overlap Analysis: TC-8010

## Prerequisite Check

- Upstream Affected Component custom field (customfield_10632): **configured**
- PS Component custom field (customfield_10669): **configured**
- Stream custom field (customfield_10832): **configured**
- All prerequisite fields are present; Step 4.3 proceeds.

## Current Issue Context

| Field | Value |
|-------|-------|
| Issue Key | TC-8010 |
| CVE ID | CVE-2026-44492 |
| Upstream Affected Component | axios |
| PS Component | pscomponent:org/rhtpa-ui |
| Stream | rhtpa-2.2 |
| Fix Threshold | 1.8.2 |

## JQL Search for Related CVE Jiras

Query: `project = TC AND issuetype = 10024 AND cf[10632] ~ 'axios' AND key != TC-8010`

### Results

| Issue | CVE | Summary | Status | Upstream Affected Component | PS Component | Stream |
|-------|-----|---------|--------|----------------------------|--------------|--------|
| TC-8008 | CVE-2026-42035 | axios - Prototype Pollution via header parsing [rhtpa-2.2] | In Progress | axios | pscomponent:org/rhtpa-ui | rhtpa-2.2 |

### Filtering

- TC-8008 PS Component (pscomponent:org/rhtpa-ui) matches current issue: **YES**
- TC-8008 Stream (rhtpa-2.2) matches current issue: **YES**
- TC-8008 passes filter -- relevant for overlap analysis

## Remediation Task Traversal

TC-8008 issue links inspected for Depend-type links to remediation Tasks:

| Linked Task | Link Type | Summary | Status |
|-------------|-----------|---------|--------|
| TC-8009 | Depend | Bump axios to 1.9.0 in rhtpa-ui [rhtpa-2.2] | In Progress |

### TC-8009 Remediation Coverage Analysis

- **Description excerpt**: "Bump axios from 1.7.4 to 1.9.0 to resolve CVE-2026-42035. The fix requires axios >= 1.8.0."
- **Bump target version**: **1.9.0**
- **Current CVE fix threshold**: **1.8.2**
- **Comparison**: 1.9.0 >= 1.8.2

**Result: COVERED** -- The existing remediation task TC-8009 bumps axios to 1.9.0, which meets and exceeds the current CVE's fix threshold of 1.8.2.

## Overlap Finding

Existing remediation task **TC-8009** (from CVE-2026-42035 / TC-8008) already bumps **axios** to **1.9.0**, which meets or exceeds this CVE's fix threshold (**1.8.2**). No new remediation task is needed for TC-8010.

### Proposed Actions

1. **Create Related link** between TC-8010 and TC-8008 (same upstream component -- cross-CVE traceability):
   - `create_link(inwardIssue: TC-8010, outwardIssue: TC-8008, type: "Related")`

2. **Create Depend link** from TC-8009 (covering remediation task) to TC-8010 (current CVE):
   - `create_link(inwardIssue: TC-8010, outwardIssue: TC-8009, type: "Depend")`

3. **Post overlap comment** on TC-8010:
   ```
   Cross-CVE overlap: existing remediation task TC-8009 (from
   CVE-2026-42035 / TC-8008) already bumps axios to 1.9.0, which meets
   or exceeds this CVE's fix threshold (1.8.2).

   Links created:
   - Related: TC-8010 <-> TC-8008 (same upstream component)
   - Depend: TC-8010 -> TC-8009 (covering remediation)
   ```

### Recommendation

**Close TC-8010** -- the fix is already covered by TC-8009. No new remediation task creation is needed.
