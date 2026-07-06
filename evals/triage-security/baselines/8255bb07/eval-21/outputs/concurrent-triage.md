# Concurrent Triage Detection (Step 7) -- TC-8020

## Prerequisite Check

The Upstream Affected Component custom field (`customfield_10632`) is configured in Security Configuration. The field on TC-8020 is populated with value `quinn-proto`. Step 7 proceeds.

## JQL Query Executed

```
project = TC
  AND issuetype = 10024
  AND cf[10632] ~ 'quinn-proto'
  AND status IN ('In Progress', 'Code Review')
  AND key != TC-8020
```

## Results

The search returned **1 result**:

| CVE Issue | Status | Assignee |
|-----------|--------|----------|
| TC-8019 | In Progress | engineer-b@example.com |

## Concurrent Triage Warning

**Concurrent triage detected on the same upstream component (quinn-proto).**

Another engineer (`engineer-b@example.com`) is actively triaging TC-8019, which also affects the `quinn-proto` upstream component. TC-8019 is currently `In Progress`, meaning that engineer is likely in or approaching Step 8 (Remediation) and may create remediation tasks that bump `quinn-proto` past the fix threshold.

Creating remediation tasks for TC-8020 now risks producing duplicate tasks if TC-8019's remediation already covers the same library bump. This is the exact scenario Step 7 is designed to prevent.

## Options Presented to Engineer

1. **Wait** -- Pause triage until TC-8019 completes. Once TC-8019 is resolved, re-run from Step 4.3 (cross-CVE overlap detection) to check whether TC-8019's remediation already covers CVE-2026-31812's fix threshold (quinn-proto >= 0.11.14). If the overlap is confirmed, TC-8020 can be closed without creating duplicate tasks.

2. **Skip** -- Skip remediation task creation (Step 8) entirely for TC-8020. Add a Jira comment to TC-8020 explaining that task creation was skipped due to concurrent triage of the same upstream component on TC-8019. The issue remains triaged (Affects Versions corrected, ai-cve-triaged label applied) but no remediation tasks are created.

3. **Proceed** -- Create remediation tasks for TC-8020 anyway, but add the `concurrent-triage-overlap` label to TC-8020. This label ensures that when TC-8019's triage reaches Step 4.3 (cross-CVE overlap detection), it will detect TC-8020's tasks and reconcile any overlap. This is the safest option when the engineer believes both CVEs require independent remediation or when the fix thresholds differ.

## Timing

This concurrent triage check runs **before** Case A/B/C branching in Step 8. The engineer must choose one of the three options before the skill proceeds to determine the remediation path (Case A: create tasks, Case B: cross-stream impact, or Case C: close as not affected).

## Recommendation

Given that TC-8019 is `In Progress` on the same component (`quinn-proto`), the recommended option depends on context:

- If TC-8019's CVE also requires bumping quinn-proto to >= 0.11.14 (or higher), **Option 1 (Wait)** is safest -- it avoids duplicate tasks entirely.
- If the engineer needs to proceed immediately, **Option 3 (Proceed with label)** preserves forward progress while enabling automated reconciliation via Step 4.3 overlap detection on the other triage.
- **Option 2 (Skip)** is appropriate only if the engineer has confirmed out-of-band that TC-8019's remediation will cover this CVE.
