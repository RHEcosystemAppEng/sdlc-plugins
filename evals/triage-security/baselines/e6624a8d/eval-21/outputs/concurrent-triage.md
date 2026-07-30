# Step 7 -- Concurrent Triage Detection: TC-8020

## Configuration

The Upstream Affected Component custom field (`customfield_10632`) is configured in Security Configuration. The current issue TC-8020 has this field set to `quinn-proto`. Step 7 is therefore applicable (not skipped).

## JQL Query

```
project = TC
  AND issuetype = 10024
  AND cf[10632] ~ 'quinn-proto'
  AND status IN ('In Progress', 'Code Review')
  AND key != TC-8020
```

## Results

The JQL search returned **1 result**:

| CVE Issue | Status | Assignee |
|-----------|--------|----------|
| TC-8019 | In Progress | engineer-b@example.com |

## Analysis

Concurrent triage detected. Another engineer (`engineer-b@example.com`) is actively triaging TC-8019, which affects the same upstream component (`quinn-proto`). TC-8019 is currently in "In Progress" status, meaning that engineer is likely performing their own version impact analysis or remediation task creation for a different CVE that also targets quinn-proto.

Creating remediation tasks for TC-8020 now could produce duplicate remediation work if TC-8019's triage also results in a quinn-proto version bump that meets or exceeds the fix threshold for CVE-2026-31812 (>= 0.11.14). The two triages could each independently create upstream backport and downstream propagation tasks that target the same library in the same repositories.

## Warning Presented to Engineer

```
Concurrent triage detected on the same upstream component (quinn-proto):

| CVE Issue | Status      | Assignee                  |
|-----------|-------------|---------------------------|
| TC-8019   | In Progress | engineer-b@example.com    |

Another engineer is actively triaging a related CVE. Creating remediation
tasks now may produce duplicates.

Options:
1. Wait -- pause until the other triage completes, then re-run Step 4.3
   to detect any overlap
2. Skip -- skip remediation task creation for this CVE
3. Proceed -- create tasks anyway with a concurrent-triage-overlap label
   so the other engineer's Step 4.3 catches the overlap
```

## Handling

The engineer must choose one of the three options before the triage can proceed to Case A/B/C branching in Step 8:

- **Option 1 (Wait)**: Stop execution. The engineer should re-run triage on TC-8020 after TC-8019's triage completes. At that point, Step 4.3 (Cross-CVE overlap detection) will detect whether TC-8019's remediation already covers CVE-2026-31812's fix threshold (>= 0.11.14).

- **Option 2 (Skip)**: Skip Step 8 entirely. No remediation tasks are created. A Jira comment is added to TC-8020 explaining that task creation was skipped due to concurrent triage on TC-8019 for the same upstream component quinn-proto.

- **Option 3 (Proceed)**: Add the `concurrent-triage-overlap` label to TC-8020 and continue to Step 8 (Case A cross-stream impact check, then Case B remediation task creation). The label ensures TC-8019's engineer can detect the overlap via their own Step 4.3 cross-CVE overlap detection when they reach that step.
