# Triage Outcome: TC-8003

## Decision: Close as Duplicate

TC-8003 is a **duplicate** of **TC-7999** and should be closed.

## Rationale

1. **Same CVE**: Both TC-8003 and TC-7999 track CVE-2026-31812 (quinn-proto
   panic on large stream counts).

2. **Same stream**: Both issues carry the stream suffix `[rhtpa-2.2]`,
   scoping them to the 2.2.x version stream. PSIRT created two separate
   Vulnerability issues for the same CVE in the same stream, which is a
   duplicate.

3. **TC-7999 is already In Progress**: The sibling issue is actively being
   worked on (status: In Progress), with Affects Versions already set to
   `RHTPA 2.2.0, RHTPA 2.2.1`. This is more complete than TC-8003's
   PSIRT-assigned `RHTPA 2.2.0` alone.

4. **Version impact confirms overlap**: Lock file analysis shows:
   - RHTPA 2.2.0 (quinn-proto 0.11.9) -- affected
   - RHTPA 2.2.1 (quinn-proto 0.11.12) -- affected
   - RHTPA 2.2.2 (retag of 2.2.1) -- affected
   - RHTPA 2.2.3 (quinn-proto 0.11.14) -- NOT affected (fixed)
   - RHTPA 2.2.4 (quinn-proto 0.11.14) -- NOT affected (fixed)

   All affected versions are already tracked by TC-7999.

## Proposed Jira Actions

The following actions require engineer confirmation before execution:

1. **Add comment to TC-8003**:
   > Duplicate of TC-7999 -- same CVE (CVE-2026-31812) tracked for the same
   > stream [rhtpa-2.2]. TC-7999 is already In Progress with Affects Versions
   > [RHTPA 2.2.0, RHTPA 2.2.1]. Version impact analysis confirms complete
   > overlap.
   >
   > Version impact for CVE-2026-31812 (quinn-proto < 0.11.14):
   >
   > | Version | quinn-proto | Affected? | Notes |
   > |---------|-------------|-----------|-------|
   > | 2.2.0 | 0.11.9 | YES | |
   > | 2.2.1 | 0.11.12 | YES | |
   > | 2.2.2 | -- | YES | retag of 2.2.1 |
   > | 2.2.3 | 0.11.14 | NO | fixed |
   > | 2.2.4 | 0.11.14 | NO | fixed |

2. **Transition TC-8003** to Closed with resolution **Duplicate**.

3. **Assign TC-8003** to the current user.

4. **Add label** `ai-cve-triaged` to TC-8003 to mark it as triaged.

## Steps Not Executed (due to duplicate closure)

The following steps are skipped because TC-8003 is closed as a duplicate:

- **Step 3 (Affects Versions Correction)**: Not needed -- TC-7999 already
  has the correct Affects Versions.
- **Step 5 (Version Lifecycle Check)**: Deferred to TC-7999's triage.
- **Step 6 (Already Fixed Check)**: Deferred to TC-7999's triage.
- **Step 7 (Concurrent Triage Detection)**: Not applicable -- no
  remediation tasks will be created from TC-8003.
- **Step 8 (Remediation)**: Not applicable -- remediation is handled
  through TC-7999.

## Cross-Stream Note

The 2.1.x stream (versions 2.1.0 and 2.1.1) is also affected by this CVE
(both ship quinn-proto 0.11.9). However, cross-stream remediation is not
handled from TC-8003 because it is a duplicate. Cross-stream impact should
be assessed from TC-7999's triage (Case A analysis).
