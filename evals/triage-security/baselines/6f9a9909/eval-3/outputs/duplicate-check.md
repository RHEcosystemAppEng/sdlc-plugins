# Duplicate Check -- TC-8003

## Step 4 -- Duplicate, Sibling, Overlap, and Reconciliation Check

### JQL Search Results

A JQL search for sibling issues with the same CVE label
(`project = TC AND labels = 'CVE-2026-31812' AND issuetype = 10024 AND key != TC-8003`)
returned one result:

| Issue | Summary | Status | Labels | Affects Versions | Stream Suffix |
|-------|---------|--------|--------|------------------|---------------|
| TC-7999 | CVE-2026-31812 quinn-proto - Panic on large stream counts [rhtpa-2.2] | In Progress | CVE-2026-31812, pscomponent:org/rhtpa-server | RHTPA 2.2.0, RHTPA 2.2.1 | [rhtpa-2.2] |

### Stream Classification

- **TC-8003** stream suffix: `[rhtpa-2.2]` -- mapped to stream **2.2.x**
- **TC-7999** stream suffix: `[rhtpa-2.2]` -- mapped to stream **2.2.x**

Both issues have the **same stream suffix** (`[rhtpa-2.2]`).

### Step 4.1 -- Same-Stream Duplicate Detection

TC-7999 is a **same-stream sibling** of TC-8003:
- Same CVE: CVE-2026-31812
- Same stream: 2.2.x (both have suffix `[rhtpa-2.2]`)
- TC-7999 is already **In Progress** (open and being actively worked)
- TC-7999 already has broader Affects Versions coverage: RHTPA 2.2.0 and RHTPA 2.2.1
  (TC-8003 only has RHTPA 2.2.0)

Per the skill's Step 4.1 rule: "If a same-stream sibling exists and is open or in
progress, recommend closing the current issue as Duplicate."

**Recommendation: Close TC-8003 as Duplicate of TC-7999.**

### Affects Versions Comparison

| Field | TC-8003 (current) | TC-7999 (sibling) |
|-------|--------------------|--------------------|
| Affects Versions | RHTPA 2.2.0 | RHTPA 2.2.0, RHTPA 2.2.1 |

TC-7999 already has a superset of TC-8003's Affects Versions. The version impact
analysis shows RHTPA 2.2.0, 2.2.1, and 2.2.2 are affected -- TC-7999 already
tracks two of these. No Affects Versions correction is needed on TC-7999 as part
of this triage (though 2.2.2 as a retag of 2.2.1 may warrant inclusion separately).

### Steps 4.2, 4.3, 4.4

- **Step 4.2 (Cross-stream coordination):** Not applicable. TC-7999 is same-stream,
  not cross-stream.
- **Step 4.3 (Cross-CVE overlap):** Skipped. The Upstream Affected Component, PS
  Component, and Stream custom fields are not configured in the project's Security
  Configuration. Step 4.3 requires all three fields to be present.
- **Step 4.4 (Preemptive task reconciliation):** Not applicable. The issue is being
  closed as duplicate -- no remediation tasks will be created.
