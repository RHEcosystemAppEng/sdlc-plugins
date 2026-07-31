# Step 4.2 -- Triage Outcome: Pre-Existing Link Handling

## Summary

TC-8006 (stream [rhtpa-2.1]) has a pre-existing 'Related' link to sibling TC-8001 (stream [rhtpa-2.2]). Step 4.2's idempotent link check detected this and skipped link creation.

## How Step 4.2 Handled the Pre-Existing Link

### 1. Link Check Procedure

Per Step 4.2 of jira-triage-operations.md, before creating a 'Related' link to any different-stream sibling, the skill MUST check the current issue's `issuelinks` array (from the `jira.get_issue` response already fetched in Step 1). The check looks for any existing link satisfying ALL of:

- `type.name` is "Related"
- `inwardIssue.key` or `outwardIssue.key` matches the sibling key

### 2. Check Result

TC-8006's issuelinks array contains:

```
Link ID: 1990401
Type: Related
Direction: outward
outwardIssue.key: TC-8001
```

This satisfies all conditions of the idempotent check for sibling TC-8001.

### 3. Action Taken

**Link creation skipped.** The skill logged:

> Related link to TC-8001 already exists -- skipping

`jira.create_link` was NOT invoked. No Jira mutation occurred for this link.

### 4. Sibling Landscape Still Presented

The idempotent check only governs link creation. The sibling landscape table was still presented to the engineer:

```
CVE-2026-31812 companion issues:

| Issue      | Stream | Status      | Affects Versions              |
|------------|--------|-------------|-------------------------------|
| TC-8001    | 2.2.x  | In Progress | RHTPA 2.2.0, RHTPA 2.2.1     |
| TC-8006 <- | 2.1.x  | New         | RHTPA 2.1.0                   |
```

This ensures the engineer has full visibility into cross-stream companion issues regardless of whether link creation was needed.

### 5. Rationale

The idempotent link check (referenced as section 1.58 in the skill) prevents duplicate links when re-triaging an issue or when PSIRT pre-links sibling issues. Without this check, calling `jira.create_link` on an already-linked pair would either error or create a duplicate link. The check reads the existing `issuelinks` array from the Step 1 data fetch -- no additional Jira API call is required.
