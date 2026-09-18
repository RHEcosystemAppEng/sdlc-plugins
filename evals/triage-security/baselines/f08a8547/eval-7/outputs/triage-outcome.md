# Triage Outcome -- TC-8006

## How Step 4.2 Handled the Pre-Existing Link

TC-8006 arrived with a pre-existing "Related" link to sibling issue TC-8001 (link ID 1990401, outward direction: TC-8006 -> TC-8001). This is the key scenario this eval tests: **idempotent link handling when a Related link already exists**.

### Step 4.2 Procedure

1. **JQL search** returned TC-8001 as a sibling with stream suffix `[rhtpa-2.2]` (different from TC-8006's `[rhtpa-2.1]`), classifying it as a cross-stream companion, not a same-stream duplicate.

2. **Link idempotency check**: Before creating a link, Step 4.2 inspects the current issue's `issuelinks` array (already fetched in Step 1) to see if any existing link satisfies ALL of:
   - `type.name` is `"Related"`
   - `inwardIssue.key` or `outwardIssue.key` matches the sibling key

3. **Match found**: TC-8006's issue links include a Related link where `outwardIssue.key` = TC-8001. This satisfies both conditions.

4. **Result**: Link creation was **skipped** with the log message:
   > "Related link to TC-8001 already exists -- skipping"

5. **No duplicate link created**: The skill did not call `jira.create_link()` because the idempotency check detected the pre-existing link. This prevents duplicate Related links between the same pair of issues.

### Why This Matters

Without the idempotency check, re-running triage (or triaging an issue that PSIRT pre-linked) would create duplicate Related links between the same issues. Step 4.2's check-before-create pattern ensures that:
- Pre-existing links (created by PSIRT, by a prior triage, or manually) are respected
- The skill is safe to re-run without side effects on issue linkage
- Both inward and outward link directions are checked (the link could point in either direction)

## Overall Triage Summary

### Issue Context

- **Issue**: TC-8006 -- CVE-2026-31812 quinn-proto - Panic on large stream counts [rhtpa-2.1]
- **Stream scope**: 2.1.x (scoped issue)
- **CVE**: CVE-2026-31812
- **Library**: quinn-proto (Cargo ecosystem)
- **Fix threshold**: 0.11.14
- **CVSS**: 7.5 (High)

### Version Impact (Stream 2.1.x)

| Version | quinn-proto | Affected? |
|---------|-------------|-----------|
| 2.1.0 | 0.11.9 | YES |
| 2.1.1 | 0.11.9 | YES |

All versions in the 2.1.x stream are affected -- both ship quinn-proto 0.11.9, which is below the fix threshold of 0.11.14.

### Cross-Stream Impact (Case A)

The version impact analysis also shows that the 2.2.x stream is partially affected (versions 2.2.0 through 2.2.2). However, sibling TC-8001 already exists for stream 2.2.x and is In Progress, so no preemptive remediation tasks are needed for that stream. The cross-stream impact comment would note:

> Cross-stream impact: quinn-proto < 0.11.14 also affects stream 2.2.x based on lock file analysis. This stream is tracked by companion issue TC-8001 (see Related link).

### Sibling Coordination

| Issue | Stream | Status | Affects Versions | Link |
|-------|--------|--------|------------------|------|
| TC-8001 | 2.2.x | In Progress | RHTPA 2.2.0, RHTPA 2.2.1 | Related (pre-existing) |
| TC-8006 (current) | 2.1.x | New | RHTPA 2.1.0 | -- |

No Affects Versions overlap between the two issues. No same-stream duplicates found.

### Triage Decision: Case B (Affected -- create remediation tasks)

Since both versions in stream 2.1.x are affected, the triage outcome is **Case B**: create remediation tasks for the 2.1.x stream.

Because quinn-proto is a Cargo (source dependency) ecosystem, **two tasks** would be created per the ecosystem classification table:

1. **Upstream backport task**: Bump quinn-proto to >= 0.11.14 on branch `release/0.3.z` in the backend source repository
2. **Downstream propagation task**: Update the backend source reference in rhtpa-release.0.3.z (Konflux release repo) to pick up the upstream fix. Blocked by the upstream task.

Both tasks would be linked to TC-8006 with "Depend" link type, and the downstream task would be blocked by the upstream task via "Blocks" link type.

### Affects Versions Correction (Step 3)

PSIRT assigned: RHTPA 2.1.0
Version impact shows: RHTPA 2.1.0 (YES), RHTPA 2.1.1 (YES)

Proposed correction (scoped to stream 2.1.x):
- Current: [RHTPA 2.1.0]
- Proposed: [RHTPA 2.1.0, RHTPA 2.1.1]

RHTPA 2.1.1 should be added because the version impact analysis confirms it also ships vulnerable quinn-proto 0.11.9.
