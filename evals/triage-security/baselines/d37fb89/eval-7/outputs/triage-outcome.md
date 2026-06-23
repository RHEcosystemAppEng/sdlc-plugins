# Triage Outcome -- TC-8006 (Step 4.2 Pre-Existing Link Handling)

## How Step 4.2 Handled the Pre-Existing Link

### Context

TC-8006 (stream [rhtpa-2.1]) arrived with a pre-existing "Related" link to sibling TC-8001 (stream [rhtpa-2.2]). Both issues track the same CVE (CVE-2026-31812) for different product version streams. The link was already present in TC-8006's `issuelinks` array when fetched in Step 1.

### Step 4.2 Idempotent Link Behavior

Step 4.2 of the triage-security skill specifies an explicit idempotency check before creating cross-stream sibling links. The procedure is:

1. **Read the current issue's `issuelinks` array** from the `jira.get_issue` response already fetched in Step 1.
2. **Check if any existing link satisfies ALL of:**
   - `type.name` is `"Related"`
   - `inwardIssue.key` or `outwardIssue.key` matches the sibling key
3. **If a matching link exists:** skip link creation and log "Related link to [sibling-key] already exists -- skipping."
4. **If no matching link exists:** create the link via `jira.create_link`.

### What Happened

TC-8006's issuelinks included:
- Link ID 1990401, type "Related", direction outward, target TC-8001

The skill checked this against sibling TC-8001 found by JQL:
- `type.name` == "Related"? **Yes**
- `outwardIssue.key` == "TC-8001"? **Yes**

Both conditions were satisfied, so the skill logged:

> "Related link to TC-8001 already exists -- skipping"

No `jira.create_link` call was made. This prevents duplicate links from being created when the triage-security skill is run on an issue that was already partially processed or where PSIRT pre-linked the companion issues.

### Why This Matters

Without the idempotency check, re-running triage on TC-8006 would create a second "Related" link to TC-8001, resulting in duplicate links cluttering the issue. The Step 4.2 design ensures that:

- The skill is **safe to re-run** (idempotent for link creation)
- Pre-existing links created by PSIRT, other automation, or previous triage runs are respected
- The link direction (inward vs outward) does not matter -- the check covers both directions

### Overall Triage Outcome

The full triage for TC-8006 would proceed as follows after Step 4:

| Step | Result |
|------|--------|
| Step 1 -- Data Extraction | CVE-2026-31812, quinn-proto < 0.11.14, stream 2.1.x |
| Step 2 -- Version Impact | 2.1.0 (0.11.9, affected), 2.1.1 (0.11.9, affected) |
| Step 3 -- Affects Versions | Current: [RHTPA 2.1.0] -- may need addition of RHTPA 2.1.1 if it exists in Jira |
| Step 4 -- Sibling Check | TC-8001 (2.2.x) found, pre-existing Related link preserved, no duplicates |
| Step 5 -- Lifecycle Check | Would verify 2.1.x support status via product pages URL |
| Step 6 -- Already Fixed Check | TC-8001 is In Progress (not resolved) -- no already-fixed scenario |
| Step 7 -- Remediation | Case A: Both 2.1.0 and 2.1.1 are affected -- create remediation tasks for 2.1.x stream (2 tasks: upstream backport + downstream propagation for Cargo ecosystem) |

Cross-stream impact note: The 2.2.x stream is also affected (2.2.0 and 2.2.1 ship vulnerable versions), but that stream is tracked by companion issue TC-8001 which is already In Progress. No new Vulnerability issues or remediation tasks would be created for 2.2.x from this issue.
