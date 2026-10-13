# Step 7 -- Concurrent Triage Detection for TC-8020

## Prerequisite Check

- **Upstream Affected Component custom field**: customfield_10632 -- configured in Security Configuration.
- **Current issue's Upstream Affected Component value**: `quinn-proto` (extracted from customfield_10632 on TC-8020).
- **Prerequisite satisfied**: Yes. The field is configured and populated, so Step 7 proceeds.

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

**One result returned.**

## Concurrent Triage Warning

A concurrent triage has been detected on the same upstream component (`quinn-proto`):

```
WARNING: Concurrent triage detected on the same upstream component (quinn-proto):

| CVE Issue | Status      | Assignee                |
|-----------|-------------|-------------------------|
| TC-8019   | In Progress | engineer-b@example.com  |

Another engineer is actively triaging a related CVE that affects the same
upstream component (quinn-proto). Creating remediation tasks now may produce
duplicates if both triages reach Step 8 simultaneously.

Options:
1. Wait -- pause until the other triage (TC-8019) completes, then re-run
   Step 4.3 to detect any overlap with remediation tasks created by TC-8019.
2. Skip -- skip remediation task creation for this CVE entirely. Add a Jira
   comment explaining why task creation was skipped due to concurrent triage.
3. Proceed -- create remediation tasks anyway with a `concurrent-triage-overlap`
   label so that TC-8019's triage (specifically its Step 4.3 cross-CVE overlap
   detection) catches the overlap and avoids duplicate tasks.
```

## Analysis

TC-8019 is triaging a different CVE that also affects `quinn-proto` and is currently In Progress. This means another engineer (engineer-b@example.com) is actively working on triage for the same upstream library.

### Risk of proceeding without coordination

If TC-8020 proceeds to Step 8 (remediation task creation) while TC-8019 is still in progress, both triages could independently create remediation tasks that bump `quinn-proto` -- resulting in duplicate remediation work for the same library in the same streams. For example:

- TC-8019 may create a task to bump quinn-proto to version X for stream 2.2.x.
- TC-8020 would create its own task to bump quinn-proto to >= 0.11.14 for stream 2.2.x.
- If TC-8019's bump version already meets or exceeds 0.11.14, the TC-8020 task is redundant.

### Recommended course of action

The three options each have trade-offs:

1. **Wait** (recommended when timelines allow): Pausing allows TC-8019 to complete. When TC-8020 is re-run, Step 4.3 (cross-CVE overlap detection) will detect whether TC-8019's remediation tasks already bump quinn-proto past 0.11.14. If they do, TC-8020 can skip task creation and link to the existing remediation. This avoids all duplication.

2. **Skip**: Appropriate if TC-8019 is expected to cover the same fix threshold. However, this risks leaving TC-8020 without remediation if TC-8019's fix does not reach 0.11.14.

3. **Proceed**: Safe when combined with the `concurrent-triage-overlap` label. The label ensures that TC-8019's subsequent Step 4.3 run will detect the overlap and reconcile. This adds a small amount of coordination overhead but does not block either triage.

## Outcome Gate

Step 7 blocks progression to Step 7.5 (Release Jira Orchestration) and Step 8 (Case A/B/C remediation branching) until the engineer selects one of the three options. No remediation tasks, release Jira structures, or Jira mutations beyond the concurrent-triage warning are performed until the engineer responds.
