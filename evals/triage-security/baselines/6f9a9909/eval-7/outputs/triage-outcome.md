# Triage Outcome -- TC-8006

## How Step 4.2 Handled the Pre-Existing Link

### Context

TC-8006 (stream [rhtpa-2.1]) arrived with a pre-existing "Related" link to sibling TC-8001 (stream [rhtpa-2.2]). The link already existed in TC-8006's `issuelinks` array with the following properties:

- **Link ID**: 1990401
- **Type**: Related
- **Direction**: outward (TC-8006 -> TC-8001)

### Step 4.2 Idempotent Link Check

Step 4.2 specifies an idempotent link creation protocol. Before creating a "Related" link to any different-stream sibling, the skill reads the current issue's `issuelinks` array (already fetched in Step 1) and checks whether any existing link satisfies **all of**:

1. `type.name` is `"Related"`
2. `inwardIssue.key` or `outwardIssue.key` matches the sibling key

For sibling TC-8001:
- Condition 1: The existing link's type is "Related" -- **satisfied**
- Condition 2: The existing link's `outwardIssue.key` is "TC-8001" -- **satisfied**

Since a matching link already exists, Step 4.2 **skips link creation** and logs:

> "Related link to TC-8001 already exists -- skipping"

No `jira.create_link` API call is made. This ensures idempotent behavior -- re-running triage on an issue that already has sibling links does not create duplicate links.

### Remaining Step 4.2 Actions

Even though link creation was skipped, Step 4.2 still performs the remaining checks:

1. **Affects Versions overlap verification**: Confirmed no overlap between TC-8006 (RHTPA 2.1.0) and TC-8001 (RHTPA 2.2.0, RHTPA 2.2.1). Each issue carries versions from its own stream only.

2. **Sibling landscape presentation**: The companion issue table was presented showing both TC-8001 (2.2.x, In Progress) and TC-8006 (2.1.x, New).

## Overall Triage Outcome

### Version Impact Summary

TC-8006 is scoped to stream 2.1.x. Both versions in this stream are affected:

| Version | quinn-proto | Affected? |
|---------|-------------|-----------|
| 2.1.0 | 0.11.9 | YES |
| 2.1.1 | 0.11.9 | YES |

The fix threshold is quinn-proto >= 0.11.14.

### Cross-Stream Analysis (Case A)

TC-8006 is a scoped issue ([rhtpa-2.1]). The version impact analysis reveals that stream 2.2.x is also affected (versions 2.2.0, 2.2.1, 2.2.2 ship quinn-proto < 0.11.14). However, TC-8001 already exists as a companion CVE Jira for stream 2.2.x and is In Progress. Therefore:

- **No proactive remediation tasks** are needed for stream 2.2.x (it has its own CVE Jira: TC-8001)
- A cross-stream impact comment would be posted noting that stream 2.2.x is also affected and tracked by TC-8001

### Remediation (Case B)

Since both 2.1.x versions are affected, Case B applies: create remediation tasks for stream 2.1.x.

As quinn-proto is a **Cargo** (source dependency) ecosystem package, 2 tasks would be created per the ecosystem classification table:

1. **Upstream backport task**: Bump quinn-proto to >= 0.11.14 on the `release/0.3.z` branch of the backend source repository
2. **Downstream propagation task**: Update the Konflux release repo (rhtpa-release.0.3.z) to reference the upstream commit containing the fix. Blocked by the upstream task.

Both tasks would be linked to TC-8006 with link type "Depend".

### Post-Triage Actions

- Add `ai-cve-triaged` label to TC-8006
- Post summary comment with version impact table, Affects Versions correction, and links to created remediation tasks
- Include @mention of the issue reporter
