# Step 4 – Duplicate, Sibling, and Overlap Check: TC-8006

## Sibling search (simulated JQL)

```
project = TC AND labels = 'CVE-2026-31812' AND issuetype = 10024 AND key != TC-8006
```

Simulated result: 1 issue.

| Issue | Summary suffix | Stream | Status | Affects Versions |
|---|---|---|---|---|
| TC-8001 | `[rhtpa-2.2]` | 2.2.x | In Progress | RHTPA 2.2.0, RHTPA 2.2.1 |

## Classification

- Current issue TC-8006 suffix: `[rhtpa-2.1]`, stream 2.1.x.
- TC-8001 suffix: `[rhtpa-2.2]`, stream 2.2.x. The streams differ, so TC-8001 is a **different-stream sibling (companion tracker)** and not a duplicate.
- Same-stream siblings: **none**.

## 4.1 – Same-stream duplicates

No same-stream sibling exists, so there is **no duplicate closure**. TC-8006 stays open for its own triage.

## 4.2 – Cross-stream coordination (TC-8001)

### 4.2.1 – Check for an existing link before creating one

TC-8006's `issuelinks` array (from the Step 1 `get_issue` response) has one entry:

| Link ID | type.name | Direction | Linked issue |
|---|---|---|---|
| 1990401 | Related | outward (TC-8006 → TC-8001) | TC-8001 |

Match evaluation:
- `type.name == "Related"`: yes.
- `outwardIssue.key == TC-8001` (the sibling key): yes. The direction does not matter, because the rule accepts either `inwardIssue.key` or `outwardIssue.key`.

**Result: a matching link exists, so link creation is skipped.**

Log:
> "Related link to TC-8001 already exists — skipping"

No `jira.create_link` call is issued, so this step makes no Jira mutation and needs no confirmation prompt.

### 4.2.2 – Affects Versions overlap check

| Issue | Stream | Affects Versions (after Step 3 proposal) |
|---|---|---|
| TC-8006 | 2.1.x | RHTPA 2.1.0, RHTPA 2.1.1 |
| TC-8001 | 2.2.x | RHTPA 2.2.0, RHTPA 2.2.1 |

The intersection is empty: **no version overlap**, so no overlap flag is raised.

Observation for the engineer (informational only; this skill does not edit TC-8001): lock file analysis shows RHTPA 2.2.2 is also affected because it is a backend retag of 2.2.1 (quinn-proto 0.11.12). TC-8001 does not list it. Its own triage should consider adding it.

### 4.2.3 – Sibling landscape

```
CVE-2026-31812 companion issues:

| Issue     | Stream | Status      | Affects Versions                  |
|-----------|--------|-------------|-----------------------------------|
| TC-8006 ← | 2.1.x  | New         | RHTPA 2.1.0 (proposed: + RHTPA 2.1.1) |
| TC-8001   | 2.2.x  | In Progress | RHTPA 2.2.0, RHTPA 2.2.1          |
```

## 4.3 – Cross-CVE overlap detection

**Skipped.** The Upstream Affected Component, PS Component, and Stream custom fields are not configured in Security Configuration.

## 4.4 – Preemptive task reconciliation

Simulated search: `project = TC AND issuetype = Task AND labels = 'security-preemptive' AND labels = 'CVE-2026-31812'`. The eval supplied no preemptive tasks, so nothing matched for `rhtpa-2.1`. The step proceeds silently, and Step 8 still creates tasks for 2.1.x.

## Impact on later steps

- Case A (cross-stream): the 2.2.x stream is affected (2.2.0, 2.2.1, 2.2.2), but it already has its own CVE Jira (TC-8001). So **no preemptive tasks** are created for 2.2.x. Only the cross-stream impact comment is posted, and it refers to the existing Related link.
- Case B: 2 Cargo remediation tasks for stream 2.1.x (upstream backport or dependency bump on `release/0.3.z`, plus downstream propagation to rhtpa-release.0.3.z), each linked to TC-8006 with "Depend".
