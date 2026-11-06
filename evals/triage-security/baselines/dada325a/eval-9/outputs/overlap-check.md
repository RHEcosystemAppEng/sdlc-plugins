# Step 4 – Duplicate, Sibling, and Overlap Check: TC-8011

## 4.1 / 4.2 – Same-CVE siblings

Simulated JQL:
```
project = TC AND labels = 'CVE-2026-45678' AND issuetype = 10024 AND key != TC-8011
```
No siblings were provided for CVE-2026-45678. So there is no same-stream duplicate and no cross-stream companion. Continue to Step 4.3.

## 4.3 – Cross-CVE overlap detection

### 1. Upstream Affected Component
`customfield_10632` on TC-8011 = **webpack** (filled in, so the step runs).

### 2. Related CVE search (simulated)
```
jira.search_jql(
  "project = TC AND issuetype = 10024 AND cf[10632] ~ 'webpack' AND key != TC-8011",
  fields: ["summary", "status", "labels", "issuelinks",
           "customfield_10632", "customfield_10669", "customfield_10832"]
)
```
Result: **TC-8012**, CVE-2026-43210 webpack - ReDoS in chunk name validation [rhtpa-2.2] (Closed / Done).

### 3. Filter by PS Component and Stream

| Field | TC-8011 (current) | TC-8012 | Match |
|---|---|---|---|
| customfield_10632 (Upstream component) | webpack | webpack | Yes |
| customfield_10669 (PS Component) | pscomponent:org/rhtpa-ui | pscomponent:org/rhtpa-ui | Yes |
| customfield_10832 (Stream) | rhtpa-2.2 | rhtpa-2.2 | Yes |

TC-8012 passes the filter and counts as a related CVE.

### 4. Traverse issue links
TC-8012 `issuelinks` → **Depend** → **TC-8013** (remediation Task)
- Summary: Bump webpack to 5.96.1 in rhtpa-ui [rhtpa-2.2]
- Status: Closed (Done)
- Description: "Bump webpack from 5.95.0 to 5.96.1 to resolve CVE-2026-43210. The fix requires webpack >= 5.96.0."
- **Bump target version extracted: 5.96.1**

### 5. Compare remediation coverage

| Value | Version |
|---|---|
| TC-8013 bump target | 5.96.1 |
| TC-8011 (CVE-2026-45678) fix threshold | 5.98.0 |

Semver comparison: 5.96.1 vs 5.98.0. Major versions are equal (5) and the minor is 96 < 98, so **5.96.1 < 5.98.0**.

TC-8013's bump is **below** the current CVE's fix threshold. webpack 5.96.1 is still in CVE-2026-45678's affected range (< 5.98.0). **The existing remediation does NOT cover this CVE.**

### 6. Findings (presented to engineer)

```
Related CVE Jiras found for webpack in the same stream:

| Related CVE    | Issue   | Remediation Task | Bump Version | Covers This CVE?        |
|----------------|---------|------------------|--------------|-------------------------|
| CVE-2026-43210 | TC-8012 | TC-8013          | 5.96.1       | No (threshold: 5.98.0)  |

No existing remediation covers this CVE's fix threshold. Proceeding with
new remediation task creation.
```

(No ProdSec Jira account ID is configured, so there is no @mention.)

### Actions NOT taken (and why)

The "covering remediation exists" branch does not apply. So none of the following happen:
- **No** Related link TC-8011 ↔ TC-8012 from the covering-overlap branch
- **No** Depend link TC-8011 → TC-8013. TC-8013 does not fix this CVE, and a Depend link would wrongly mark it as this CVE's remediation.
- **No** "Cross-CVE overlap" comment saying the fix is already covered
- **No** recommendation to close TC-8011

### Implication for Step 7.5.3 (Cross-CVE dedup)

TC-8013 has the same upstream component (webpack), but Step 4.3 shows its bump (5.96.1) is below 5.98.0. It is also already Closed/Done. If TC-8013 shows up under the RHTPA 2.2.x release Task, Step 7.5.3 must **not** count it as covering this CVE and skip task creation. Matching only on component name would hide a real exposure. New remediation tasks are still needed.

## 4.4 – Preemptive task reconciliation (simulated)
```
project = TC AND issuetype = Task AND labels = 'security-preemptive' AND labels = 'CVE-2026-45678'
```
No preemptive tasks were provided, so nothing needs reconciling. Continue to Step 5.
