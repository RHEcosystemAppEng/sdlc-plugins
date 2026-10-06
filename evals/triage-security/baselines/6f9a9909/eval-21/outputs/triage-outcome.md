# Triage Outcome: TC-8020 (CVE-2026-31812 quinn-proto)

## Summary

TC-8020 tracks CVE-2026-31812, a denial-of-service vulnerability in quinn-proto (CVSS 7.5, High) where versions before 0.11.14 allow a remote attacker to cause a panic via excessive stream counts in QUIC transport frames. The issue is scoped to stream **2.2.x** via the summary suffix `[rhtpa-2.2]`.

## Version Impact

| Version | Stream | quinn-proto | Affected? | Notes |
|---------|--------|-------------|-----------|-------|
| 2.1.0 | 2.1.x | 0.11.9 | YES | |
| 2.1.1 | 2.1.x | 0.11.9 | YES | |
| 2.2.0 | 2.2.x | 0.11.9 | YES | |
| 2.2.1 | 2.2.x | 0.11.12 | YES | |
| 2.2.2 | 2.2.x | -- | YES | retag of 2.2.1 |
| 2.2.3 | 2.2.x | 0.11.14 | NO | fixed |
| 2.2.4 | 2.2.x | 0.11.14 | NO | fixed |

Within the issue's scoped stream (2.2.x), versions **2.2.0, 2.2.1, and 2.2.2** are affected. Versions 2.2.3 and 2.2.4 already ship the fixed version (0.11.14) and are not affected.

Stream 2.1.x (outside this issue's scope) is also affected: both 2.1.0 and 2.1.1 ship quinn-proto 0.11.9.

## Affects Versions Correction (Step 3)

The PSIRT-assigned Affects Version **RHTPA 2.0.0** is incorrect -- no 2.0.x stream exists in the configured Version Streams. The corrected Affects Versions (scoped to 2.2.x) should be:

- **Current**: `[RHTPA 2.0.0]`
- **Proposed**: `[RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]`

## Triage Decision: Case A + Case B (Affected, with cross-stream impact)

### Rationale

1. **Supported versions are affected** -- within the 2.2.x stream, versions 2.2.0, 2.2.1, and 2.2.2 ship vulnerable quinn-proto (< 0.11.14). This rules out Case C (close as not affected).

2. **Cross-stream impact (Case A)** -- the issue is scoped to 2.2.x, but 2.1.x is also affected. Case A applies: a cross-stream impact comment should be posted, and preemptive remediation tasks should be created for 2.1.x if no sibling CVE Jira exists for that stream.

3. **Remediation tasks needed (Case B)** -- since quinn-proto is a Cargo (source dependency) ecosystem package, two tasks per affected stream are required:
   - **Upstream backport task**: bump quinn-proto to >= 0.11.14 in the rhtpa-backend repository on the relevant upstream branch
   - **Downstream propagation task**: update the source reference in the Konflux release repo (rhtpa-release.0.4.z for 2.2.x) to pick up the upstream fix

### Concurrent Triage Gate (Step 7)

**Before creating any remediation tasks**, a concurrent triage was detected:

- **TC-8019** is In Progress, assigned to engineer-b@example.com, and also targets the quinn-proto upstream component (customfield_10632).

The engineer must choose one of three options before proceeding:

1. **Wait** -- pause until TC-8019 completes, then re-run to detect overlap via Step 4.3
2. **Skip** -- skip remediation task creation entirely
3. **Proceed** -- create tasks with a `concurrent-triage-overlap` label

**No remediation tasks can be created until the engineer resolves the concurrent triage gate.**

### Planned Remediation Tasks (if engineer chooses to proceed)

#### For stream 2.2.x (in-scope):

1. **Upstream backport task**: "Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (rhtpa-2.2)"
   - Repository: rhtpa-backend
   - Target branch: release/0.4.z
   - Labels: ai-generated-jira, Security, CVE-2026-31812
   - Link: Depend on TC-8020

2. **Downstream propagation task**: "Propagate CVE-2026-31812 fix: update rhtpa-backend ref in rhtpa-release.0.4.z (rhtpa-2.2)"
   - Repository: rhtpa-release.0.4.z
   - Target branch: main
   - Labels: ai-generated-jira, Security, CVE-2026-31812
   - Link: Depend on TC-8020, Blocks relationship with upstream task

#### For stream 2.1.x (cross-stream, Case A -- preemptive if no sibling CVE Jira exists):

3. **Upstream backport task (preemptive)**: "Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (rhtpa-2.1)"
   - Repository: rhtpa-backend
   - Target branch: release/0.3.z
   - Labels: ai-generated-jira, Security, CVE-2026-31812, security-preemptive
   - Link: Related to TC-8020 (not Depend, since this is a different stream)

4. **Downstream propagation task (preemptive)**: "Propagate CVE-2026-31812 fix: update rhtpa-backend ref in rhtpa-release.0.3.z (rhtpa-2.1)"
   - Repository: rhtpa-release.0.3.z
   - Target branch: main
   - Labels: ai-generated-jira, Security, CVE-2026-31812, security-preemptive
   - Link: Related to TC-8020, Blocks relationship with upstream preemptive task

### Post-Triage Actions

After remediation tasks are created (pending concurrent triage resolution):

1. Add `ai-cve-triaged` label to TC-8020
2. Post summary comment to TC-8020 with:
   - Version impact table
   - Affects Versions correction (RHTPA 2.0.0 replaced with RHTPA 2.2.0, 2.2.1, 2.2.2)
   - Links to all remediation tasks created
   - @mention of the issue reporter
   - Comment Footnote per shared/comment-footnote.md (skill: triage-security)
3. Transition TC-8020 to In Progress

## Key Findings

- The PSIRT-assigned Affects Version (RHTPA 2.0.0) is incorrect and must be corrected to RHTPA 2.2.0, 2.2.1, 2.2.2.
- The fix was already picked up in versions 2.2.3+ (build tags v0.4.11+, shipping quinn-proto 0.11.14).
- Both the 2.1.x and 2.2.x streams are affected, requiring cross-stream impact handling (Case A).
- A concurrent triage on the same component (TC-8019, In Progress) blocks immediate task creation until the engineer makes a choice. This is the critical gate before any Jira mutations for remediation.
