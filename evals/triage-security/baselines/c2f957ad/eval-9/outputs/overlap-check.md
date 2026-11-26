# Step 4 – Duplicate, Sibling, Overlap, and Reconciliation Check: TC-8011

## 4.0–4.2 – Same-CVE siblings

JQL: `project = TC AND labels = 'CVE-2026-45678' AND issuetype = 10024 AND key != TC-8011`

The eval provided no siblings with the same CVE label. There are no same-stream duplicates (4.1) and no cross-stream companions (4.2). Continue to 4.3.

## 4.3 – Cross-CVE overlap detection

### 1. Upstream Affected Component
customfield_10632 on TC-8011 = **webpack** (populated).

### 2. Related CVE search
```
project = TC AND issuetype = 10024 AND cf[10632] ~ 'webpack' AND key != TC-8011
fields: summary, status, labels, issuelinks, customfield_10632, customfield_10669, customfield_10832
```
Result: **TC-8012** (CVE-2026-43210 webpack - ReDoS in chunk name validation [rhtpa-2.2]), Closed (Done).

### 3. Filter by PS Component and Stream

| Field | TC-8011 (current) | TC-8012 | Match |
|---|---|---|---|
| customfield_10632 | webpack | webpack | Yes |
| customfield_10669 | pscomponent:org/rhtpa-ui | pscomponent:org/rhtpa-ui | Yes |
| customfield_10832 | rhtpa-2.2 | rhtpa-2.2 | Yes |

TC-8012 passes the filter.

### 4. Traverse issue links
TC-8012 has a Depend link to **TC-8013**, "Bump webpack to 5.96.1 in rhtpa-ui [rhtpa-2.2]", Closed (Done).
Description: "Bump webpack from 5.95.0 to 5.96.1 to resolve CVE-2026-43210. The fix requires webpack >= 5.96.0."

### 5. Compare remediation coverage

| Item | Version |
|---|---|
| TC-8013 bump target | 5.96.1 |
| TC-8011 (CVE-2026-45678) fix threshold | 5.98.0 |

Semver comparison: 5.96.1 vs 5.98.0. The major versions are equal (5) and the minor version 96 < 98, so **5.96.1 < 5.98.0**. The bump target is **below** the fix threshold. TC-8013 fixed CVE-2026-43210 (which needs >= 5.96.0) but **does not cover** CVE-2026-45678.

Assumption: after TC-8013, rhtpa-ui in 2.2.x is at 5.96.1. That is still inside this CVE's affected range (< 5.98.0), so it remains vulnerable. This is inferred from the task description only. Lock-file evidence was not available (see data-extraction.md).

### 6. Findings (no covering remediation)

```
Related CVE Jiras found for webpack in the same stream:

| Related CVE    | Issue   | Remediation Task | Bump Version | Covers This CVE?       |
|----------------|---------|------------------|--------------|------------------------|
| CVE-2026-43210 | TC-8012 | TC-8013          | 5.96.1       | No (threshold: 5.98.0) |

No existing remediation covers this CVE's fix threshold. Proceeding with
new remediation task creation.
```

Because nothing covers this CVE, the "covering remediation" actions are **not** performed:
- No Related link TC-8011 <-> TC-8012 is created by Step 4.3. That link is only required on a confirmed overlap. It can still be added later at the engineer's discretion.
- No Depend link TC-8011 -> TC-8013. TC-8013 is not this CVE's remediation.
- No overlap comment and no close recommendation.
- No ProdSec @mention, because no ProdSec Jira account ID is configured.

## 4.4 – Preemptive task reconciliation

JQL: `project = TC AND issuetype = Task AND labels = 'security-preemptive' AND labels = 'CVE-2026-45678'`. The eval provided no results, so there is nothing to reconcile.

## Downstream caution for Step 7.5.3

The Step 7.5.3 dedup matches on Upstream Affected Component only, with no version check. If TC-8013 is Blocks-linked to the RHTPA 2.2.x release Task, a component-only match (webpack == webpack) would wrongly mark this stream as dedup'd and skip task creation. The version-aware result from Step 4.3 (TC-8013 does **not** cover 5.98.0) should take precedence. TC-8013 is also Closed (Done), so it cannot absorb new work. Do not dedup against TC-8013.
