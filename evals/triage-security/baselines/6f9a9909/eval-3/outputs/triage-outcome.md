# Triage Outcome -- TC-8003

## Decision: Close as Duplicate

TC-8003 is a **duplicate** of TC-7999. Both issues track the same CVE (CVE-2026-31812)
for the same version stream (2.2.x, suffix `[rhtpa-2.2]`).

### Rationale

1. **Same CVE**: Both TC-8003 and TC-7999 carry the label CVE-2026-31812 and track
   the same vulnerability in quinn-proto (panic on large stream counts).

2. **Same stream scope**: Both issues have the identical stream suffix `[rhtpa-2.2]`,
   placing them in the 2.2.x version stream. Per the triage-security skill's Step 4.1,
   a same-stream sibling that is open or in progress triggers a duplicate closure
   recommendation.

3. **TC-7999 is already In Progress**: The sibling issue is actively being worked on,
   meaning triage and remediation are already underway. TC-7999 has broader Affects
   Versions coverage (RHTPA 2.2.0 and RHTPA 2.2.1) compared to TC-8003's single
   version (RHTPA 2.2.0).

4. **No additional value from TC-8003**: The version impact analysis confirms the same
   affected versions (2.2.0, 2.2.1, 2.2.2) that TC-7999 is already tracking. Keeping
   TC-8003 open would create confusion and duplicate remediation effort.

### Proposed Jira Actions

The following Jira mutations would be performed (each requiring engineer confirmation):

1. **Add comment to TC-8003:**
   > Duplicate of TC-7999 -- same CVE (CVE-2026-31812) tracked for the same stream
   > [rhtpa-2.2]. Version impact analysis confirms overlap:
   >
   > | Version | quinn-proto | Affected? |
   > |---------|-------------|-----------|
   > | 2.2.0 | 0.11.9 | YES |
   > | 2.2.1 | 0.11.12 | YES |
   > | 2.2.2 | (retag of 2.2.1) | YES |
   > | 2.2.3 | 0.11.14 | NO |
   > | 2.2.4 | 0.11.14 | NO |
   >
   > TC-7999 is already In Progress with Affects Versions [RHTPA 2.2.0, RHTPA 2.2.1].
   > Closing this issue as duplicate.

2. **Transition TC-8003** to Closed with resolution "Duplicate".

3. **Assign TC-8003** to current user.

4. **Add label** `ai-cve-triaged` to TC-8003.

### Steps Not Executed (due to duplicate closure)

The following steps are skipped because the issue is being closed as duplicate:

- **Step 3 (Affects Versions Correction):** Not needed -- TC-8003 is being closed,
  not corrected. TC-7999 already has appropriate Affects Versions.
- **Step 5 (Version Lifecycle Check):** Not needed -- lifecycle status is irrelevant
  for a duplicate closure.
- **Step 6 (Already Fixed Check):** Not needed -- duplicate closure takes precedence.
- **Step 7 (Concurrent Triage Detection):** Not needed -- no remediation tasks will
  be created.
- **Step 8 (Remediation):** Not needed -- TC-7999 owns remediation for this CVE
  in the 2.2.x stream. No new remediation tasks are created.

### Cross-Stream Note

The version impact analysis also reveals that the 2.1.x stream is affected
(quinn-proto 0.11.9 in both 2.1.0 and 2.1.1). However, since TC-8003 is scoped
to [rhtpa-2.2] and is being closed as a duplicate, cross-stream impact (Case A)
is not triggered from this issue. TC-7999 (the surviving issue) should address
cross-stream impact in its own triage if not already done.
