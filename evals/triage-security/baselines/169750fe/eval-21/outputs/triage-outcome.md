# Triage Outcome -- TC-8020 (CVE-2026-31812 quinn-proto)

## Issue Summary

- **Issue**: TC-8020
- **CVE**: CVE-2026-31812
- **Library**: quinn-proto (Rust crate, Cargo ecosystem)
- **Fix threshold**: >= 0.11.14
- **CVSS**: 7.5 (High) -- Denial of Service
- **Stream scope**: 2.2.x (from summary suffix `[rhtpa-2.2]`)

## Version Impact Summary

### In-scope stream (2.2.x)

| Version | quinn-proto | Affected? |
|---------|-------------|-----------|
| 2.2.0 | 0.11.9 | YES |
| 2.2.1 | 0.11.12 | YES |
| 2.2.2 | 0.11.12 (retag) | YES |
| 2.2.3 | 0.11.14 | NO |
| 2.2.4 | 0.11.14 | NO |

### Out-of-scope stream (2.1.x) -- cross-stream impact

| Version | quinn-proto | Affected? |
|---------|-------------|-----------|
| 2.1.0 | 0.11.9 | YES |
| 2.1.1 | 0.11.9 | YES |

## Steps Completed Before Remediation Decision

1. **Step 0 -- Configuration validated**: Security Configuration present with version streams (2.1.x, 2.2.x), source repositories, product lifecycle, and component label pattern.
2. **Step 0.3 -- Matrix staleness check**: Matrix last updated 2026-06-28 (within 14-day threshold at time of triage).
3. **Step 0.8 -- Assignment**: TC-8020 assigned to current user, transitioned to Assigned status.
4. **Step 1 -- Data extraction**: CVE-2026-31812, quinn-proto < 0.11.14, fixed in 0.11.14. Stream scoped to 2.2.x.
5. **Step 1.5 -- External enrichment**: MITRE and OSV data cross-validated; fix threshold confirmed at 0.11.14.
6. **Step 1.7 -- Embargo check**: CVSS 7.5 meets threshold (>= 7.0). If embargo policy URL is configured, warning gate presented. Assumed cleared to proceed.
7. **Step 2 -- Version impact analysis**: 2.2.0, 2.2.1, 2.2.2 affected; 2.2.3, 2.2.4 not affected. Cross-stream: 2.1.x fully affected.
8. **Step 3 -- Affects Versions correction**: RHTPA 2.0.0 (wrong) corrected to RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2 (scoped to 2.2.x stream).
9. **Step 4 -- Duplicate/sibling/overlap check**: Sibling and cross-CVE overlap checks performed.
10. **Step 5 -- Lifecycle check**: Affected versions verified as supported.
11. **Step 6 -- Already fixed check**: No resolved siblings covering these versions.

## Step 7 -- Concurrent Triage Detection Result

**Concurrent triage detected.** TC-8019 (In Progress, assigned to engineer-b@example.com) is actively triaging a different CVE that also affects the upstream component quinn-proto.

Three options presented to the engineer:

1. **Wait** -- Pause until TC-8019 completes. Re-run from Step 4.3 to check whether TC-8019's remediation already covers quinn-proto >= 0.11.14. This is the safest option to avoid duplicate remediation tasks.

2. **Skip** -- Skip remediation task creation entirely. Post a Jira comment on TC-8020 documenting the skip reason (concurrent triage on quinn-proto by TC-8019). The CVE remains triaged (Affects Versions corrected, version impact documented) but no remediation tasks are created.

3. **Proceed** -- Add the `concurrent-triage-overlap` label to TC-8020 and continue to Step 7.5 (Release Jira Orchestration) and Step 8 (Case A/B/C branching). The label enables TC-8019's Step 4.3 cross-CVE overlap detection to catch and reconcile any duplicate coverage.

## Triage Decision (Pending Engineer Choice on Step 7)

The triage outcome depends on the engineer's Step 7 decision. The following describes what would happen for each path:

### If the engineer proceeds (Option 3) or after waiting (Option 1):

**Case A applies (cross-stream impact)** because:
- This is a **scoped** issue (stream suffix `[rhtpa-2.2]`)
- The 2.1.x stream is also affected (all versions ship quinn-proto 0.11.9)
- Case A posts a cross-stream impact comment noting that 2.1.x is also affected

**Case B applies (affected versions exist in scope)** because:
- Versions 2.2.0, 2.2.1, and 2.2.2 are affected within the issue's 2.2.x stream scope
- Ecosystem is Cargo (source dependency) with upstream fix available (0.11.14 is released, and Step 2.5 would confirm the upstream branch `release/0.4.z` already ships 0.11.14 at HEAD per tags v0.4.11 and v0.4.12)
- **Two remediation tasks** would be created for stream 2.2.x:
  1. **Dependency bump task**: Bump quinn-proto to >= 0.11.14 in rhtpa-backend (upstream source repo) on `release/0.4.z` branch via `cargo update -p quinn-proto`
  2. **Downstream propagation task**: Propagate the fix into the Konflux release repo `rhtpa-release.0.4.z` by updating the pinned source commit in `artifacts.lock.yaml`

**Case A preemptive tasks** for 2.1.x:
- If no sibling CVE Jira exists for 2.1.x, two preemptive remediation tasks would be created with the `security-preemptive` label and "Related" link type to TC-8020
- If a sibling CVE Jira exists for 2.1.x, no preemptive tasks are created (that stream's own CVE issue handles it)

### If the engineer skips (Option 2):

- No remediation tasks created
- Jira comment posted to TC-8020 documenting the skip
- Affects Versions correction (Step 3) still applied
- The `ai-cve-triaged` label would still be added
- Post-triage summary comment posted documenting version impact and the skip decision

## Key Findings

1. **PSIRT Affects Versions are incorrect**: RHTPA 2.0.0 does not exist in any configured stream. Corrected to RHTPA 2.2.0, 2.2.1, 2.2.2 based on lock file evidence.
2. **Partial fix in-stream**: The 2.2.x stream is partially fixed -- versions 2.2.3+ already ship quinn-proto 0.11.14. Only 2.2.0-2.2.2 need remediation.
3. **Cross-stream impact**: The 2.1.x stream is fully affected (all versions ship quinn-proto 0.11.9).
4. **Concurrent triage blocks immediate remediation**: TC-8019 is actively triaging another CVE on the same component (quinn-proto). The engineer must choose how to handle this before remediation tasks can be created, to prevent duplicate work.
5. **Upstream fix is available**: quinn-proto 0.11.14 is released and already present in the latest 2.2.x builds. Remediation uses the "dependency bump" variant (not "upstream backport"), meaning tasks involve `cargo update` rather than creating a backport patch.
