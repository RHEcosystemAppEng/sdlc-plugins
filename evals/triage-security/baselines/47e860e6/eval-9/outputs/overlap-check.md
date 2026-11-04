# Step 4 – Duplicate, Sibling, Overlap, and Reconciliation Check: TC-8011

## Step 4 / 4.1 / 4.2 – Same-CVE siblings

JQL (simulated): `project = TC AND labels = 'CVE-2026-45678' AND issuetype = 10024 AND key != TC-8011`

- The input data shows no sibling Vulnerability issues for CVE-2026-45678.
- **No same-stream duplicates.** Step 4.1 does not apply.
- **No cross-stream companions.** Step 4.2 does not apply.

## Step 4.3 – Cross-CVE overlap detection

### Prerequisite note

The mock CLAUDE.md Security Configuration does **not** declare the Upstream Affected Component, PS Component, or Stream custom field IDs. Read strictly, Step 4.3 would be skipped. However, the issue itself has these fields populated (`customfield_10632`, `customfield_10669`, `customfield_10832`), and the task supplies the JQL result. So the overlap analysis was run with those field IDs. **Recommendation:** add them to Security Configuration so future runs do not skip this step.

### 1. Upstream Affected Component

- `customfield_10632` on TC-8011 is **webpack**. It is populated, so the check proceeds.

### 2. Related CVE search

```
project = TC AND issuetype = 10024 AND cf[10632] ~ 'webpack' AND key != TC-8011
fields: summary, status, labels, issuelinks, customfield_10632, customfield_10669, customfield_10832
```

Result: **TC-8012**, CVE-2026-43210 webpack - ReDoS in chunk name validation [rhtpa-2.2], status Closed (Done).

### 3. Filter by PS Component and Stream

| Field | TC-8011 (current) | TC-8012 | Match? |
|-------|-------------------|---------|--------|
| customfield_10632 (Upstream component) | webpack | webpack | Yes |
| customfield_10669 (PS Component) | pscomponent:org/rhtpa-ui | pscomponent:org/rhtpa-ui | Yes |
| customfield_10832 (Stream) | rhtpa-2.2 | rhtpa-2.2 | Yes |

TC-8012 is relevant because it has the same component and the same stream.

### 4. Linked remediation Tasks

TC-8012 `issuelinks` contains a **Depend** link to **TC-8013**:
- Summary: "Bump webpack to 5.96.1 in rhtpa-ui [rhtpa-2.2]"
- Status: Closed (Done)
- Description: "Bump webpack from 5.95.0 to 5.96.1 to resolve CVE-2026-43210. The fix requires webpack >= 5.96.0."
- **Bump target version: 5.96.1**

### 5. Coverage comparison

| Item | Version |
|------|---------|
| TC-8013 bump target | **5.96.1** |
| CVE-2026-45678 fix threshold (TC-8011) | **5.98.0** |
| Comparison | 5.96.1 **<** 5.98.0 (minor version 96 < 98) |

**5.96.1 is below the fix threshold of 5.98.0, so TC-8013 does NOT cover CVE-2026-45678.** webpack 5.96.1 is still inside this CVE's affected range (< 5.98.0).

### 6. Findings presented to engineer

```
Related CVE Jiras found for webpack in the same stream:

| Related CVE     | Issue   | Remediation Task | Bump Version | Covers This CVE?        |
|-----------------|---------|------------------|--------------|-------------------------|
| CVE-2026-43210  | TC-8012 | TC-8013          | 5.96.1       | No (threshold: 5.98.0)  |

No existing remediation covers this CVE's fix threshold. Proceeding with
new remediation task creation.
```

- ProdSec @mention: omitted because no ProdSec Jira account ID is configured.

### Actions NOT taken, and why

The "covering remediation exists" branch only applies when the bump meets or exceeds the threshold, which it does not here. So:
- **No** Related link TC-8011 ↔ TC-8012 is created as an overlap traceability link.
- **No** Depend link TC-8011 → TC-8013. TC-8013 is not a covering remediation.
- **No** "Cross-CVE overlap: ... meets or exceeds" comment is posted.
- **No** recommendation to close TC-8011 as covered by TC-8013.

The non-covering branch defines no Jira mutation. TC-8012/TC-8013 are recorded as context only: the earlier bump moved webpack to 5.96.1, which may be the baseline for the new bump. That baseline still has to be confirmed from lock-file evidence.

## Step 4.4 – Preemptive task reconciliation

JQL (simulated): `project = TC AND issuetype = Task AND labels = 'security-preemptive' AND labels = 'CVE-2026-45678' ORDER BY created DESC`

- No preemptive task appears in the input data. **No reconciliation.** Proceed to Step 5.
