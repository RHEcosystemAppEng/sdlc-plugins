# Step 7 -- Concurrent Triage Detection

## Prerequisite Check

The Upstream Affected Component custom field (customfield_10632) is configured in Security Configuration. Step 7 proceeds.

The current issue TC-8020 has customfield_10632 set to **quinn-proto**.

## Concurrent Triage Search

The following JQL query was constructed to search for in-progress triages on the same upstream component:

```
project = TC
  AND issuetype = 10024
  AND cf[10632] ~ 'quinn-proto'
  AND status IN ('In Progress', 'Code Review')
  AND key != TC-8020
```

### Search Results

The JQL search returned **1 result**:

| Issue | Status | CVE | Summary | Assignee |
|-------|--------|-----|---------|----------|
| TC-8019 | In Progress | (from labels) | (concurrent triage on quinn-proto) | engineer-b@example.com |

## Concurrent Triage Warning

**WARNING: Concurrent triage detected on the same upstream component (quinn-proto):**

| CVE Issue | Status | Assignee |
|-----------|--------|----------|
| TC-8019 | In Progress | engineer-b@example.com |

Another engineer is actively triaging a related CVE that affects the same upstream component (quinn-proto). Creating remediation tasks now may produce duplicate remediation tasks if both triages reach Step 8 simultaneously.

**Options:**

1. **Wait** -- Pause until the other triage (TC-8019) completes, then re-run Step 4.3 to detect any overlap. This is the safest option to avoid duplicate remediation tasks.

2. **Skip** -- Skip remediation task creation for this CVE (TC-8020). A Jira comment will be added to TC-8020 explaining that task creation was skipped due to concurrent triage on the same component.

3. **Proceed** -- Create remediation tasks anyway with a `concurrent-triage-overlap` label added to TC-8020, so that engineer-b's Step 4.3 cross-CVE overlap detection can catch the overlap when their triage reaches that step.

**Awaiting engineer confirmation before proceeding to Case A/B/C branching in Step 8.**

## Analysis

This concurrent triage check runs **before** Case A/B/C branching in Step 8. The purpose is to prevent duplicate remediation tasks when two engineers are triaging different CVEs that affect the same upstream component (quinn-proto) simultaneously. Without this check, both triages could independently create upstream backport tasks and downstream propagation tasks for the same library bump, resulting in duplicate work.

The detection uses the Upstream Affected Component custom field (customfield_10632) to find Vulnerability issues with matching component values that are currently In Progress or in Code Review status, excluding the current issue.

### Implications of Each Option

- **Wait**: The most conservative approach. After TC-8019's triage completes, Step 4.3 cross-CVE overlap detection would automatically detect whether TC-8019's remediation already covers TC-8020's fix threshold. If the bump version from TC-8019's remediation meets or exceeds 0.11.14, no new tasks are needed.

- **Skip**: Appropriate when the engineer believes TC-8019's triage will cover this CVE's fix. A comment documents the decision for audit trail purposes.

- **Proceed**: Creates tasks with the `concurrent-triage-overlap` label. This label ensures that when engineer-b's triage of TC-8019 reaches Step 4.3, it will detect the overlap via the cross-CVE overlap detection mechanism and can reconcile the duplicate tasks.
