# Triage Outcome -- TC-8002 (CVE-2026-28940)

## Decision: Case C -- Close as Not a Bug (Not Affected)

### Rationale

The version impact analysis shows that **no supported versions** ship a vulnerable version of serde_json. All versions across both the 2.1.x and 2.2.x streams ship serde_json >= 1.0.137, which exceeds the fix threshold of 1.0.135. The vulnerability (stack overflow on deeply nested JSON input) was already remediated in serde_json 1.0.135, and the earliest version shipped in any supported product release is 1.0.137.

### Evidence

- CVE-2026-28940 affects serde_json versions **before 1.0.135**
- The minimum serde_json version across all supported product versions is **1.0.137** (in stream 2.1.x, versions 2.1.0 and 2.1.1)
- The issue-scoped stream (2.2.x) ships serde_json **1.0.138-1.0.139**, all above the fix threshold
- Lock file evidence confirms every pinned source commit includes a patched serde_json version

### VEX Justification

**Vulnerable Code not Present** -- the vulnerable version of serde_json (< 1.0.135) is not shipped in any supported product version. All versions include the fix (configurable recursion limit).

Note: If the VEX Justification custom field (customfield_12345) is configured, it should be set to "Vulnerable Code not Present" (alternatively "Component not Present" could apply if the specific vulnerable code path was removed, but since the package is present at a fixed version, "Vulnerable Code not Present" is the more precise justification).

### Proposed Jira Actions

The following actions would be performed on TC-8002 (each requiring engineer confirmation per skill guardrails):

1. **Assign and transition** (Step 0.7):
   - Assign TC-8002 to the current user
   - Transition from "New" to "Assigned" status

2. **Affects Versions correction** (Step 3):
   - Current: `RHTPA 2.2.0`
   - Proposed: Remove all Affects Versions (no versions are actually affected)
   - Alternatively, retain RHTPA 2.2.0 as the PSIRT-claimed scope for audit trail purposes since the issue will be closed immediately

3. **Add triage comment** (Post-Triage Summary):
   Post a summary comment to TC-8002 documenting:
   - The version impact table showing NO for all versions
   - The lock file evidence (serde_json 1.0.137-1.0.139 across all versions)
   - The close rationale: all supported versions ship a fixed serde_json version
   - @mention of the issue reporter (PSIRT analyst)

4. **Close the issue** (Case C):
   - Transition TC-8002 to "Closed"
   - Resolution: "Not a Bug"
   - Set VEX Justification field (customfield_12345): "Vulnerable Code not Present"

5. **Add label** (Post-Triage Summary):
   - Add `ai-cve-triaged` label to TC-8002

### Cross-Stream Impact

Since the issue is scoped to stream 2.2.x (`[rhtpa-2.2]` suffix), the skill would also check stream 2.1.x for impact (Case A check). However, since **no versions in any stream are affected**, there is no cross-stream impact to report and no remediation tasks to create for any stream.

### No Remediation Tasks Required

No remediation tasks are created because the vulnerability does not affect any supported version. The dependency was already at a fixed version across all product releases.
