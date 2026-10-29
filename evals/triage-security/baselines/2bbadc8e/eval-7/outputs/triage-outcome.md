# Triage Outcome -- Step 4.2 Pre-Existing Link Handling

## Summary

Step 4.2 (Cross-Stream Coordination) determined that the pre-existing Related link between TC-8006 and TC-8001 satisfies the sibling linking requirement. **No new link was created.** The skill's idempotent link check detected the existing link and skipped the redundant Jira mutation.

## How Step 4.2 Handled the Pre-Existing Link

### Procedure Followed

Per the `jira-triage-operations.md` Step 4.2 procedure, before creating a Related link to a different-stream sibling, the skill checks the current issue's `issuelinks` array (already fetched in Step 1) for an existing link satisfying **all** of these criteria:

1. `type.name` is `"Related"`
2. `inwardIssue.key` or `outwardIssue.key` matches the sibling key

### Evidence Evaluated

TC-8006's existing issue links (from Step 1 data extraction):

| Link ID | Type | Direction | Target |
|---------|------|-----------|--------|
| 1990401 | Related | outward (TC-8006 -> TC-8001) | TC-8001 |

### Decision

- Criterion 1: Link type name is `"Related"` -- **satisfied**
- Criterion 2: `outwardIssue.key` matches sibling key TC-8001 -- **satisfied**

Both criteria are met. The existing link covers the cross-stream coordination requirement.

### Action Taken

> "Related link to TC-8001 already exists -- skipping"

**No Jira mutation proposed.** The skill recognized the pre-existing link and did not attempt to create a duplicate. This is the idempotent behavior specified in Step 4.2: "If a matching link exists, skip link creation and log."

### Why This Matters

The idempotent link check prevents two failure modes:

1. **Duplicate link errors**: Jira may reject a second Related link between the same two issues, causing a triage failure.
2. **Redundant mutations**: Even if Jira silently accepted the duplicate, creating unnecessary links wastes API calls and clutters the issue's link history.

The pre-existing link (ID 1990401) was created before this triage run -- possibly by PSIRT, a prior partial triage, or manual action. Regardless of its origin, the skill's check-before-create pattern correctly identified it as sufficient and skipped the creation step.

## Remaining Step 4 Outcomes

- **Step 4.1 (Same-Stream Duplicates)**: No same-stream siblings found. TC-8001 is in stream 2.2.x, TC-8006 is in stream 2.1.x. Not a duplicate.
- **Step 4.3 (Cross-CVE Overlap)**: Skipped -- Upstream Affected Component, PS Component, and Stream custom fields are not configured.
- **Step 4.4 (Preemptive Task Reconciliation)**: No preemptive tasks found for CVE-2026-31812 in stream 2.1.x. No reconciliation needed.

## PROPOSALS (Not Executed)

No Jira mutations are proposed from Step 4 for TC-8006. The only potential mutation (creating a Related link to TC-8001) was determined to be unnecessary because the link already exists.

Subsequent steps (Steps 5-8) would continue with the triage, potentially proposing:
- Affects Versions correction (Step 3 -- if version impact analysis identifies additional affected 2.1.x versions)
- Remediation task creation (Step 8 -- if supported 2.1.x versions are confirmed affected)
- Cross-stream impact comment (Step 8 Case A -- if 2.2.x stream is also affected and this is a scoped issue, though TC-8001 already tracks that stream)

All such mutations would be presented as proposals requiring engineer confirmation before execution.
