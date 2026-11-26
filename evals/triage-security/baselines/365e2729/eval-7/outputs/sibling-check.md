# Step 4 – Duplicate, Sibling, and Overlap Check: TC-8006

## Sibling search (simulated)

```
jira.search_jql(
  "project = TC AND labels = 'CVE-2026-31812' AND issuetype = 10024 AND key != TC-8006"
)
```

Result (as stated in the eval): one issue.

| Issue | Summary suffix | Stream | Status | Affects Versions |
|---|---|---|---|---|
| TC-8001 | [rhtpa-2.2] | 2.2.x | In Progress | RHTPA 2.2.0, RHTPA 2.2.1 |

## Classification

- Current issue TC-8006: suffix `[rhtpa-2.1]`, so stream 2.1.x.
- TC-8001: suffix `[rhtpa-2.2]`, so stream 2.2.x.
- The streams differ, so TC-8001 is a **different-stream sibling** (a companion tracker), **not a duplicate**.

## 4.1 – Same-stream duplicates

There are no same-stream siblings. No Duplicate closure is recommended.

## 4.2 – Cross-stream coordination

### 4.2.1 Existing-link check (idempotency)

The skill checks the `issuelinks` array from the Step 1 `get_issue` response for a link where:
- `type.name == "Related"`: **match** (Type: Related)
- `inwardIssue.key` or `outwardIssue.key == "TC-8001"`: **match** (outwardIssue = TC-8001, direction TC-8006 -> TC-8001, link ID 1990401)

Both conditions hold, so the link already exists. Log:

> "Related link to TC-8001 already exists — skipping"

**No `jira.create_link` call is made.** The direction of the existing link (outward) does not matter, because the check accepts either `inwardIssue` or `outwardIssue`. No duplicate Related link is created, and no confirmation prompt is needed because no mutation is proposed.

### 4.2.2 Affects Versions overlap check

- TC-8006: current [RHTPA 2.1.0]; proposed after Step 3: [RHTPA 2.1.0, RHTPA 2.1.1]. All are 2.1.x.
- TC-8001: [RHTPA 2.2.0, RHTPA 2.2.1]. All are 2.2.x.
- The two sets do not intersect, so there is **no version overlap** and no overlap warning.

Side observation (not in TC-8006's scope): the lock file analysis shows RHTPA 2.2.2 is also affected, because it is a retag of 2.2.1 at v0.4.8 with quinn-proto 0.11.12. TC-8001 does not list it. That is for TC-8001's own triage to fix. TC-8006 must not touch TC-8001's versions.

### 4.2.3 Sibling landscape

```
CVE-2026-31812 companion issues:

| Issue      | Stream | Status      | Affects Versions                         |
|------------|--------|-------------|------------------------------------------|
| TC-8001    | 2.2.x  | In Progress | RHTPA 2.2.0, RHTPA 2.2.1                 |
| TC-8006 <- | 2.1.x  | New         | RHTPA 2.1.0 (proposed: + RHTPA 2.1.1)    |
```

## 4.3 – Cross-CVE overlap detection

**Skipped.** The Upstream Affected Component, PS Component, and Stream custom fields are not configured in Security Configuration.

## 4.4 – Preemptive task reconciliation

Simulated search: `project = TC AND issuetype = Task AND labels = 'security-preemptive' AND labels = 'CVE-2026-31812'`, filtered to `(rhtpa-2.1)`. The eval provides no such task, so none was found and the skill continues to Step 5.

## Implications for later steps

- Step 6 (Already Fixed): TC-8001 is In Progress, not Closed/Done, so this is not an already-fixed case.
- Step 8 Case A: stream 2.2.x is also affected, but it already has its own CVE Jira (TC-8001). The skill posts the cross-stream impact comment and creates **no** preemptive tasks for 2.2.x.
- Step 8 Case B: 2.1.x is affected. Cargo means 2 tasks for 2.1.x, each linked to TC-8006 with "Depend".
