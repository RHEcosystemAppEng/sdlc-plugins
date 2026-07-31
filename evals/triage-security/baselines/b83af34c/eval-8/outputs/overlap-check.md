# Step 4.3 — Cross-CVE Overlap Detection for TC-8010

## Prerequisite Check

All three required custom fields are available on the current issue:
- Upstream Affected Component (customfield_10632): **axios** -- present and populated
- PS Component (customfield_10669): **pscomponent:org/rhtpa-ui** -- present and populated
- Stream (customfield_10832): **rhtpa-2.2** -- present and populated

Step 4.3 proceeds (all prerequisites met).

## Step 4.3.1 — Extract Upstream Affected Component

Extracted from TC-8010's `customfield_10632`: **axios**

## Step 4.3.2 — Search for Related CVE Jiras

JQL query executed:
```
project = TC AND issuetype = 10024 AND cf[10632] ~ 'axios' AND key != TC-8010
```
Fields requested: `summary, status, labels, issuelinks, customfield_10632, customfield_10669, customfield_10832`

**Search results**: 1 issue returned

| Key | Summary | Status | Upstream Affected Component | PS Component | Stream |
|-----|---------|--------|----------------------------|--------------|--------|
| TC-8008 | CVE-2026-42035 axios - Prototype Pollution via header parsing [rhtpa-2.2] | In Progress | axios | pscomponent:org/rhtpa-ui | rhtpa-2.2 |

## Step 4.3.3 — Filter by PS Component and Stream

Filtering criteria (must match current issue TC-8010):
- PS Component (customfield_10669) must equal: `pscomponent:org/rhtpa-ui`
- Stream (customfield_10832) must equal: `rhtpa-2.2`

| Key | PS Component Match? | Stream Match? | Included? |
|-----|---------------------|---------------|-----------|
| TC-8008 | YES (pscomponent:org/rhtpa-ui) | YES (rhtpa-2.2) | YES |

**TC-8008 passes both filters** — same PS Component and same Stream as TC-8010.

## Step 4.3.4 — Traverse Issue Links on TC-8008

Inspecting TC-8008's `issuelinks` array for linked remediation Tasks with link type `"Depend"`:

| Link Type | Direction | Linked Issue | Summary | Status |
|-----------|-----------|--------------|---------|--------|
| Depend | outward | TC-8009 | Bump axios to 1.9.0 in rhtpa-ui [rhtpa-2.2] | In Progress |

Found 1 remediation Task: **TC-8009**

## Step 4.3.5 — Compare Remediation Coverage

Fetched TC-8009 description to extract bump version:
- **Description excerpt**: "Bump axios from 1.7.4 to 1.9.0 to resolve CVE-2026-42035. The fix requires axios >= 1.8.0."
- **Remediation bump version**: **1.9.0**

Comparison against current CVE's fix threshold:
- Current CVE (CVE-2026-44492) fix threshold: **1.8.2**
- TC-8009 bump version: **1.9.0**
- **1.9.0 >= 1.8.2**: YES — the existing remediation **meets or exceeds** the fix threshold

**Conclusion**: TC-8009 already covers CVE-2026-44492. No new remediation task is needed.

## Step 4.3.6 — Traceability Links and Comment

### 6a. Create Related link: TC-8010 <-> TC-8008

**Idempotency check**: Inspected TC-8010's `issuelinks` array (fetched in Step 1).
TC-8010 has no existing issue links — no link with `type.name = "Related"` and
`inwardIssue.key` or `outwardIssue.key` matching TC-8008 exists.

Action: Create the link.
```
jira.create_link(
  inwardIssue: "TC-8010",
  outwardIssue: "TC-8008",
  type: "Related"
)
```

### 6b. Create Depend link: TC-8010 -> TC-8009

**Idempotency check**: Inspected TC-8010's `issuelinks` array (fetched in Step 1).
TC-8010 has no existing issue links — no link with `type.name = "Depend"` and
`inwardIssue.key` or `outwardIssue.key` matching TC-8009 exists.

Action: Create the link.
```
jira.create_link(
  inwardIssue: "TC-8010",
  outwardIssue: "TC-8009",
  type: "Depend"
)
```

### 6c. Post comment on TC-8010

Comment to be posted on TC-8010:
```
Cross-CVE overlap: existing remediation task TC-8009 (from CVE-2026-42035 / TC-8008)
already bumps axios to 1.9.0, which meets or exceeds this CVE's fix threshold (1.8.2).

Links created:
- Related: TC-8010 <-> TC-8008 (same upstream component: axios)
- Depend: TC-8010 -> TC-8009 (covering remediation)

[Comment Footnote]
```

## Recommendation

Existing remediation task **TC-8009** (from CVE-2026-42035 / TC-8008) already bumps
**axios** to **1.9.0**, which meets or exceeds this CVE's fix threshold (**1.8.2**).
No new remediation task needed.

**Recommendation: Close TC-8010** — the fix is already covered by TC-8009.
