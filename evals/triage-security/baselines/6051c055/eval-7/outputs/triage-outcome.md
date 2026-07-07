# Step 4.2 Triage Outcome: Pre-Existing Link Handling

## Summary

TC-8006 (CVE-2026-31812, stream [rhtpa-2.1]) has a pre-existing Related link to sibling TC-8001 (stream [rhtpa-2.2]). Step 4.2 detected this existing link and correctly skipped link creation, demonstrating idempotent behavior.

## Step 4.2 Detailed Walkthrough

### 1. Sibling Identified

The JQL search for sibling issues with label `CVE-2026-31812` returned TC-8001:
- **Key**: TC-8001
- **Stream suffix**: [rhtpa-2.2] (different from TC-8006's [rhtpa-2.1])
- **Classification**: Different-stream companion (not a duplicate)
- **Status**: In Progress
- **Affects Versions**: RHTPA 2.2.0, RHTPA 2.2.1

### 2. Pre-Existing Link Detection

Per Step 4.2 of the skill specification, before creating a Related link the skill must:

> "Check for existing link before creating one. Read the current issue's `issuelinks` array from the `jira.get_issue` response (already fetched in Step 1). Check if any existing link satisfies all of:
> - `type.name` is `"Related"`
> - `inwardIssue.key` or `outwardIssue.key` matches the sibling key"

**Inspection of TC-8006's issuelinks:**

The issue data from Step 1 shows TC-8006 already has the following link:
- **Link ID**: 1990401
- **Type**: Related
- **Direction**: outward (TC-8006 -> TC-8001)
- **outwardIssue.key**: TC-8001

**Matching evaluation:**
- `type.name == "Related"`: YES
- `outwardIssue.key == "TC-8001"` (matches sibling key): YES

Both criteria are satisfied.

### 3. Link Creation Skipped

Because a matching link already exists, the skill follows the specified behavior:

> "If a matching link exists, skip link creation and log:
> 'Related link to [sibling-key] already exists -- skipping'"

**Log message:**
> Related link to TC-8001 already exists -- skipping

No `jira.create_link` call is made. This prevents a duplicate link error from Jira and ensures idempotent behavior when re-triaging or when PSIRT has already pre-linked companion issues.

### 4. Remaining Step 4.2 Actions Still Performed

Even though link creation was skipped, the rest of Step 4.2 proceeds normally:

**Affects Versions overlap check:**
- TC-8006 Affects Versions: RHTPA 2.1.0 (stream 2.1.x)
- TC-8001 Affects Versions: RHTPA 2.2.0, RHTPA 2.2.1 (stream 2.2.x)
- Result: No overlap detected. Each issue owns versions exclusively from its own stream.

**Sibling landscape table presented to engineer:**

CVE-2026-31812 companion issues:

| Issue | Stream | Status | Affects Versions |
|-------|--------|--------|------------------|
| TC-8001 | 2.2.x | In Progress | RHTPA 2.2.0, RHTPA 2.2.1 |
| TC-8006 (current) | 2.1.x | New | RHTPA 2.1.0 |

### 5. Why This Matters

The idempotent link check in Step 4.2 handles several real-world scenarios:

1. **PSIRT pre-linking**: PSIRT may link companion issues when creating them, as happened here with TC-8006 and TC-8001. Without the idempotency check, the skill would attempt to create a duplicate link and either error or create a redundant link.

2. **Re-triage**: If an engineer re-runs triage on an already-triaged issue, the links from the first triage run already exist. The skip prevents duplicate links.

3. **Audit trail**: The log message ("Related link to TC-8001 already exists -- skipping") provides a clear audit trail that the skill detected and respected the existing link rather than blindly creating a new one.

## Continuation

After Step 4.2 completes, triage continues with:
- Step 4.3 (Cross-CVE overlap detection) -- requires Upstream Affected Component custom field, which is not configured in this project's Security Configuration, so this step would be skipped
- Step 4.4 (Preemptive task reconciliation) -- search for preemptive tasks with label `security-preemptive` and `CVE-2026-31812`
- Steps 5-8 proceed as normal for the scoped 2.1.x stream
