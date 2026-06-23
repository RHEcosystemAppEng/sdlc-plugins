# Triage Outcome -- TC-8006

## Step 4.2 Pre-existing Link Handling

Step 4.2 requires creating a "Related" link between the current issue and any different-stream sibling issues found via JQL. However, it includes an **idempotent check**: before calling `jira.create_link`, the skill inspects the current issue's `issuelinks` array (already fetched in Step 1's `jira.get_issue` call) to determine whether a matching link already exists.

For TC-8006, the `issuelinks` array contains:

```
- type.name: "Related"
- outwardIssue.key: "TC-8001"
- Link ID: 1990401
```

This satisfies all three matching criteria defined in Step 4.2:
1. `type.name` is `"Related"` -- matches
2. `outwardIssue.key` is `"TC-8001"` -- matches the sibling key
3. Link direction is outward (TC-8006 -> TC-8001) -- valid

Because a matching "Related" link to TC-8001 already exists, `jira.create_link` is **not called**. The log message recorded:

> Related link to TC-8001 already exists -- skipping

### What the idempotent check affects

The pre-existing link check **only** controls whether `jira.create_link` is called. It does not suppress or alter any other Step 4.2 behavior:

- The **Affects Versions overlap check** still runs (no overlap found -- TC-8006 owns 2.1.x versions, TC-8001 owns 2.2.x versions).
- The **sibling landscape table** is still presented in full, showing both TC-8001 (2.2.x, In Progress) and TC-8006 (2.1.x, New).
- The sibling classification (DIFFERENT-stream companion) is still recorded.

This design ensures that re-running triage on an issue that was previously linked (or linked manually by PSIRT) does not create duplicate links while still providing the engineer with the complete cross-stream picture.

## Summary

- **Issue**: TC-8006 (CVE-2026-31812, quinn-proto, stream 2.1.x)
- **Sibling**: TC-8001 (same CVE, stream 2.2.x, In Progress)
- **Link action**: Skipped (pre-existing "Related" link detected)
- **Duplicate**: No (different streams)
- **Version impact (2.1.x)**: Both 2.1.0 and 2.1.1 ship quinn-proto 0.11.9 (vulnerable, below fix threshold 0.11.14)
- **Cross-stream note**: TC-8001 covers 2.2.x; versions 2.2.3+ already ship the fixed version (0.11.14)
- **Next steps**: Proceed through Steps 5-7 for stream 2.1.x remediation (both 2.1.0 and 2.1.1 are affected and require a fix)
