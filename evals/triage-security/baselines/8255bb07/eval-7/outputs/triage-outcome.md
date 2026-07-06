# Triage Outcome -- Step 4.2 Pre-Existing Link Handling

## Summary

Step 4.2 (Cross-stream coordination) correctly detected and handled a pre-existing "Related" link between TC-8006 and its sibling TC-8001. Link creation was skipped because the link already existed, demonstrating the idempotent linking behavior required by the skill procedure.

## Detailed Analysis

### Context

- **Current issue**: TC-8006 -- CVE-2026-31812 quinn-proto - Panic on large stream counts [rhtpa-2.1]
- **Sibling issue**: TC-8001 -- CVE-2026-31812 quinn-proto - Panic on large stream counts [rhtpa-2.2]
- **Pre-existing link**: Related link (ID 1990401), outward direction from TC-8006 to TC-8001

### How Step 4.2 Handled the Pre-Existing Link

1. **JQL search** returned TC-8001 as a sibling (same CVE label CVE-2026-31812, different issue key).

2. **Stream classification**: TC-8001 has suffix `[rhtpa-2.2]` which differs from TC-8006's suffix `[rhtpa-2.1]`. TC-8001 is classified as a **different-stream sibling** (companion tracker), not a same-stream duplicate.

3. **Existing link check** (the critical idempotency step): Before attempting to create a "Related" link, Step 4.2 reads the current issue's `issuelinks` array from the `jira.get_issue` response already fetched in Step 1. The procedure checks whether any existing link satisfies ALL of:
   - `type.name` is `"Related"` -- **YES** (link 1990401 type is "Related")
   - `inwardIssue.key` or `outwardIssue.key` matches the sibling key -- **YES** (`outwardIssue.key` = "TC-8001")

4. **Decision**: A matching link exists. Step 4.2 logs:
   > "Related link to TC-8001 already exists -- skipping"

5. **No `jira.create_link` call is made.** The pre-existing link is sufficient; creating a duplicate link would be redundant and could cause Jira API errors.

### Why This Matters

The idempotent link check prevents:
- **Duplicate links** in Jira when re-triaging an issue or when links were created by another process (e.g., PSIRT, a previous triage run, or manual linking by an engineer).
- **API errors** from attempting to create a link that already exists.
- **Noise** in the issue's link section from redundant entries.

This pattern is consistent across the skill: the same idempotent check is specified in Step 4.3 (cross-CVE overlap detection) for both "Related" and "Depend" links.

### Remaining Step 4 Outcomes

- **Step 4.1 (Same-stream duplicates)**: No same-stream duplicates found. TC-8001 is a different-stream companion.
- **Step 4.2 (Affects Versions overlap)**: No overlap. TC-8006 carries RHTPA 2.1.0 (stream 2.1.x); TC-8001 carries RHTPA 2.2.0 and RHTPA 2.2.1 (stream 2.2.x).
- **Step 4.3 (Cross-CVE overlap)**: Skipped -- Upstream Affected Component custom field not configured.
- **Step 4.4 (Preemptive task reconciliation)**: No preemptive tasks found for this CVE and stream.
