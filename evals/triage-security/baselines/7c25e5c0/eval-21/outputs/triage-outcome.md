# Triage Outcome — TC-8020

## Step 7 Result: Concurrent Triage Detected

The concurrent triage detection check (Step 7) identified that **TC-8019** is currently in progress and triaging a different CVE that affects the same upstream component (**quinn-proto**). The check was performed using the Upstream Affected Component custom field (`customfield_10632`) configured in Security Configuration.

### Detection Details

- **Current issue**: TC-8020 (CVE-2026-31812, quinn-proto)
- **Conflicting issue**: TC-8019 (In Progress, assigned to engineer-b@example.com)
- **Shared component**: quinn-proto (Upstream Affected Component field)

### Why This Matters

Both TC-8019 and TC-8020 affect the same upstream library (quinn-proto). If both triages proceed to Step 8 independently, they may each create remediation tasks to bump quinn-proto — resulting in duplicate tasks targeting the same library in the same repository/branch.

### Options Presented

The engineer was presented with three options:

1. **Wait** — pause until TC-8019 completes, then re-run Step 4.3 cross-CVE overlap detection to see if TC-8019's remediation already covers TC-8020's fix threshold. This avoids duplicate tasks entirely.
2. **Skip** — do not create remediation tasks for TC-8020. Add a Jira comment documenting the skip reason (concurrent triage overlap with TC-8019).
3. **Proceed** — create remediation tasks with a `concurrent-triage-overlap` label. This label ensures that TC-8019's triage (if it reaches Step 4.3 later) will detect the overlap and can reconcile.

### Next Steps

The triage is paused at Step 7 pending the engineer's choice. No remediation tasks have been created. Case A/B/C branching in Step 8 will proceed only after the engineer selects one of the three options above.

- If **Wait**: execution halts; re-run triage after TC-8019 is resolved.
- If **Skip**: Step 8 is bypassed; a skip comment is posted to TC-8020.
- If **Proceed**: Step 8 continues with normal Case A/B/C logic, adding `concurrent-triage-overlap` to all created remediation tasks.
