# Triage Outcome for TC-8006

## How Step 4.2 Handled the Pre-Existing Link

### Context

TC-8006 (stream [rhtpa-2.1]) arrived with a pre-existing "Related" link to sibling TC-8001 (stream [rhtpa-2.2]). This link (Link ID 1990401, direction: outward from TC-8006 to TC-8001) was already present in the issue's `issuelinks` array when the issue was fetched in Step 1.

### Step 4.2 Idempotent Link Handling

The Step 4.2 cross-stream coordination procedure specifies an explicit idempotency check before creating any link:

1. The procedure reads the current issue's `issuelinks` array from the `jira.get_issue` response (already fetched in Step 1).
2. It checks whether any existing link satisfies **all** of:
   - `type.name` is "Related"
   - `inwardIssue.key` or `outwardIssue.key` matches the sibling key
3. For TC-8006, the existing link to TC-8001 matches on both criteria:
   - `type.name` = "Related" (matches)
   - `outwardIssue.key` = "TC-8001" (matches the sibling key)
4. Because a matching link exists, Step 4.2 **skips link creation** and logs:
   > "Related link to TC-8001 already exists -- skipping"

This idempotent behavior prevents duplicate link creation. If the link had not existed, Step 4.2 would have proposed creating a new "Related" link (subject to engineer confirmation per the guardrails). The pre-existing link is functionally equivalent to one the skill would have created, so no further action is needed.

### Affects Versions Overlap Verification

Step 4.2 also verifies that there is no Affects Versions overlap between the two sibling issues. The check confirmed clean separation:
- TC-8006: RHTPA 2.1.0 (stream 2.1.x)
- TC-8001: RHTPA 2.2.0, RHTPA 2.2.1 (stream 2.2.x)

No overlap detected -- each issue owns only versions from its own stream.

## Overall Triage Assessment

### Version Impact Summary (scoped to 2.1.x per issue stream)

| Version | quinn-proto | Affected? | Notes |
|---------|-------------|-----------|-------|
| 2.1.0 | 0.11.9 | YES | 0.11.9 < 0.11.14 |
| 2.1.1 | 0.11.9 | YES | 0.11.9 < 0.11.14 |

Both versions in the 2.1.x stream ship quinn-proto 0.11.9, which is within the vulnerable range (versions before 0.11.14).

### Proposed Affects Versions Correction (Step 3)

- Current: [RHTPA 2.1.0]
- Proposed: [RHTPA 2.1.0, RHTPA 2.1.1]
- Rationale: Version impact analysis shows both 2.1.0 and 2.1.1 ship quinn-proto 0.11.9 (affected). PSIRT assigned only 2.1.0; 2.1.1 is missing and should be added.

### Sibling Landscape (Step 4)

| Issue | Stream | Status | Affects Versions | Link Status |
|-------|--------|--------|------------------|-------------|
| TC-8001 | 2.2.x | In Progress | RHTPA 2.2.0, RHTPA 2.2.1 | Pre-existing Related link (no action needed) |
| TC-8006 (current) | 2.1.x | New | RHTPA 2.1.0 (proposed: + RHTPA 2.1.1) | N/A |

### Triage Recommendation (Step 7 -- Case A: Affected)

Both versions in the 2.1.x stream are affected. Proposed actions:

1. **Correct Affects Versions**: Add RHTPA 2.1.1 to TC-8006's Affects Versions (RHTPA 2.1.0 already present)
2. **Create upstream backport task**: Remediate CVE-2026-31812 -- bump quinn-proto to >= 0.11.14 on branch `release/0.3.z` in the `backend` (rhtpa-backend) repository
3. **Create downstream propagation task**: Update backend source reference in rhtpa-release.0.3.z Konflux repo to pick up the upstream fix (blocked by upstream task)
4. **Link tasks**: Link both tasks to TC-8006 with "Depend" link type; link downstream task as blocked by upstream task
5. **Add ai-cve-triaged label**: Mark TC-8006 as triaged
6. **Post summary comment**: Document version impact, Affects Versions correction, and remediation tasks on TC-8006

All of the above are proposed actions pending engineer confirmation. No Jira mutations have been executed.
