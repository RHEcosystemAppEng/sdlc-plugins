# Step 4 – Duplicate, Sibling, and Overlap Check: TC-8006

## Sibling search (simulated)

```
jira.search_jql(
  "project = TC AND labels = 'CVE-2026-31812' AND issuetype = 10024 AND key != TC-8006"
)
```

Simulated result (1 issue):

| Key | Summary suffix | Stream | Status | Affects Versions |
|-----|----------------|--------|--------|------------------|
| TC-8001 | `[rhtpa-2.2]` | 2.2.x | In Progress | RHTPA 2.2.0, RHTPA 2.2.1 |

## Classification

- The current issue TC-8006 is in stream **2.1.x** (`[rhtpa-2.1]`).
- TC-8001 is in stream **2.2.x** (`[rhtpa-2.2]`), so it is a **different-stream sibling**: a
  companion tracker, not a duplicate.
- Same-stream siblings: **none**.

### 4.1 – Same-stream duplicates

No same-stream sibling was found, so there is no Duplicate closure recommendation. TC-8006 stays open for
triage.

### 4.2 – Cross-stream coordination (TC-8001)

1. **Existing link check.** I read the `issuelinks` array that Step 1 already fetched for
   TC-8006:

   | Link ID | type.name | inwardIssue.key | outwardIssue.key |
   |---------|-----------|-----------------|------------------|
   | 1990401 | Related | (none: this issue is the source) | TC-8001 |

   Match criteria:
   - `type.name == "Related"`: yes
   - `inwardIssue.key` or `outwardIssue.key == TC-8001`: yes (`outwardIssue.key`)

   Result: **a matching link exists, so link creation is skipped.**

   > "Related link to TC-8001 already exists — skipping"

   `jira.create_link(inwardIssue: TC-8006, outwardIssue: TC-8001, type: "Related")` is
   **not** called, so no duplicate Related link is created.

2. **Affects Versions overlap check**
   - TC-8006 (2.1.x): current [RHTPA 2.1.0]. After the proposed Step 3 correction: [RHTPA 2.1.0,
     RHTPA 2.1.1].
   - TC-8001 (2.2.x): [RHTPA 2.2.0, RHTPA 2.2.1].
   - Intersection: **none**. Each issue carries only its own stream's versions, so there
     is no overlap to flag.
   - Informational: the simulated lock-file data also shows RHTPA 2.2.2 (a backend retag of
     v0.4.8, quinn-proto 0.11.12) as affected. TC-8001 does not list it. That correction
     belongs to TC-8001's own triage, not to TC-8006, so nothing is changed on it here.

3. **Sibling landscape**

   ```
   CVE-2026-31812 companion issues:

   | Issue     | Stream | Status      | Affects Versions                         |
   |-----------|--------|-------------|------------------------------------------|
   | TC-8006 ← | 2.1.x  | New         | RHTPA 2.1.0 (proposed: + RHTPA 2.1.1)    |
   | TC-8001   | 2.2.x  | In Progress | RHTPA 2.2.0, RHTPA 2.2.1                 |
   ```

### 4.3 – Cross-CVE overlap detection

**Skipped.** The Upstream Affected Component, PS Component and Stream custom fields are not
configured in Security Configuration.

### 4.4 – Preemptive task reconciliation (simulated)

Query: `project = TC AND issuetype = Task AND labels = 'security-preemptive' AND labels = 'CVE-2026-31812'`.
The scenario provides no preemptive task, so no `(rhtpa-2.1)` task matches. Triage proceeds
to Step 5 without reconciliation.

## Jira mutations from Step 4

| Proposed operation | Executed? | Reason |
|--------------------|-----------|--------|
| Create Related link TC-8006 ↔ TC-8001 | **No (skipped)** | Link 1990401 (Related, TC-8006 → TC-8001) already exists |
| Close TC-8006 as Duplicate | No | Sibling is in a different stream, so it is not a duplicate |
| Version overlap flag | No | No overlapping Affects Versions |
