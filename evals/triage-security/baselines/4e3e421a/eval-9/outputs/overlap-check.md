# Step 4 – Duplicate, Sibling, Overlap, and Reconciliation Check: TC-8011

## Step 4 / 4.1 / 4.2 – Same-CVE Siblings

Simulated JQL:
```
project = TC AND labels = 'CVE-2026-45678' AND issuetype = 10024 AND key != TC-8011
```
Result: the input contains no siblings with the same CVE label.
- 4.1 Same-stream duplicates: none.
- 4.2 Cross-stream companions: none.
- Result: proceed to Step 4.3.

## Step 4.3 – Cross-CVE Overlap Detection

### Prerequisites
- Upstream Affected Component field (customfield_10632): set to `webpack` on TC-8011, so the check proceeds.
- PS Component field (customfield_10669): `pscomponent:org/rhtpa-ui`
- Stream field (customfield_10832): `rhtpa-2.2`

### 1. Upstream Affected Component
`webpack`

### 2. Related CVE search (simulated)
```
project = TC AND issuetype = 10024 AND cf[10632] ~ 'webpack' AND key != TC-8011
fields: summary, status, labels, issuelinks, customfield_10632, customfield_10669, customfield_10832
```
Result: **TC-8012** (CVE-2026-43210, "webpack - ReDoS in chunk name validation [rhtpa-2.2]"), status Closed (Done).

### 3. Filter by PS Component and Stream

| Field | TC-8011 (current) | TC-8012 | Match |
|---|---|---|---|
| customfield_10632 | webpack | webpack | Yes |
| customfield_10669 | pscomponent:org/rhtpa-ui | pscomponent:org/rhtpa-ui | Yes |
| customfield_10832 | rhtpa-2.2 | rhtpa-2.2 | Yes |

TC-8012 is relevant: same component and same stream.

### 4. Traverse issue links
TC-8012 `issuelinks` contains:
- **Depend** link to **TC-8013** (remediation Task): "Bump webpack to 5.96.1 in rhtpa-ui [rhtpa-2.2]", status Closed (Done).
- Description excerpt: "Bump webpack from 5.95.0 to 5.96.1 to resolve CVE-2026-43210. The fix requires webpack >= 5.96.0."
- Extracted bump target version: **5.96.1**

### 5. Compare remediation coverage

| Item | Version |
|---|---|
| TC-8013 bump target | 5.96.1 |
| TC-8011 (CVE-2026-45678) fix threshold | 5.98.0 |

Semver comparison: major 5 = 5, minor **96 < 98**, so **5.96.1 < 5.98.0**.

The bump version is **below** the fix threshold. The existing remediation **does NOT cover** this CVE. After TC-8013, webpack 5.96.1 is still inside the vulnerable range (< 5.98.0).

### 6. Findings presented to the engineer

```
Related CVE Jiras found for webpack in the same stream:

| Related CVE    | Issue   | Remediation Task | Bump Version | Covers This CVE?        |
|----------------|---------|------------------|--------------|-------------------------|
| CVE-2026-43210 | TC-8012 | TC-8013          | 5.96.1       | No (threshold: 5.98.0)  |

No existing remediation covers this CVE's fix threshold. Proceeding with
new remediation task creation.
```

- ProdSec Jira account ID is not configured, so the @mention is omitted.
- The "covering remediation" actions are **not** taken, because the overlap does not cover this CVE:
  - No Related link TC-8011 to TC-8012 is created by Step 4.3.
  - No Depend link TC-8011 to TC-8013 is created. TC-8013 does not remediate this CVE, and linking it would wrongly signal that the CVE is fixed.
  - No cross-CVE overlap comment is posted, and closure is **not** recommended.
- Useful context for remediation: TC-8013 is Done, so 2.2.x likely ships webpack 5.96.1. That still has to be confirmed with lock-file evidence. Any new task needs to bump webpack from at least 5.96.1 to **>= 5.98.0**.

## Step 4.4 – Preemptive Task Reconciliation (simulated)

```
project = TC AND issuetype = Task AND labels = 'security-preemptive' AND labels = 'CVE-2026-45678' ORDER BY created DESC
```
Result: no preemptive tasks were provided, so there is nothing to reconcile. Proceed to Step 5.
