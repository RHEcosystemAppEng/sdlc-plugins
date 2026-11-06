# TC-8006 — Step 4: Duplicate, Sibling, Overlap, and Reconciliation Check

## Sibling search (simulated JQL)

```
project = TC AND labels = 'CVE-2026-31812' AND issuetype = 10024 AND key != TC-8006
```

The simulated query returned one result:

| Key | Summary suffix | Status | Affects Versions |
|---|---|---|---|
| TC-8001 | [rhtpa-2.2] | In Progress | RHTPA 2.2.0, RHTPA 2.2.1 |

## Classification

- Current issue TC-8006 is in stream **2.1.x** (`[rhtpa-2.1]`).
- TC-8001 is in stream **2.2.x** (`[rhtpa-2.2]`).
- The suffixes differ, so TC-8001 is a **different-stream sibling**: a companion tracker, not a duplicate.

## Step 4.1 — Same-stream duplicates

No sibling has the `[rhtpa-2.1]` suffix. **No duplicate exists, so TC-8006 is not closed as Duplicate.** TC-8001 is In Progress, but that only matters for same-stream duplicates, so it does not apply here.

## Step 4.2 — Cross-stream coordination for TC-8001

### 4.2.1 Existing-link check (idempotency)

I checked the current issue's `issuelinks` array (already loaded in Step 1) for a link that meets both conditions:

| Condition | Existing link 1990401 | Match? |
|---|---|---|
| `type.name == "Related"` | Related | Yes |
| `inwardIssue.key` or `outwardIssue.key` == TC-8001 | outwardIssue.key = TC-8001 (TC-8006 → TC-8001) | Yes |

**A matching link exists, so link creation is skipped.** Log:

> "Related link to TC-8001 already exists — skipping"

There is no `jira.create_link` call and no new link to confirm with the engineer.

### 4.2.2 Affects Versions overlap check

| Issue | Proposed / current Affects Versions |
|---|---|
| TC-8006 (2.1.x) | RHTPA 2.1.0, RHTPA 2.1.1 (after the Step 3 correction; currently RHTPA 2.1.0) |
| TC-8001 (2.2.x) | RHTPA 2.2.0, RHTPA 2.2.1 |

The two sets do not intersect, so **no version overlap is flagged**. Each issue carries only versions from its own stream.

An informational note, outside TC-8006's scope: the lock-file analysis shows RHTPA 2.2.2 (a backend retag of 2.2.1) is also affected, and TC-8001 does not list it. That is for TC-8001's own triage to fix. Case A's cross-stream impact comment in Step 8 would mention it.

### 4.2.3 Sibling landscape

```
CVE-2026-31812 companion issues:

| Issue     | Stream | Status      | Affects Versions                         |
|-----------|--------|-------------|------------------------------------------|
| TC-8006 ← | 2.1.x  | New         | RHTPA 2.1.0 (proposed: + RHTPA 2.1.1)    |
| TC-8001   | 2.2.x  | In Progress | RHTPA 2.2.0, RHTPA 2.2.1                 |
```

## Step 4.3 — Cross-CVE overlap detection

**Skipped.** The Upstream Affected Component, PS Component, and Stream custom fields are not configured in Security Configuration.

## Step 4.4 — Preemptive task reconciliation

The skill would run this query:

```
project = TC AND issuetype = Task AND labels = 'security-preemptive' AND labels = 'CVE-2026-31812' ORDER BY created DESC
```

and then filter for `(rhtpa-2.1)` in the summary. The eval scenario provides no preemptive-task results, so I treated it as **no matching preemptive task**. Nothing was linked or relabeled, and the skill proceeds to Step 5.

## Step 6 preview — Already fixed

The only sibling, TC-8001, is In Progress and not Closed/Done, so no resolved sibling covers 2.1.x. The issue is not already fixed.
