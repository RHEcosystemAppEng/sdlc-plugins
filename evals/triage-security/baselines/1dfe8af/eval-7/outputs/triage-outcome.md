# Triage Outcome -- Step 4.2 Pre-Existing Link Handling

## Summary

TC-8006 (CVE-2026-31812 quinn-proto [rhtpa-2.1]) has a sibling issue TC-8001 tracking the same CVE for stream [rhtpa-2.2]. Step 4.2 requires creating a "Related" link between companion cross-stream issues, but the link must be checked for existence first to ensure idempotency.

## How Step 4.2 Handled the Pre-Existing Link

### 1. Sibling Detection

The JQL search for sibling issues with the same CVE label (`CVE-2026-31812`) returned one result:
- **TC-8001** -- status `In Progress`, stream `[rhtpa-2.2]`, Affects Versions `[RHTPA 2.2.0, RHTPA 2.2.1]`

TC-8001 was classified as a **different-stream companion** (stream `[rhtpa-2.2]` differs from TC-8006's stream `[rhtpa-2.1]`). It is NOT a same-stream duplicate.

### 2. Link Existence Check (Idempotent Guard)

Before attempting to create a Related link, Step 4.2 requires inspecting the current issue's `issuelinks` array (already fetched in Step 1) for any link that satisfies all of:
- `type.name` is `"Related"`
- `inwardIssue.key` or `outwardIssue.key` matches the sibling key (`TC-8001`)

**Check result**: TC-8006's existing issue links include:
- Link ID `1990401`, type `Related`, direction `outward`, linked issue `TC-8001`

This link satisfies both conditions. The `type.name` is `"Related"` and the `outwardIssue.key` is `TC-8001`.

### 3. Link Creation Skipped

Because a matching Related link already exists, **link creation was skipped**. The log message:

> Related link to TC-8001 already exists -- skipping

No `jira.create_link` call was made. This prevents duplicate link creation and ensures the triage operation is idempotent -- running triage again on this issue will not create redundant links.

### 4. Sibling Landscape Still Presented

Despite the link already existing, the sibling landscape table was still presented to the engineer for situational awareness:

| Issue | Stream | Status | Affects Versions |
|-------|--------|--------|------------------|
| TC-8001 | 2.2.x | In Progress | RHTPA 2.2.0, RHTPA 2.2.1 |
| TC-8006 (current) | 2.1.x | New | RHTPA 2.1.0 |

This table provides the engineer with a complete view of all companion issues tracking CVE-2026-31812 across streams, regardless of whether links needed to be created or already existed.

### 5. Affects Versions Overlap Check

The overlap check was still performed:
- TC-8006 owns RHTPA 2.1.0 (2.1.x stream)
- TC-8001 owns RHTPA 2.2.0, RHTPA 2.2.1 (2.2.x stream)
- No overlap -- each issue carries only versions from its own stream.

## Key Behavioral Properties Demonstrated

1. **Idempotency**: The skill checks for existing links before creating them, so re-running triage does not create duplicate Related links.
2. **Correct classification**: TC-8001 was classified as a different-stream companion (not a same-stream duplicate), because its stream suffix `[rhtpa-2.2]` differs from TC-8006's `[rhtpa-2.1]`.
3. **Full presentation**: The sibling landscape table is always presented regardless of whether link creation was needed, ensuring the engineer has complete cross-stream context.
4. **Log transparency**: A clear log message indicates why link creation was skipped, providing an audit trail.
