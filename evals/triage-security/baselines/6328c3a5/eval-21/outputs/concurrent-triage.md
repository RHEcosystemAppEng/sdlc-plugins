# Step 7 -- Concurrent Triage Detection for TC-8020

## Prerequisites

- **Upstream Affected Component custom field**: configured as `customfield_10632`
- **Upstream Affected Component value on TC-8020**: `quinn-proto`

Since the Upstream Affected Component custom field is configured and populated on
TC-8020, Step 7 proceeds (not skipped).

## JQL Search for In-Progress Triages

Query executed (simulated):

```
project = TC
  AND issuetype = 10024
  AND cf[10632] ~ 'quinn-proto'
  AND status IN ('In Progress', 'Code Review')
  AND key != TC-8020
```

### Search Results

| CVE Issue | Status | Assignee |
|-----------|--------|----------|
| TC-8019 | In Progress | engineer-b@example.com |

**1 result returned.**

## Concurrent Triage Detected

Another engineer (`engineer-b@example.com`) is actively triaging TC-8019, which
affects the same upstream component (`quinn-proto`). TC-8019 is currently in
"In Progress" status, indicating active triage work.

Creating remediation tasks for TC-8020 at this point risks producing duplicate
remediation tasks if TC-8019's triage also reaches Step 8 and creates tasks
targeting the same quinn-proto dependency bump.

## Options Presented to Engineer

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
3. Proceed -- create tasks anyway with a `concurrent-triage-overlap` label
   so the other engineer's Step 4.3 catches the overlap
```

## Analysis of Each Option

### Option 1: Wait
- Stop execution and inform the engineer to re-run triage after TC-8019
  completes.
- This is the safest option to avoid duplicate remediation tasks.
- The engineer should coordinate with engineer-b@example.com to determine
  when TC-8019's triage is complete.

### Option 2: Skip
- Skip Step 8 entirely (do not create remediation tasks).
- Add a Jira comment to TC-8020 explaining why task creation was skipped
  due to concurrent triage on the same component.
- The engineer can re-run triage later once TC-8019 is resolved.

### Option 3: Proceed
- Add the `concurrent-triage-overlap` label to TC-8020.
- Continue to Case A/B/C branching and create remediation tasks.
- The `concurrent-triage-overlap` label ensures that when TC-8019's
  triage reaches Step 4.3 (Cross-CVE overlap detection), it will
  detect TC-8020's remediation tasks and handle the overlap
  (either skip duplicate creation or link to existing tasks).
- This option is appropriate when the engineer is confident the two
  CVEs require separate remediation despite targeting the same component,
  or when the engineer wants to proceed without waiting.

## Recommendation

**Option 1 (Wait)** is recommended when the two CVEs likely require the same
dependency bump (e.g., both are fixed by upgrading quinn-proto to >= 0.11.14).
In that case, TC-8019's remediation task would already cover TC-8020's fix,
and Step 4.3's cross-CVE overlap detection on a re-run would detect the
covering remediation and avoid creating duplicate tasks.

**Option 3 (Proceed)** is acceptable when the engineer wants to move forward
immediately and trusts the overlap detection mechanism to reconcile any
duplicates later.

## Gate Status

Step 7 **blocks progression** to Step 7.5 (Release Jira Orchestration) and
Step 8 (Remediation) until the engineer selects one of the three options.
No remediation tasks, release Jira links, or Case A/B/C branching decisions
are made until the concurrent triage gate is resolved.
