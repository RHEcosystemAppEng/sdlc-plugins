# Step 4 — Duplicate, Sibling, and Overlap Check

## 4.0 — Sibling Search

JQL query executed (simulated):
```
project = TC AND labels = 'CVE-2026-31812' AND issuetype = 10024 AND key != TC-8006
```

**Results**: 1 sibling found.

| Issue | Summary | Stream Suffix | Status | Affects Versions |
|-------|---------|---------------|--------|------------------|
| TC-8001 | CVE-2026-31812 quinn-proto - Panic on large stream counts [rhtpa-2.2] | [rhtpa-2.2] | In Progress | RHTPA 2.2.0, RHTPA 2.2.1 |

## 4.1 — Same-stream Duplicate Check

TC-8001 has stream suffix **[rhtpa-2.2]**. The current issue TC-8006 has stream suffix **[rhtpa-2.1]**.

**Classification**: TC-8001 is a **different-stream companion** (stream rhtpa-2.2 vs current issue's rhtpa-2.1). This is NOT a same-stream duplicate.

PSIRT creates one Vulnerability issue per stream intentionally. Different-stream siblings are companion trackers, not duplicates.

## 4.2 — Cross-stream Coordination

### Link Idempotency Check

Before creating a "Related" link to TC-8001, check the current issue's existing `issuelinks` array (already fetched in Step 1).

**Existing links on TC-8006:**
- Link ID 1990401: Type = "Related", Direction = outward, Target = TC-8001

**Check result**: An existing link satisfies ALL conditions:
- `type.name` is `"Related"` ✓
- `outwardIssue.key` matches TC-8001 ✓

**Decision**: Related link to TC-8001 already exists — skipping link creation.

> Related link to TC-8001 already exists — skipping

The `jira.create_link()` call is NOT executed because the link already exists. This idempotent check prevents duplicate links.

### Sibling Landscape

The sibling landscape table is still presented to the engineer despite the link already existing — the idempotent check only affects link creation, not the sibling summary.

```
CVE-2026-31812 companion issues:

| Issue     | Stream | Status      | Affects Versions               |
|-----------|--------|-------------|--------------------------------|
| TC-8001   | 2.2.x  | In Progress | RHTPA 2.2.0, RHTPA 2.2.1      |
| TC-8006 ← | 2.1.x  | New         | RHTPA 2.1.0                    |
```

**Notes:**
- TC-8001 is already In Progress on stream 2.2.x — active triage is underway for that stream.
- TC-8006 (current issue) covers stream 2.1.x.
- The existing Related link between TC-8006 and TC-8001 provides cross-stream traceability.

### Affects Versions Overlap Check

No version overlap detected:
- TC-8006 claims: RHTPA 2.1.0 (stream 2.1.x)
- TC-8001 claims: RHTPA 2.2.0, RHTPA 2.2.1 (stream 2.2.x)

Each issue carries versions only from its own stream. No correction needed.
