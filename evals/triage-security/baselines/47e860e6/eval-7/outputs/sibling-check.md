# Step 4 – Duplicate, Sibling, Overlap, and Reconciliation Check: TC-8006

## Sibling search

JQL (simulated, not executed):

```
project = TC AND labels = 'CVE-2026-31812' AND issuetype = 10024 AND key != TC-8006
```

Result (as given by the eval): 1 issue.

| Key | Summary suffix | Stream | Status | Affects Versions |
|-----|----------------|--------|--------|------------------|
| TC-8001 | [rhtpa-2.2] | 2.2.x | In Progress | RHTPA 2.2.0, RHTPA 2.2.1 |

## Classification

- Current issue TC-8006 stream: 2.1.x (`[rhtpa-2.1]`).
- TC-8001 stream: 2.2.x (`[rhtpa-2.2]`) -> **different-stream sibling (companion tracker)**, not a duplicate.
- Same-stream siblings: **none** -> Step 4.1 (close as Duplicate) does **not** apply. TC-8006 stays open.

## 4.2 – Cross-stream coordination for TC-8001

### 1. Existing-link check (idempotency)

Inspected TC-8006 `issuelinks` (from the Step 1 issue fetch):

| Link ID | type.name | Direction | Linked issue |
|---------|-----------|-----------|--------------|
| 1990401 | Related | outward (TC-8006 -> TC-8001) | TC-8001 |

Match criteria: `type.name == "Related"` AND (`inwardIssue.key` or `outwardIssue.key`) == `TC-8001` -> **both satisfied** (outwardIssue.key = TC-8001).

Log:
> "Related link to TC-8001 already exists — skipping"

**No `jira.create_link` call is made.** No duplicate Related link is created.

### 2. Affects Versions overlap check

- TC-8006 (2.1.x): current [RHTPA 2.1.0]; proposed after Step 3 [RHTPA 2.1.0, RHTPA 2.1.1]
- TC-8001 (2.2.x): [RHTPA 2.2.0, RHTPA 2.2.1]
- Intersection: **empty** -> no version overlap; no overlap warning raised. Each issue carries only its own stream's versions.

Informational (not a TC-8006 action): version impact data shows RHTPA 2.2.2 (backend retag of v0.4.8, quinn-proto 0.11.12) is also affected but is not on TC-8001's Affects Versions. That correction belongs to TC-8001's own triage.

### 3. Sibling landscape

```
CVE-2026-31812 companion issues:

| Issue     | Stream | Status      | Affects Versions                         |
|-----------|--------|-------------|------------------------------------------|
| TC-8001   | 2.2.x  | In Progress | RHTPA 2.2.0, RHTPA 2.2.1                 |
| TC-8006 ← | 2.1.x  | New         | RHTPA 2.1.0 (proposed: + RHTPA 2.1.1)    |
```

## 4.3 – Cross-CVE overlap detection

Skipped: Upstream Affected Component custom field is not configured in Security Configuration.

## 4.4 – Preemptive task reconciliation

Simulated search: `project = TC AND issuetype = Task AND labels = 'security-preemptive' AND labels = 'CVE-2026-31812'` filtered by `(rhtpa-2.1)`. No preemptive tasks were provided in the eval inputs -> treated as none found; proceed silently to Step 5. Step 8 would create remediation tasks for 2.1.x normally.

## Step 6 note

TC-8001 is In Progress (not resolved) -> it does not indicate an already-fixed scenario for TC-8006.
