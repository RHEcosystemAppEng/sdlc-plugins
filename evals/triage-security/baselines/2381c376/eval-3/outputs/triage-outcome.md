# Triage Outcome: TC-8003

## Decision: Close as Duplicate

TC-8003 is a **duplicate** of TC-7999. Both issues track CVE-2026-31812 (quinn-proto panic on large stream counts) for the same version stream (2.2.x, stream suffix `[rhtpa-2.2]`).

TC-7999 is already **In Progress**, meaning an engineer is actively working on remediation for this CVE in the 2.2.x stream. Creating additional remediation tasks from TC-8003 would produce duplicate work.

## Rationale

1. **Same CVE**: Both TC-8003 and TC-7999 carry the label `CVE-2026-31812`.
2. **Same stream**: Both issues have the stream suffix `[rhtpa-2.2]`, scoping them to the 2.2.x version stream.
3. **Same component**: Both have the label `pscomponent:org/rhtpa-server`.
4. **Sibling is active**: TC-7999 is In Progress, confirming it is not stale or abandoned.
5. **Version coverage**: TC-7999 already has Affects Versions [RHTPA 2.2.0, RHTPA 2.2.1], covering the primary affected versions in the 2.2.x stream.

## Proposed Jira Actions

The following actions are proposed (not executed) per the triage-security procedure:

### 1. Add duplicate comment to TC-8003

**Proposed action**: Add comment to TC-8003

> Duplicate of TC-7999 -- same CVE (CVE-2026-31812) tracked for the same stream [rhtpa-2.2]. Version impact analysis confirms overlap: both issues cover quinn-proto vulnerability in the 2.2.x stream. TC-7999 is already In Progress with Affects Versions [RHTPA 2.2.0, RHTPA 2.2.1].

(Comment would include the Comment Footnote per skill requirements.)

### 2. Transition TC-8003 to Closed

**Proposed action**: Transition TC-8003 to Closed with resolution "Duplicate"

- Current status: New
- Target status: Closed
- Resolution: Duplicate

### 3. Assign TC-8003 to current user

**Proposed action**: Assign TC-8003 to the current (triaging) user to record who performed the duplicate assessment.

### 4. Add ai-cve-triaged label

**Proposed action**: Add `ai-cve-triaged` label to TC-8003 to mark it as triaged and prevent re-processing.

## Steps Not Executed (due to duplicate closure)

The following steps are skipped because the issue is being closed as a duplicate:

- **Step 3 (Affects Versions Correction)**: Not needed -- TC-8003 will be closed. The Affects Versions correction (adding RHTPA 2.2.1 and RHTPA 2.2.2) should be verified on TC-7999 instead.
- **Step 5 (Version Lifecycle Check)**: Not needed -- closure does not depend on lifecycle status.
- **Step 6 (Already Fixed Check)**: Not applicable -- TC-7999 is not resolved/closed.
- **Step 7 (Concurrent Triage Detection)**: Skipped -- Upstream Affected Component custom field not configured.
- **Step 7.5 (Release Jira Orchestration)**: Not needed -- no remediation tasks will be created.
- **Step 8 (Remediation)**: Not needed -- duplicate closure means no new remediation tasks.

## Cross-Stream Note

The version impact analysis reveals that stream 2.1.x is also affected (versions 2.1.0 and 2.1.1 both ship quinn-proto 0.11.9). However, since TC-8003 is scoped to `[rhtpa-2.2]` and is being closed as a duplicate, the cross-stream impact for 2.1.x is not actionable on this issue. The 2.1.x impact should be tracked separately -- either through an existing sibling CVE issue for the 2.1.x stream, or flagged for PSIRT to create one.

## Version Impact Summary (for reference)

| Version | Stream | quinn-proto | Affected? | Notes |
|---------|--------|-------------|-----------|-------|
| 2.1.0 | 2.1.x | 0.11.9 | YES | Outside this issue's scope |
| 2.1.1 | 2.1.x | 0.11.9 | YES | Outside this issue's scope |
| 2.2.0 | 2.2.x | 0.11.9 | YES | Covered by TC-7999 |
| 2.2.1 | 2.2.x | 0.11.12 | YES | Covered by TC-7999 |
| 2.2.2 | 2.2.x | -- | YES | retag of 2.2.1; covered by TC-7999 |
| 2.2.3 | 2.2.x | 0.11.14 | NO | Fixed (>= 0.11.14) |
| 2.2.4 | 2.2.x | 0.11.14 | NO | Fixed (>= 0.11.14) |
