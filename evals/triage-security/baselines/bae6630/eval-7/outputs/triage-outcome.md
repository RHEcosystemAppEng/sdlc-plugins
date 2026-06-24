# Triage Outcome -- TC-8006

## How Step 4.2 Handled the Pre-Existing Link

### Context

TC-8006 (`[rhtpa-2.1]`) arrived with a pre-existing "Related" link to sibling TC-8001 (`[rhtpa-2.2]`). Both issues track the same CVE (CVE-2026-31812) for the quinn-proto library, but in different product version streams (2.1.x and 2.2.x respectively).

### Step 4.2 Idempotent Link Handling

Step 4.2 of the `triage-security` skill specifies an explicit idempotency check before creating cross-stream sibling links. The procedure is:

1. **Check for existing link**: Read the current issue's `issuelinks` array from the `jira.get_issue` response (already fetched in Step 1). Check if any existing link satisfies ALL of:
   - `type.name` is `"Related"`
   - `inwardIssue.key` or `outwardIssue.key` matches the sibling key

2. **If a matching link exists**: Skip link creation and log the message:
   > "Related link to [sibling-key] already exists -- skipping"

3. **If no matching link exists**: Create the link via `jira.create_link`.

### Application to TC-8006

The `issuelinks` array from TC-8006's issue data (fetched in Step 1) contains:

```
Link ID: 1990401
Type: Related
Direction: outward (TC-8006 -> TC-8001)
```

This link satisfies both conditions:
- `type.name` = "Related" (matches)
- `outwardIssue.key` = "TC-8001" (matches the sibling key)

**Outcome**: Link creation was **skipped**. The skill logged: "Related link to TC-8001 already exists -- skipping."

No duplicate link was created. No Jira API call to `jira.create_link` was made. This is the correct idempotent behavior -- running triage on an issue that already has its sibling links in place does not produce redundant link mutations.

### Additional Step 4.2 Checks

After the link check, Step 4.2 performed two additional verifications:

1. **Affects Versions overlap**: TC-8006 carries `RHTPA 2.1.0` (stream 2.1.x) and TC-8001 carries `RHTPA 2.2.0, RHTPA 2.2.1` (stream 2.2.x). No overlap detected -- each issue correctly owns only its own stream's versions.

2. **Sibling landscape presentation**: The companion issue table was presented showing TC-8001 (2.2.x, In Progress) and TC-8006 (2.1.x, New), giving the engineer visibility into the full CVE tracking picture across streams.

### Overall Triage Summary

- **Issue**: TC-8006 (CVE-2026-31812, quinn-proto < 0.11.14)
- **Stream scope**: 2.1.x
- **Affected versions in scope**: RHTPA 2.1.0 (quinn-proto 0.11.9, which is < 0.11.14)
- **RHTPA 2.1.1** also ships quinn-proto 0.11.9 and is affected -- Affects Versions correction needed to add RHTPA 2.1.1
- **Sibling TC-8001**: In Progress for stream 2.2.x -- already linked via pre-existing Related link (no new link created)
- **Cross-stream impact**: Stream 2.2.x versions 2.2.0 and 2.2.1 are also affected but tracked by sibling TC-8001. Versions 2.2.3+ are fixed (ship quinn-proto 0.11.14).
- **Remediation**: Case A applies -- create remediation tasks for stream 2.1.x (upstream backport task for rhtpa-backend on release/0.3.z branch + downstream propagation subtask for rhtpa-release.0.3.z Konflux repo)
