# Triage Outcome — TC-8002

## Decision: Case C — No Supported Versions Affected

CVE-2026-28940 (serde_json < 1.0.135) does **not** affect any supported product version. Every version in both the 2.1.x and 2.2.x streams ships serde_json >= 1.0.137, which is above the fix threshold of 1.0.135.

### Recommendation

**Close TC-8002 as "Not a Bug" (not affected).**

The vulnerable version of serde_json is not present in any supported release. The fix (1.0.135) was already included before the earliest supported version (2.1.0) was built.

### VEX Justification

Set VEX Justification custom field (`customfield_12345`) to: **Component not Present**

Rationale: The lock file analysis shows the vulnerable package version (serde_json < 1.0.135) is not included in any supported version. All versions ship serde_json 1.0.137 or later, which is outside the affected range.

## Proposed Jira Actions

The following Jira mutations would be performed (each requiring engineer confirmation in interactive mode):

### 1. Assign and Transition (Step 0.8)

- **Assign** TC-8002 to the current user
- **Transition** TC-8002 from New to Assigned

### 2. Affects Versions Correction (Step 3)

- **Current**: RHTPA 2.2.0
- **Proposed**: Remove all Affects Versions (no versions are affected)
- **Rationale**: PSIRT assigned RHTPA 2.2.0, but lock file analysis confirms serde_json 1.0.138 is shipped in 2.2.0, which is above the fix threshold of 1.0.135. No version is actually affected.
- **Comment**: "Corrected Affects Versions: [RHTPA 2.2.0] -> [] (none affected). Based on lock file analysis at pinned commits from security-matrix.md. All supported versions ship serde_json >= 1.0.137, which is above the fix threshold of 1.0.135. Scoped to stream 2.2.x per issue suffix."

### 3. Duplicate/Sibling Check (Step 4)

- Search for sibling Vulnerability issues with label CVE-2026-28940
- If siblings exist in 2.1.x stream, they would also show no affected versions
- No cross-CVE overlap check (Upstream Affected Component field not configured)
- No preemptive task reconciliation needed (no remediation tasks to create)

### 4. Version Lifecycle Check (Step 5)

- Verify 2.2.x versions are still within support lifecycle via Product pages URL
- Even if supported, outcome does not change since no versions are affected

### 5. Already Fixed Check (Step 6)

- Check resolved siblings -- not directly applicable since the vulnerability was never present in supported versions (the dependency was already at a patched version)

### 6. Close as Not a Bug (Step 8, Case C)

After engineer confirmation, execute in order:

a. **Add comment** to TC-8002:

> No supported versions ship a vulnerable version of serde_json.
>
> Version impact analysis:
>
> | Version | serde_json | Affected? |
> |---------|-----------|-----------|
> | 2.1.0 | 1.0.137 | NO |
> | 2.1.1 | 1.0.137 | NO |
> | 2.2.0 | 1.0.138 | NO |
> | 2.2.1 | 1.0.138 | NO |
> | 2.2.2 | 1.0.138 | NO (retag of 2.2.1) |
> | 2.2.3 | 1.0.139 | NO |
> | 2.2.4 | 1.0.139 | NO |
>
> All supported versions ship serde_json 1.0.137+ which is outside the affected range (< 1.0.135). The vulnerability was already fixed before any currently supported version was released.

b. **Set VEX Justification** (`customfield_12345`): "Component not Present"

c. **Transition** TC-8002 to Closed with resolution "Not a Bug"

d. **Add label**: `ai-cve-triaged`

### 7. Post-Triage Summary (final comment)

Post a summary comment to TC-8002 documenting:

> **Triage Summary for CVE-2026-28940 (serde_json)**
>
> - **Outcome**: Closed as Not a Bug -- no supported versions affected
> - **Fix threshold**: serde_json 1.0.135
> - **Version impact**: All 7 supported versions (2.1.0, 2.1.1, 2.2.0-2.2.4) ship serde_json >= 1.0.137
> - **Affects Versions correction**: RHTPA 2.2.0 removed (not affected)
> - **VEX Justification**: Component not Present
> - **Remediation tasks created**: None (not needed)
> - **Stream scope**: 2.2.x (per issue suffix [rhtpa-2.2]); cross-stream analysis shows 2.1.x is also not affected
>
> @reporter (PSIRT analyst who created this issue)

## Steps Skipped

| Step | Reason |
|------|--------|
| Step 1.7 (Embargo Check) | CVSS 5.3 (Medium) below threshold; no embargo policy URL configured |
| Step 4.3 (Cross-CVE Overlap) | Upstream Affected Component field not configured |
| Step 7 (Concurrent Triage) | Upstream Affected Component field not configured |
| Step 7.5 (Release Jira Orchestration) | No remediation tasks to create (Case C) |
| Step 8 Case A/B (Remediation) | No affected versions -- Case C applies |

## Key Evidence

- All lock file versions confirmed via `git show <tag>:Cargo.lock` (simulated from mock data)
- Minimum serde_json version across all tags: **1.0.137** (at v0.3.8 / v0.3.12)
- Fix threshold: **1.0.135**
- Margin: all versions exceed the fix threshold by at least 2 patch versions
- The vulnerability (stack overflow on deeply nested JSON input) was resolved in serde_json 1.0.135 with a configurable recursion limit defaulting to 128 levels
