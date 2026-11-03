# Step 4 – Duplicate, Sibling, Overlap, and Reconciliation Check: TC-8006

## Sibling JQL (simulated, not executed)

```
project = TC AND labels = 'CVE-2026-31812' AND issuetype = 10024 AND key != TC-8006
```

Simulated result: **1 issue**

| Key | Summary suffix | Stream | Status | Affects Versions |
|---|---|---|---|---|
| TC-8001 | [rhtpa-2.2] | 2.2.x | In Progress | RHTPA 2.2.0, RHTPA 2.2.1 |

## Classification

- Current issue TC-8006 has suffix `[rhtpa-2.1]`, which maps to stream 2.1.x.
- TC-8001 has suffix `[rhtpa-2.2]`, which maps to stream 2.2.x. That is a **different stream**.

| Category | Issues |
|---|---|
| Same-stream siblings | none |
| Different-stream siblings (companion trackers) | TC-8001 |

## 4.1 – Same-stream duplicates

There are no same-stream siblings. TC-8006 is **not** a duplicate and should not be closed as Duplicate. TC-8001 being In Progress does not matter for duplicate detection because it tracks another stream.

## 4.2 – Cross-stream coordination (TC-8001)

### 4.2.1 – Existing-link check (idempotent linking)

I checked the `issuelinks` array on TC-8006, which was already fetched in Step 1:

| Link ID | type.name | Direction | Linked key | Matches? |
|---|---|---|---|---|
| 1990401 | Related | outward (TC-8006 → TC-8001), so `outwardIssue.key` = TC-8001 | TC-8001 | YES |

Both conditions hold: `type.name == "Related"` and `outwardIssue.key == TC-8001`. **Link creation is skipped.**

> "Related link to TC-8001 already exists — skipping"

No `jira.create_link` call is proposed, so no duplicate Related link is created.

### 4.2.2 – Affects Versions overlap check

| Issue | Affects Versions (after the Step 3 proposal) |
|---|---|
| TC-8006 (2.1.x) | RHTPA 2.1.0, RHTPA 2.1.1 |
| TC-8001 (2.2.x) | RHTPA 2.2.0, RHTPA 2.2.1 |

The two sets do not intersect, so there is **no overlap** and no flag is raised.

Informational only: lock-file analysis shows RHTPA 2.2.2 is affected too, because it is a retag of 2.2.1 with quinn-proto 0.11.12. TC-8001 does not list it. That belongs to TC-8001's own triage and TC-8006 does not change it.

### 4.2.3 – Sibling landscape

```
CVE-2026-31812 companion issues:

| Issue     | Stream | Status      | Affects Versions               |
|-----------|--------|-------------|--------------------------------|
| TC-8006 ← | 2.1.x  | New         | RHTPA 2.1.0 (→ + RHTPA 2.1.1)  |
| TC-8001   | 2.2.x  | In Progress | RHTPA 2.2.0, RHTPA 2.2.1       |
```

## 4.3 – Cross-CVE overlap detection

**Skipped.** The Upstream Affected Component, PS Component, and Stream custom fields are not configured in Security Configuration.

## 4.4 – Preemptive task reconciliation

Simulated JQL: `project = TC AND issuetype = Task AND labels = 'security-preemptive' AND labels = 'CVE-2026-31812' ORDER BY created DESC`. The eval scenario provides no preemptive tasks, so nothing matches `(rhtpa-2.1)`. Proceed to Step 5 with no reconciliation.

## Effect on later steps

- Step 6 (Already Fixed): TC-8001 is In Progress, not resolved, so it gives no already-fixed signal.
- Step 8 Case A: TC-8006 is scoped. The other affected stream (2.2.x) already has its own CVE Jira, TC-8001, so no preemptive tasks are created for 2.2.x. A cross-stream impact comment pointing at the Related link is still appropriate.
- Step 8 Case B: create 2 Cargo remediation tasks for 2.1.x only, linked to TC-8006 with "Depend".
