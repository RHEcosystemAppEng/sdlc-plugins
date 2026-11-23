# Step 4 – Duplicate, Sibling, Overlap, and Reconciliation Check: TC-8011

## Step 4 / 4.1 / 4.2 – Same-CVE siblings

- JQL (simulated): `project = TC AND labels = 'CVE-2026-45678' AND issuetype = 10024 AND key != TC-8011`
- No result was provided for this query, and TC-8011 has no existing links. Result: **no same-CVE siblings**.
- No same-stream duplicates (4.1) and no cross-stream companions (4.2), so the check moves on to 4.3.

## Step 4.3 – Cross-CVE overlap detection

**Prerequisite note:** the mock CLAUDE.md Security Configuration does not declare the Upstream Affected Component, PS Component, or Stream custom fields. Read strictly, Step 4.3 would be skipped. The task instructions supply the field (`customfield_10632` = `webpack`) and the JQL result, so the step was run using those values. The config gap should be fixed by adding these fields to Security Configuration.

### 1. Upstream Affected Component

- `customfield_10632` on TC-8011 is **webpack**, which is populated, so the step proceeds.

### 2. Related-CVE search

```
project = TC AND issuetype = 10024 AND cf[10632] ~ 'webpack' AND key != TC-8011
fields: summary, status, labels, issuelinks, customfield_10632, customfield_10669, customfield_10832
```

Result: **TC-8012** (CVE-2026-43210, "webpack - ReDoS in chunk name validation [rhtpa-2.2]", Closed/Done).

### 3. Filter by PS Component and Stream

| Field | TC-8011 (current) | TC-8012 | Match |
|---|---|---|---|
| customfield_10632 (Upstream Affected Component) | webpack | webpack | Yes |
| customfield_10669 (PS Component) | pscomponent:org/rhtpa-ui | pscomponent:org/rhtpa-ui | Yes |
| customfield_10832 (Stream) | rhtpa-2.2 | rhtpa-2.2 | Yes |

TC-8012 is relevant: same component, same PS component, same stream.

### 4. Traverse issue links on TC-8012

- `Depend` link: **TC-8013**, "Bump webpack to 5.96.1 in rhtpa-ui [rhtpa-2.2]" (Closed/Done).
- TC-8013 description: "Bump webpack from 5.95.0 to 5.96.1 to resolve CVE-2026-43210. The fix requires webpack >= 5.96.0."
- Extracted bump target: **webpack 5.96.1**.

### 5. Compare remediation coverage

| Item | Version |
|---|---|
| TC-8013 bump target | 5.96.1 |
| TC-8011 (CVE-2026-45678) fix threshold | 5.98.0 |

Semver comparison: 5.96.1 vs 5.98.0. Major versions are equal (5) and minor 96 < 98, so **5.96.1 < 5.98.0**.

The bump version is **below** the fix threshold, so the existing remediation **does NOT cover** this CVE. Even after TC-8013, rhtpa-ui 2.2 ships webpack 5.96.1, which is still inside CVE-2026-45678's affected range (< 5.98.0).

### 6. Findings presented to the engineer (the "no covering remediation" branch)

```
Related CVE Jiras found for webpack in the same stream:

| Related CVE    | Issue   | Remediation Task | Bump Version | Covers This CVE?        |
|----------------|---------|------------------|--------------|-------------------------|
| CVE-2026-43210 | TC-8012 | TC-8013          | 5.96.1       | No (threshold: 5.98.0)  |

No existing remediation covers this CVE's fix threshold. Proceeding with
new remediation task creation.
```

(No ProdSec @mention because no ProdSec Jira account ID is configured.)

### Actions NOT taken (and why)

The covering-remediation branch was not taken, so none of the following are proposed:
- **No** Related link TC-8011 ↔ TC-8012
- **No** Depend link TC-8011 → TC-8013
- **No** cross-CVE overlap comment
- **No** recommendation to close TC-8011 as covered by TC-8013

Under Step 4.3, linking and the overlap comment happen only when the existing remediation meets or exceeds the fix threshold. A Depend link to TC-8013 would wrongly suggest that TC-8013 remediates CVE-2026-45678.

## Step 4.4 – Preemptive task reconciliation

- JQL (simulated): `project = TC AND issuetype = Task AND labels = 'security-preemptive' AND labels = 'CVE-2026-45678'`
- No result was provided, so no matching preemptive task exists. The check proceeds silently to Step 5.

## Downstream consistency note (Step 7.5.3)

Step 7.5.3's cross-CVE dedup matches remediation Tasks by Upstream Affected Component only, with no version check. If TC-8013 is linked (Blocks) to the RHTPA 2.2.x release Task, 7.5.3 would match "webpack" and could wrongly skip task creation. The Step 4.3 finding (TC-8013 bumps only to 5.96.1, below 5.98.0) should take precedence. TC-8013 must not be treated as a dedup match for CVE-2026-45678, and new remediation tasks are still required. TC-8013 is also already Closed/Done, so it cannot absorb more work.
