# Step 7 -- Concurrent Triage Detection

## Prerequisite Check

The Upstream Affected Component custom field (`customfield_10632`) is configured in Security Configuration. This step is **not skipped**.

## Component Extraction

The current issue TC-8020 has `customfield_10632` (Upstream Affected Component) set to **quinn-proto**.

## JQL Search for In-Progress Triages

Query executed:

```
project = TC
  AND issuetype = 10024
  AND cf[10632] ~ 'quinn-proto'
  AND status IN ('In Progress', 'Code Review')
  AND key != TC-8020
```

### Search Results

The JQL search returned **1 result**:

| CVE Issue | Status | Assignee |
|-----------|--------|----------|
| TC-8019 | In Progress | engineer-b@example.com |

## Concurrent Triage Warning

A concurrent triage has been detected on the same upstream component (`quinn-proto`):

> **Concurrent triage detected** on the same upstream component (quinn-proto):
>
> | CVE Issue | Status | Assignee |
> |-----------|--------|----------|
> | TC-8019 | In Progress | engineer-b@example.com |
>
> Another engineer is actively triaging a related CVE that affects the same
> upstream library (quinn-proto). Creating remediation tasks now may produce
> duplicates if both triages independently create tasks to bump quinn-proto
> to a fixed version.

## Options Presented to Engineer

Three options are offered before proceeding to Case A/B/C branching in Step 8:

1. **Wait** -- Pause until TC-8019's triage completes. Once engineer-b finishes
   their triage, re-run from Step 4.3 (Cross-CVE Overlap Detection) to check
   whether TC-8019's remediation tasks already cover CVE-2026-31812's fix
   threshold (quinn-proto >= 0.11.14). This is the safest option to avoid
   duplicate remediation work.

2. **Skip** -- Skip remediation task creation for TC-8020 entirely. A Jira
   comment will be added to TC-8020 explaining that task creation was skipped
   due to concurrent triage on the same upstream component (quinn-proto) by
   TC-8019. The engineer can revisit later.

3. **Proceed** -- Create remediation tasks now, but add the
   `concurrent-triage-overlap` label to TC-8020. This label ensures that when
   engineer-b's triage of TC-8019 reaches Step 4.3 (Cross-CVE Overlap
   Detection), the overlap between TC-8019 and TC-8020 is detected
   automatically. If TC-8019's remediation already bumps quinn-proto to a
   version that meets or exceeds 0.11.14, the overlap detection will flag it
   and recommend closing TC-8020's redundant tasks.

## Rationale

Concurrent triage detection exists to prevent duplicate remediation tasks. When
two CVEs affect the same upstream component (quinn-proto in this case), fixing
one CVE by bumping the library to a new version often fixes the other CVE as
well. Without this detection step, both triages could independently create tasks
to bump quinn-proto, resulting in duplicate work.

The choice between wait, skip, and proceed depends on:
- **Urgency of the due date** (TC-8020 is due 2026-07-15)
- **Confidence that TC-8019's fix will cover TC-8020** (depends on whether
  TC-8019's target version >= 0.11.14)
- **Coordination with engineer-b** (whether direct communication is feasible)

## Next Steps

The engineer must select one of the three options before triage can continue to
Step 8 (Remediation). No Jira mutations for remediation task creation will occur
until the engineer responds.
