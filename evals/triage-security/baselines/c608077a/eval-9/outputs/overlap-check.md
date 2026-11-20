# TC-8011 — Step 4 / Step 4.3 Cross-CVE Overlap Analysis

## Step 4.1 / 4.2 – Same-CVE siblings

JQL (simulated): `project = TC AND labels = 'CVE-2026-45678' AND issuetype = 10024 AND key != TC-8011`
Result: no siblings provided → no duplicates, no cross-stream companions. Proceed to 4.3.

## Step 4.3 – Cross-CVE overlap detection

### 1. Upstream Affected Component

customfield_10632 on TC-8011 = **webpack** (populated → step runs).

### 2. Related-CVE search

```
jira.search_jql(
  "project = TC AND issuetype = 10024 AND cf[10632] ~ 'webpack' AND key != TC-8011",
  fields: ["summary","status","labels","issuelinks","customfield_10632","customfield_10669","customfield_10832"]
)
```

Result (simulated): **TC-8012** — CVE-2026-43210 webpack - ReDoS in chunk name validation [rhtpa-2.2], Closed (Done).

### 3. Filter by PS Component and Stream

| Field | TC-8011 (current) | TC-8012 | Match |
|---|---|---|---|
| customfield_10632 (Upstream component) | webpack | webpack | yes |
| customfield_10669 (PS Component) | pscomponent:org/rhtpa-ui | pscomponent:org/rhtpa-ui | yes |
| customfield_10832 (Stream) | rhtpa-2.2 | rhtpa-2.2 | yes |

TC-8012 is kept.

### 4. Linked remediation Tasks

TC-8012 issuelinks → **Depend: TC-8013** (remediation Task, Closed/Done)
- Summary: "Bump webpack to 5.96.1 in rhtpa-ui [rhtpa-2.2]"
- Description: "Bump webpack from 5.95.0 to 5.96.1 to resolve CVE-2026-43210. The fix requires webpack >= 5.96.0."
- Bump target version extracted: **5.96.1**

### 5. Coverage comparison

| Item | Version |
|---|---|
| TC-8013 bump target | 5.96.1 |
| TC-8011 (CVE-2026-45678) fix threshold | 5.98.0 |

Semver comparison: 5.96.1 vs 5.98.0 → major equal (5), minor 96 < 98 → **5.96.1 < 5.98.0**.

The bump version is **below** the fix threshold, so TC-8013 does **not** cover CVE-2026-45678. webpack 5.96.1 is still in the affected range (< 5.98.0).

### 6. Findings (presented to engineer)

```
Related CVE Jiras found for webpack in the same stream:

| Related CVE    | Issue   | Remediation Task | Bump Version | Covers This CVE?       |
|----------------|---------|------------------|--------------|------------------------|
| CVE-2026-43210 | TC-8012 | TC-8013          | 5.96.1       | No (threshold: 5.98.0) |

No existing remediation covers this CVE's fix threshold. Proceeding with
new remediation task creation.
```

(No ProdSec Jira account ID is configured, so there is no @mention.)

### Actions NOT taken (covering-remediation branch does not apply)

- No Related link TC-8011 ↔ TC-8012 created by Step 4.3. That link is created only when a covering remediation exists.
- No Depend link TC-8011 → TC-8013 created. TC-8013 does not fix this CVE, and linking it would wrongly signal the CVE as remediated.
- No cross-CVE overlap comment posted.
- No closure recommendation.

### Implication for later steps

- **Step 7.5.3 dedup caution:** if TC-8013 is Blocks-linked to the RHTPA 2.2.x release Task, 7.5.3's component-only match (webpack == webpack) would falsely mark this CVE as dedup'd. Step 4.3 shows by version that TC-8013 is insufficient, and it is already Closed/Done. The engineer should override any such dedup match and create new remediation.
- Useful context for the new task: rhtpa-ui's 2.2 stream presumably ships webpack ≥ 5.96.1 after TC-8013. This is not verified by lock-file evidence, and it is still vulnerable. The new remediation must bump to **≥ 5.98.0**.

## Step 4.4 – Preemptive task reconciliation

JQL (simulated): `project = TC AND issuetype = Task AND labels = 'security-preemptive' AND labels = 'CVE-2026-45678'` → no results provided → none found. Proceed.
