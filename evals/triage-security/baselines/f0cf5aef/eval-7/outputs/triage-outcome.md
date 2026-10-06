# Triage Outcome: Step 4.2 Pre-Existing Link Handling for TC-8006

## Summary

TC-8006 (CVE-2026-31812, stream [rhtpa-2.1]) has a pre-existing Related link to sibling TC-8001 (stream [rhtpa-2.2]). Step 4.2 correctly detected this link and handled it idempotently by skipping link creation.

## How Step 4.2 Handled the Pre-Existing Link

### The Idempotent Link Check

Step 4.2 specifies the following procedure for cross-stream siblings:

> "Check for existing link before creating one. Read the current issue's issuelinks array from the jira.get_issue response (already fetched in Step 1). Check if any existing link satisfies all of:
> - type.name is "Related"
> - inwardIssue.key or outwardIssue.key matches the sibling key"

### Application to TC-8006

1. **Existing links on TC-8006**: The issue has one link -- Related (outward) to TC-8001, link ID 1990401.

2. **Check conditions**:
   - `type.name` is `"Related"` -- TRUE
   - `outwardIssue.key` matches the sibling key `TC-8001` -- TRUE

3. **Both conditions satisfied**: A matching link already exists.

4. **Action taken**: Link creation was **skipped** with the log message:
   > "Related link to TC-8001 already exists -- skipping"

5. **No Jira mutation occurred**: The skill did not attempt to call `jira.create_link`. This is the correct idempotent behavior -- re-running triage on an issue with pre-existing sibling links does not create duplicate links.

### Why This Matters

Without the idempotent check, re-triaging TC-8006 (or triaging it after someone manually created the Related link) would attempt to create a second Related link to TC-8001, which could either fail with a Jira API error or create a confusing duplicate link. The pre-existence check prevents both scenarios.

### Remaining Step 4.2 Actions

After skipping link creation, Step 4.2 continued with:

- **Affects Versions overlap check**: No overlap found. TC-8006 has RHTPA 2.1.0 (stream 2.1.x) and TC-8001 has RHTPA 2.2.0, RHTPA 2.2.1 (stream 2.2.x). Each issue correctly carries only its own stream's versions.
- **Sibling landscape presentation**: Both companion issues were presented in a summary table showing their stream, status, and Affects Versions for engineer review.

## Sibling Relationship Classification

TC-8001 is classified as a **different-stream companion** (not a duplicate) because:
- TC-8006 stream suffix: [rhtpa-2.1] (stream 2.1.x)
- TC-8001 stream suffix: [rhtpa-2.2] (stream 2.2.x)
- Different streams mean PSIRT intentionally created separate tracker issues per stream
- The correct link type is "Related" (companion), not "Duplicate"
