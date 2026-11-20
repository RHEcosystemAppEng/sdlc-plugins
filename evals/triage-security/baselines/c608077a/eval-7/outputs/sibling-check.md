# Step 4 – Duplicate, Sibling, Overlap, and Reconciliation Check: TC-8006

## Sibling search (simulated)

JQL that would run:

```
project = TC AND labels = 'CVE-2026-31812' AND issuetype = 10024 AND key != TC-8006
```

Simulated result: 1 issue.

| Key | Summary suffix | Stream | Status | Affects Versions |
|---|---|---|---|---|
| TC-8001 | [rhtpa-2.2] | 2.2.x | In Progress | RHTPA 2.2.0, RHTPA 2.2.1 |

## Classification

- TC-8006 suffix `[rhtpa-2.1]` → stream **2.1.x**
- TC-8001 suffix `[rhtpa-2.2]` → stream **2.2.x**
- The streams differ, so TC-8001 is a **different-stream sibling (companion tracker)**, not a duplicate.

### 4.1 – Same-stream duplicates

There are no same-stream siblings, so TC-8006 is **not** closed as Duplicate.

### 4.2 – Cross-stream coordination for TC-8001

**4.2.1 – Check for an existing link (idempotency check).** The skill reads TC-8006's `issuelinks` from the Step 1 `get_issue` response and checks each entry for:

| Criterion | Existing link 1990401 | Match? |
|---|---|---|
| `type.name == "Related"` | Related | Yes |
| `inwardIssue.key` or `outwardIssue.key == TC-8001` | outwardIssue.key = TC-8001 (TC-8006 → TC-8001) | Yes |

Result: a matching link exists, so **link creation is skipped**. Log:

> "Related link to TC-8001 already exists — skipping"

No `jira.create_link(...)` call is proposed. The link direction (outward rather than the inward/outward order the skill would use when creating one) does not matter, because the check accepts either endpoint.

**4.2.2 – Affects Versions overlap check:**

| Issue | Affects Versions (after Step 3 proposal) |
|---|---|
| TC-8006 (2.1.x) | RHTPA 2.1.0, RHTPA 2.1.1 |
| TC-8001 (2.2.x) | RHTPA 2.2.0, RHTPA 2.2.1 |

The two sets do not intersect, so there is **no version overlap** and no flag to the engineer. Each issue carries only its own stream's versions.

Informational, outside TC-8006's scope: lock-file analysis shows RHTPA 2.2.2 (a backend retag of 2.2.1) is also affected, and TC-8001 does not list it. That correction belongs to TC-8001's own triage. It is mentioned in the cross-stream comment (Case A) and not edited from this issue.

**4.2.3 – Sibling landscape:**

```
CVE-2026-31812 companion issues:

| Issue     | Stream | Status      | Affects Versions                   |
|-----------|--------|-------------|------------------------------------|
| TC-8001   | 2.2.x  | In Progress | RHTPA 2.2.0, RHTPA 2.2.1           |
| TC-8006 ← | 2.1.x  | New         | RHTPA 2.1.0 (proposed: + RHTPA 2.1.1) |
```

### 4.3 – Cross-CVE overlap detection

**Skipped.** The Upstream Affected Component, PS Component, and Stream custom fields are not configured in Security Configuration.

### 4.4 – Preemptive task reconciliation

The JQL that would run:

```
project = TC AND issuetype = Task AND labels = 'security-preemptive' AND labels = 'CVE-2026-31812' ORDER BY created DESC
```

No preemptive-task data was provided for this eval, so we assume no task with `(rhtpa-2.1)` in its summary exists. The skill proceeds silently to Step 5. If live data returns a match, the skill would add a Depend link and remove the `security-preemptive` label.

## Step 4 Jira mutations

| Proposed mutation | Status |
|---|---|
| Related link TC-8006 ↔ TC-8001 | **Not created.** Already exists (link ID 1990401) |
| Close as Duplicate | Not applicable (different streams) |
| Version overlap comment | Not applicable (no overlap) |

Step 4 makes **no Jira writes**.
