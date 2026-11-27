# Step 4 – Duplicate, Sibling, and Overlap Check: TC-8011

## Step 4 sibling search (same CVE label)

JQL (simulated):
```
project = TC AND labels = 'CVE-2026-45678' AND issuetype = 10024 AND key != TC-8011
```
Result: no siblings appear in the supplied data.
- 4.1 Same-stream duplicates: none, so the issue is not a duplicate.
- 4.2 Cross-stream companions: none.

## Step 4.3 – Cross-CVE overlap detection

### Prerequisite note
Step 4.3 needs three fields: Upstream Affected Component, PS Component, and Stream. The project's Security Configuration does not declare any of them. Under a strict reading of the skill, that means the step is skipped. The task explicitly provides the field IDs and values (`customfield_10632`, `customfield_10669`, `customfield_10832`), so the analysis below uses them. The project should add these fields to its Security Configuration so this step runs reliably.

### 1. Upstream Affected Component of current issue
`customfield_10632` = **webpack** (populated, so the step continues)

### 2. Related CVE search
```
jira.search_jql(
  "project = TC AND issuetype = 10024 AND cf[10632] ~ 'webpack' AND key != TC-8011",
  fields: ["summary","status","labels","issuelinks","customfield_10632","customfield_10669","customfield_10832"]
)
```
Result (supplied): **TC-8012**, CVE-2026-43210 webpack - ReDoS in chunk name validation [rhtpa-2.2], status Closed (Done).

### 3. Filter by PS Component and Stream

| Field | TC-8011 (current) | TC-8012 | Match |
|-------|-------------------|---------|-------|
| customfield_10632 | webpack | webpack | Yes |
| customfield_10669 | pscomponent:org/rhtpa-ui | pscomponent:org/rhtpa-ui | Yes |
| customfield_10832 | rhtpa-2.2 | rhtpa-2.2 | Yes |

TC-8012 is relevant because it has the same component, PS component, and stream.

### 4. Traverse issue links
TC-8012 `issuelinks` has a **Depend** link to **TC-8013**, the remediation Task:
- Summary: Bump webpack to 5.96.1 in rhtpa-ui [rhtpa-2.2]
- Status: Closed (Done)
- Description: "Bump webpack from 5.95.0 to 5.96.1 to resolve CVE-2026-43210. The fix requires webpack >= 5.96.0."

### 5. Compare remediation coverage
- Version TC-8013 bumps to: **5.96.1**
- This CVE's fix threshold (CVE-2026-45678, from Step 1): **5.98.0**
- 5.96.1 < 5.98.0, so the bump version is **below** the fix threshold.
- Conclusion: **the existing remediation does NOT cover CVE-2026-45678.** Builds that contain TC-8013's fix still ship a vulnerable webpack, 5.96.1, which falls inside the affected range of < 5.98.0.

### 6. Findings presented to engineer

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
- **No Related link TC-8011 <-> TC-8012 and no Depend link TC-8011 -> TC-8013.** The skill creates these links, and the cross-CVE overlap comment, only in the "covering remediation exists" branch. This is the non-covering branch, so Step 4.3 makes no Jira mutations.
- **No close recommendation** at this step. The issue is not covered.

### Carry-forward to Step 7.5.3 (cross-CVE dedup)
Step 7.5.3 matches on the Upstream Affected Component (webpack) alone, not on version. If TC-8013 were found linked (Blocks) to the RHTPA 2.2.x release Task, a naive component match would wrongly mark this stream as dedup'd. Step 4.3 has shown that TC-8013 does not reach 5.98.0, and TC-8013 is already Closed. So TC-8013 **must not** count as a covering task in 7.5.3, and this CVE needs new remediation.

## Step 4.4 – Preemptive task reconciliation
```
project = TC AND issuetype = Task AND labels = 'security-preemptive' AND labels = 'CVE-2026-45678'
```
No preemptive tasks appear in the supplied data. Proceeding.
