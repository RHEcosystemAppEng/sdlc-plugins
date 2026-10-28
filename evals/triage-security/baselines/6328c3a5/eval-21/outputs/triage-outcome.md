# Triage Outcome for TC-8020

## Issue Summary

- **Issue**: TC-8020
- **CVE**: CVE-2026-31812
- **Library**: quinn-proto
- **Fix threshold**: 0.11.14
- **CVSS**: 7.5 (High)
- **Stream scope**: 2.2.x (from summary suffix `[rhtpa-2.2]`)

## Version Impact Summary

### In-scope stream (2.2.x)

| Version | quinn-proto | Affected? |
|---------|-------------|-----------|
| 2.2.0 | 0.11.9 | YES |
| 2.2.1 | 0.11.12 | YES |
| 2.2.2 | (retag of 2.2.1) | YES |
| 2.2.3 | 0.11.14 | NO |
| 2.2.4 | 0.11.14 | NO |

### Out-of-scope stream (2.1.x -- triggers Case A cross-stream notice)

| Version | quinn-proto | Affected? |
|---------|-------------|-----------|
| 2.1.0 | 0.11.9 | YES |
| 2.1.1 | 0.11.9 | YES |

## Triage Decision Path

### Step 0 -- Configuration Validated
All required Security Configuration sections are present in the project
CLAUDE.md: Product Lifecycle, Version Streams (2.1.x, 2.2.x), and Source
Repositories.

### Step 1 -- Data Extraction Complete
CVE data parsed successfully. Stream scope resolved to 2.2.x. Ecosystem
detected as Cargo (source dependency). Upstream Affected Component
(customfield_10632) is set to `quinn-proto`.

### Step 2 -- Version Impact Analysis Complete
Three versions in the 2.2.x stream are affected (2.2.0, 2.2.1, 2.2.2).
Two versions are not affected (2.2.3, 2.2.4 ship the fixed 0.11.14).
The 2.1.x stream is also affected but is out of scope for this issue.

### Step 3 -- Affects Versions Correction Required
- Current: RHTPA 2.0.0 (incorrect -- no 2.0.x stream exists)
- Proposed: RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2
- Rationale: Lock file evidence at pinned commits shows quinn-proto versions
  below the fix threshold (0.11.14) for these product versions. RHTPA 2.0.0
  does not correspond to any configured version stream.

### Step 4 -- Duplicate/Sibling/Overlap Check
- Sibling search: search for other Vulnerability issues with label
  CVE-2026-31812. Classification would depend on results.
- Cross-CVE overlap (Step 4.3): Upstream Affected Component field is
  configured, so overlap detection proceeds. Search for other Vulnerability
  issues with customfield_10632 ~ 'quinn-proto'.
- Preemptive reconciliation (Step 4.4): search for existing preemptive
  tasks with labels 'security-preemptive' and 'CVE-2026-31812'.

### Step 5 -- Version Lifecycle Check
Check product pages URL (https://access.example.com/product-life-cycle/rhtpa)
for lifecycle status of affected versions.

### Step 6 -- Already Fixed Check
Cross-reference any resolved sibling Vulnerability issues for CVE-2026-31812.

### Step 7 -- Concurrent Triage Detection: BLOCKED

**Concurrent triage detected.** TC-8019 is actively being triaged by
`engineer-b@example.com` (status: In Progress) and affects the same
upstream component (`quinn-proto`).

The engineer must choose one of three options before proceeding:
1. **Wait** -- pause until TC-8019 completes
2. **Skip** -- skip remediation task creation
3. **Proceed** -- create tasks with `concurrent-triage-overlap` label

**Triage is gated at Step 7 pending the engineer's decision.**

## Planned Remediation (contingent on Step 7 resolution)

If the engineer chooses to proceed (Option 3) or waits and re-runs:

### Case A -- Cross-Stream Impact (scoped issue)
Since TC-8020 is scoped to 2.2.x but stream 2.1.x is also affected,
a cross-stream impact comment would be posted:

> Cross-stream impact: quinn-proto versions before 0.11.14 also affects
> stream 2.1.x based on lock file analysis. Stream 2.1.x is tracked by
> companion issues (see Related links) or may require separate PSIRT triage.

If no sibling CVE Jira exists for 2.1.x, proactive (preemptive)
remediation tasks would be created for that stream with the
`security-preemptive` label and "Related" link type.

### Case B -- Remediation Task Creation (for 2.2.x)
Since versions 2.2.0, 2.2.1, and 2.2.2 are affected in the in-scope
stream, and the upstream fix is already available (versions 2.2.3+ ship
the fixed 0.11.14), the remediation approach is:

**Ecosystem**: Cargo (source dependency, fix available upstream)
**Task count**: 2 tasks for the 2.2.x stream

1. **Dependency bump task**: Bump quinn-proto to >= 0.11.14 on the
   upstream branch `release/0.4.z` in the backend repository. Since
   versions 2.2.3 and 2.2.4 already ship 0.11.14, the upstream
   branch already has the fix. This task verifies the fix is on the
   correct release branch.

2. **Downstream propagation task**: Update the Konflux release repo
   (`rhtpa-release.0.4.z`) to reference the source tag containing
   the quinn-proto fix. This task is blocked by the dependency bump
   task (Blocks link type).

Both tasks would be linked to TC-8020 with "Depend" link type and
linked to the release Task (from Step 7.5) with "Blocks" link type.

### Post-Triage Actions (after remediation)
- Add `ai-cve-triaged` label to TC-8020
- Post summary comment with version impact table, Affects Versions
  correction, remediation task links, and reporter @mention
- The summary comment includes the Comment Footnote

## Current Status

**Triage is incomplete -- gated at Step 7 (Concurrent Triage Detection).**

The concurrent triage on TC-8019 for the same upstream component
(quinn-proto) must be resolved before remediation tasks can be created.
The engineer must select Wait, Skip, or Proceed to continue.
