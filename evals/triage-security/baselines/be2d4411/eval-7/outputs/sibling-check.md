# Step 4 -- Duplicate, Sibling, and Overlap Check for TC-8006

## 4.0 -- JQL Sibling Search

Search query:
```
project = TC AND labels = 'CVE-2026-31812' AND issuetype = 10024 AND key != TC-8006
```

Results: **1 sibling found**

| Issue | Summary | Status | Labels | Affects Versions |
|-------|---------|--------|--------|------------------|
| TC-8001 | CVE-2026-31812 quinn-proto - Panic on large stream counts [rhtpa-2.2] | In Progress | CVE-2026-31812, pscomponent:org/rhtpa-server | RHTPA 2.2.0, RHTPA 2.2.1 |

## 4.1 -- Same-Stream Duplicate Check

- Current issue TC-8006 stream suffix: `[rhtpa-2.1]` (stream 2.1.x)
- Sibling TC-8001 stream suffix: `[rhtpa-2.2]` (stream 2.2.x)

**Classification: Different-stream companion** -- TC-8001 tracks a different version stream (2.2.x) than the current issue (2.1.x). This is NOT a same-stream duplicate. PSIRT creates one Vulnerability issue per stream intentionally.

No same-stream duplicates found. Proceeding to Step 4.2.

## 4.2 -- Cross-Stream Coordination

TC-8001 is a **different-stream sibling** (companion tracker) for the same CVE.

### Link existence check (idempotent)

Per Step 4.2 of the triage procedure, before creating a Related link, the skill checks the current issue's `issuelinks` array (already fetched in Step 1) for any existing link satisfying all of:
- `type.name` is `"Related"`
- `inwardIssue.key` or `outwardIssue.key` matches TC-8001

**Existing issuelinks on TC-8006:**
- Link ID 1990401: type = "Related", direction = outward, outwardIssue.key = **TC-8001**

**Result:** A Related link to TC-8001 already exists (Link ID 1990401, outward direction).

> "Related link to TC-8001 already exists -- skipping"

Link creation is **SKIPPED**. The pre-existing Related link satisfies the idempotency requirement. No duplicate link will be created.

### Affects Versions overlap check

- TC-8006 Affects Versions: RHTPA 2.1.0
- TC-8001 Affects Versions: RHTPA 2.2.0, RHTPA 2.2.1

No overlap detected -- each issue carries versions exclusively from its own stream (2.1.x vs 2.2.x).

### Sibling Landscape

Despite the link already existing, the sibling landscape table is still presented to the engineer for situational awareness:

```
CVE-2026-31812 companion issues:

| Issue      | Stream | Status      | Affects Versions              |
|------------|--------|-------------|-------------------------------|
| TC-8006 <- | 2.1.x  | New         | RHTPA 2.1.0                   |
| TC-8001    | 2.2.x  | In Progress | RHTPA 2.2.0, RHTPA 2.2.1     |
```

The arrow (`<-`) marks the current issue being triaged.

## 4.3 -- Cross-CVE Overlap Detection

The Upstream Affected Component custom field is not configured in the project's Security Configuration. Step 4.3 is **skipped entirely** per the prerequisite check.

## 4.4 -- Preemptive Task Reconciliation

No preemptive tasks found matching CVE-2026-31812 and stream 2.1.x. Proceeding to Step 5.
