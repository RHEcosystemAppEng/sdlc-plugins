# Step 4 – Duplicate, Sibling, Overlap, and Reconciliation Check: TC-8006

## Sibling Search (simulated JQL)

```
project = TC AND labels = 'CVE-2026-31812' AND issuetype = 10024 AND key != TC-8006
```

Assumed result: 1 issue.

| Issue | Summary suffix | Stream | Status | Affects Versions |
|---|---|---|---|---|
| TC-8001 | [rhtpa-2.2] | 2.2.x | In Progress | RHTPA 2.2.0, RHTPA 2.2.1 |

## Classification

- Current issue TC-8006 has suffix [rhtpa-2.1], which is stream **2.1.x**.
- TC-8001 has suffix [rhtpa-2.2], which is stream **2.2.x**, so it is a **different-stream sibling** (companion tracker).
- Same-stream siblings: **none**.

## Step 4.1 – Same-stream duplicates

There is no same-stream sibling, so there is **no duplicate**. TC-8006 is not closed as Duplicate, and no Duplicate comment, transition, or closure is proposed.

## Step 4.2 – Cross-stream coordination (TC-8001)

### 4.2.1 – Existing link check (idempotent linking)

I checked the `issuelinks` array that Step 1 had already fetched for TC-8006:

| Link ID | type.name | Direction | Linked key |
|---|---|---|---|
| 1990401 | Related | outward (TC-8006 → TC-8001) | TC-8001 |

Match criteria:
- `type.name == "Related"`: yes
- `outwardIssue.key == "TC-8001"`: yes

**Result: a matching link already exists.** Link creation is skipped.

> "Related link to TC-8001 already exists — skipping"

No `jira.create_link` call is made and no link mutation is proposed to the engineer. Link direction does not matter for the check, because either `inwardIssue` or `outwardIssue` may match.

### 4.2.2 – Affects Versions overlap check

| Issue | Stream | Affects Versions (after Step 3 proposal) |
|---|---|---|
| TC-8006 | 2.1.x | RHTPA 2.1.0, RHTPA 2.1.1 (current: RHTPA 2.1.0) |
| TC-8001 | 2.2.x | RHTPA 2.2.0, RHTPA 2.2.1 |

The intersection is empty, so **no version overlap** exists and nothing needs to be flagged. Each issue carries only versions from its own stream.

Informational note (outside TC-8006's scope, no action taken here): the lock-file analysis shows that RHTPA 2.2.2 (a backend retag of 2.2.1, quinn-proto 0.11.12) is also affected but is not listed on TC-8001. That should be handled when TC-8001 is triaged.

### 4.2.3 – Sibling landscape

```
CVE-2026-31812 companion issues:

| Issue     | Stream | Status      | Affects Versions                 |
|-----------|--------|-------------|----------------------------------|
| TC-8006 ← | 2.1.x  | New         | RHTPA 2.1.0 (proposed: + RHTPA 2.1.1) |
| TC-8001   | 2.2.x  | In Progress | RHTPA 2.2.0, RHTPA 2.2.1         |
```

## Step 4.3 – Cross-CVE overlap detection

**Skipped.** The Upstream Affected Component, PS Component, and Stream custom fields are not configured in Security Configuration.

## Step 4.4 – Preemptive task reconciliation

Simulated query:
```
project = TC AND issuetype = Task AND labels = 'security-preemptive' AND labels = 'CVE-2026-31812' ORDER BY created DESC
```
No preemptive task data was provided for this eval, so I assume no result matches `(rhtpa-2.1)` and proceed silently to Step 5. Nothing is reconciled, and Step 8 still creates remediation for 2.1.x.

## Step 4 Summary

| Check | Result | Jira mutation |
|---|---|---|
| 4.1 Same-stream duplicate | None | None |
| 4.2 Related link to TC-8001 | Already exists (ID 1990401), skipped | **None** |
| 4.2 Affects Versions overlap | None | None |
| 4.3 Cross-CVE overlap | Skipped (fields not configured) | None |
| 4.4 Preemptive reconciliation | No match (assumed) | None |
