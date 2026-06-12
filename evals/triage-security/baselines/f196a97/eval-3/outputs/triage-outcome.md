# Triage Outcome: TC-8003

## Decision: Close as Duplicate of TC-7999

### Rationale

TC-8003 (CVE-2026-31812 quinn-proto - Panic on large stream counts [rhtpa-2.2])
is a **duplicate** of TC-7999, which tracks the same CVE for the same version
stream (2.2.x).

**Evidence:**

1. **Same CVE**: Both issues carry the label CVE-2026-31812
2. **Same stream**: Both issues have the stream suffix [rhtpa-2.2], mapping to
   the 2.2.x version stream
3. **Same component**: Both issues have the label pscomponent:org/rhtpa-server
4. **TC-7999 is already In Progress**: Active remediation work is underway on
   the existing issue
5. **TC-7999 has correct Affects Versions**: RHTPA 2.2.0 and RHTPA 2.2.1 are
   already set, which matches the version impact analysis showing quinn-proto
   versions 0.11.9 and 0.11.12 (both < 0.11.14) in those releases

### Proposed Jira Actions

The following actions would be performed after engineer confirmation:

1. **Add comment to TC-8003**:
   > Duplicate of TC-7999 -- same CVE (CVE-2026-31812) tracked for the same
   > stream [rhtpa-2.2]. Version impact analysis confirms overlap: both issues
   > cover RHTPA 2.2.0 (quinn-proto 0.11.9) and RHTPA 2.2.1 (quinn-proto
   > 0.11.12). TC-7999 is already In Progress with correct Affects Versions.

2. **Transition TC-8003 to Closed** with resolution **Duplicate**

3. **Assign TC-8003** to current user

4. **Add label** `ai-cve-triaged` to TC-8003

### Version Impact Summary

For reference, the full version impact analysis for CVE-2026-31812
(quinn-proto < 0.11.14) in the 2.2.x stream:

| Version | quinn-proto | Affected? | Notes |
|---------|-------------|-----------|-------|
| RHTPA 2.2.0 | 0.11.9 | YES | |
| RHTPA 2.2.1 | 0.11.12 | YES | |
| RHTPA 2.2.2 | (retag of 2.2.1) | YES | Same as 2.2.1 |
| RHTPA 2.2.3 | 0.11.14 | NO | Ships fixed version |
| RHTPA 2.2.4 | 0.11.14 | NO | Ships fixed version |

Note: The 2.1.x stream is also affected (versions 2.1.0 and 2.1.1 both ship
quinn-proto 0.11.9), but that stream is outside the scope of this issue's
[rhtpa-2.2] suffix. Cross-stream impact would be handled by separate PSIRT
issues for the 2.1.x stream.

### Steps Not Executed

Because TC-8003 is being closed as a duplicate, the following steps were
short-circuited:

- **Step 5 (Version Lifecycle Check)**: Not needed -- TC-7999 is already
  tracking remediation
- **Step 6 (Already Fixed Check)**: Not needed -- TC-7999 is In Progress,
  not resolved
- **Step 7 (Remediation Task Creation)**: Not needed -- remediation is being
  handled under TC-7999
