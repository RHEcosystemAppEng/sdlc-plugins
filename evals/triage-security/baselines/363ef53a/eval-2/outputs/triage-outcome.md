# Triage Outcome -- TC-8002 (CVE-2026-28940)

## Decision: Case C -- Close as Not a Bug (not affected)

The version impact analysis shows that **no supported versions** ship a vulnerable
version of serde_json. All versions across both the 2.1.x and 2.2.x streams ship
serde_json >= 1.0.137, which is above the CVE fix threshold of 1.0.135.

The issue is scoped to the 2.2.x stream. Within that stream, the earliest version
(2.2.0, tag v0.4.5) ships serde_json 1.0.138 and the latest (2.2.4, tag v0.4.12)
ships 1.0.139. Neither is within the affected range (< 1.0.135).

The 2.1.x stream (out of scope for this issue but checked for completeness) also
ships serde_json 1.0.137 across all versions -- similarly not affected.

## Proposed Jira Actions

### 1. Affects Versions Correction (Step 3)

- **Current**: RHTPA 2.2.0
- **Proposed**: Remove RHTPA 2.2.0 (no versions in the 2.2.x stream are affected)
- **Rationale**: PSIRT assigned RHTPA 2.2.0 based on scan-time component presence,
  but lock file analysis confirms serde_json 1.0.138 is shipped in 2.2.0, which is
  already patched.
- **Action**: Clear Affects Versions (set to empty) or retain RHTPA 2.2.0 for
  traceability while closing. Engineer decision required.

### 2. Close Issue (Step 8, Case C)

- **Transition**: Close TC-8002 with resolution **"Not a Bug"**
- **VEX Justification**: Set `customfield_12345` to **"Vulnerable Code not Present"**
  - Rationale: serde_json is present in the dependency tree, but the shipped version
    (>= 1.0.137) does not contain the vulnerable code. The fix (recursion limit) was
    already included in the shipped versions.
- **Comment to post**:

  > No supported versions ship a vulnerable version of serde_json.
  > Version impact analysis:
  >
  > | Version | serde_json | Affected? |
  > |---------|-----------|-----------|
  > | 2.2.0 | 1.0.138 | NO |
  > | 2.2.1 | 1.0.138 | NO |
  > | 2.2.2 | -- | NO (retag of 2.2.1) |
  > | 2.2.3 | 1.0.139 | NO |
  > | 2.2.4 | 1.0.139 | NO |
  >
  > All supported versions ship serde_json >= 1.0.137 which is outside the
  > affected range (< 1.0.135). Closing as Not a Bug.
  >
  > VEX Justification: Vulnerable Code not Present
  >
  > [Comment Footnote]

### 3. Add Triage Label

- **Action**: Add label `ai-cve-triaged` to TC-8002
- **Purpose**: Marks the issue as triaged to prevent re-processing in discovery mode

### 4. Cross-Stream Impact

- Not applicable. Since no versions are affected in any stream (2.1.x and 2.2.x
  both ship patched versions), there is no cross-stream remediation needed (Case A
  does not apply).

### 5. Remediation Tasks

- **None required.** No remediation tasks are created because no supported versions
  are affected. This is a clean Case C closure.

## Steps Not Applicable

- **Step 4 (Duplicate/Sibling Check)**: Would be performed via JQL in a live triage.
  Not simulated here, but outcome does not change -- even if sibling issues exist for
  the 2.1.x stream, they would also result in Case C closure since 2.1.x versions are
  similarly unaffected.
- **Step 5 (Version Lifecycle Check)**: Not needed since no versions are affected.
- **Step 6 (Already Fixed Check)**: Not applicable -- the product never shipped the
  vulnerable version, so this is "not affected" rather than "already fixed."
- **Step 7 (Concurrent Triage Detection)**: Upstream Affected Component custom field
  is not configured in the mock Security Configuration, so this step would be skipped.
- **Step 7.5 (Release Jira Orchestration)**: Not applicable -- no remediation tasks
  to link to a release structure.
