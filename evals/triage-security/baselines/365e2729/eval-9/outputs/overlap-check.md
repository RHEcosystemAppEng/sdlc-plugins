# Step 4 – Duplicate, Sibling, and Overlap Check: TC-8011

## Step 4 (4.1 / 4.2) – Same-CVE siblings

JQL: `project = TC AND labels = 'CVE-2026-45678' AND issuetype = 10024 AND key != TC-8011`

The mock data shows no other issue with label CVE-2026-45678:
- 4.1 Same-stream duplicates: none.
- 4.2 Cross-stream companions: none.

Proceed to Step 4.3.

## Step 4.3 – Cross-CVE overlap detection

### 1. Upstream Affected Component

`customfield_10632` on TC-8011 = **webpack** (populated, so the step runs).

### 2. Related CVE Jira search

```
project = TC AND issuetype = 10024 AND cf[10632] ~ 'webpack' AND key != TC-8011
fields: summary, status, labels, issuelinks, customfield_10632, customfield_10669, customfield_10832
```

Result: **TC-8012** (CVE-2026-43210 webpack - ReDoS in chunk name validation [rhtpa-2.2]), status Closed (Done).

### 3. Filter by PS Component and Stream

| Field | TC-8011 (current) | TC-8012 (candidate) | Match |
|-------|-------------------|---------------------|-------|
| customfield_10632 Upstream Affected Component | webpack | webpack | Yes |
| customfield_10669 PS Component | pscomponent:org/rhtpa-ui | pscomponent:org/rhtpa-ui | Yes |
| customfield_10832 Stream | rhtpa-2.2 | rhtpa-2.2 | Yes |

TC-8012 is kept as a relevant related CVE.

### 4. Traverse issue links

TC-8012 `issuelinks`, filtered to type `Depend`:
- **TC-8013**, remediation Task, "Bump webpack to 5.96.1 in rhtpa-ui [rhtpa-2.2]", status Closed (Done)
  - Description: "Bump webpack from 5.95.0 to 5.96.1 to resolve CVE-2026-43210. The fix requires webpack >= 5.96.0."
  - Extracted bump target version: **5.96.1**

### 5. Compare remediation coverage

| Item | Version |
|------|---------|
| TC-8013 bump target | 5.96.1 |
| CVE-2026-45678 fix threshold (Step 1) | 5.98.0 |

Semver comparison: major 5 = 5, minor **96 < 98**. 5.96.1 is **below** 5.98.0.

**The existing remediation does NOT cover this CVE.** After TC-8013, rhtpa-ui
ships webpack 5.96.1, which is still inside CVE-2026-45678's affected range
(< 5.98.0). The 5.96.0 floor TC-8013 cites belongs to CVE-2026-43210, not to
this CVE.

### 6. Findings (non-covering branch)

```
Related CVE Jiras found for webpack in the same stream:

| Related CVE    | Issue   | Remediation Task | Bump Version | Covers This CVE?       |
|----------------|---------|------------------|--------------|------------------------|
| CVE-2026-43210 | TC-8012 | TC-8013          | 5.96.1       | No (threshold: 5.98.0) |

No existing remediation covers this CVE's fix threshold. Proceeding with
new remediation task creation.
```

(No ProdSec Jira account ID is configured, so there's no @mention.)

### Actions NOT taken (and why)

The covering-branch actions apply only when the bump meets or exceeds the
threshold. This case is non-covering, so none of them are performed:
- **No** Related link TC-8011 to TC-8012 is created by Step 4.3.
- **No** Depend link TC-8011 to TC-8013 is created. TC-8013 doesn't remediate this CVE, and linking it would make TC-8011 look remediated.
- **No** "Cross-CVE overlap" comment and **no** close recommendation.
- No new remediation is suppressed. Step 8 must still create tasks.

Optional informational note for the triage summary: the earlier webpack bump
(TC-8013, 5.95.0 to 5.96.1) means the new remediation's starting baseline is
probably 5.96.1, and the new target must be **>= 5.98.0**.

### Downstream consistency (Step 7.5.3)

Step 7.5.3 matches existing remediation Tasks by Upstream Affected Component
only, not by version. If TC-8013 is Blocks-linked to the RHTPA 2.2.x release
Task, a literal 7.5.3 match on `webpack` would wrongly dedup TC-8011 against
TC-8013. Step 4.3 has shown that TC-8013 (5.96.1) doesn't meet the 5.98.0
threshold, and TC-8013 is already Closed. So TC-8013 must **not** be treated as
a covering task in 7.5.3, and Step 8 must not be skipped.

## Step 4.4 – Preemptive task reconciliation

JQL: `project = TC AND issuetype = Task AND labels = 'security-preemptive' AND labels = 'CVE-2026-45678'`

The mock data has no preemptive tasks, so nothing is reconciled. Proceed to Step 5.

## Overlap check result

**NOT COVERED.** Related CVE TC-8012 / remediation TC-8013 bumps webpack only to
5.96.1, below this CVE's 5.98.0 fix threshold. TC-8011 needs its own
remediation.
