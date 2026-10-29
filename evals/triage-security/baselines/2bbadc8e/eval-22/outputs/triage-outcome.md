# Triage Outcome -- TC-8021 (CVE-2026-31812 / quinn-proto)

## Configuration Validated (Step 0)

| Configuration Item | Value |
|--------------------|-------|
| Project key | TC |
| Cloud ID | 2b9e35e3-6bd3-4cec-b838-f4249ee02432 |
| Jira version prefix | RHTPA |
| Vulnerability issue type ID | 10024 |
| Product pages URL | https://access.example.com/product-life-cycle/rhtpa |
| Component label pattern | pscomponent: |
| VEX Justification custom field | customfield_12345 |
| Upstream Affected Component custom field | customfield_10632 |
| Version Streams | 2.1.x (rhtpa-release.0.3.z), 2.2.x (rhtpa-release.0.4.z) |
| Source Repositories | rhtpa-backend (upstream) |

All required Security Configuration sections are present. Triage can proceed.

## Matrix Staleness Check (Step 0.3)

- Matrix timestamp: `2026-06-28T10:00:00Z`
- Current date: 2026-10-29
- Age: approximately 123 days (exceeds 14-day threshold)
- **Warning**: The security matrix is significantly stale. In a live triage, the engineer would be prompted to refresh, proceed, or stop.
- For this evaluation: proceeding with current matrix data.

## Issue Status (Step 0.8)

- Current status: **New** -- proceed with full triage (default path)
- PROPOSAL: Assign to current user and transition to Assigned status

## Version Impact Summary (Step 2)

### Scoped stream: 2.2.x

| Version | quinn-proto | Affected? |
|---------|-------------|-----------|
| RHTPA 2.2.0 | 0.11.9 | YES |
| RHTPA 2.2.1 | 0.11.12 | YES |
| RHTPA 2.2.2 | 0.11.12 (retag of 2.2.1) | YES |
| RHTPA 2.2.3 | 0.11.14 | NO (fixed) |
| RHTPA 2.2.4 | 0.11.14 | NO (fixed) |

### Cross-stream: 2.1.x

| Version | quinn-proto | Affected? |
|---------|-------------|-----------|
| RHTPA 2.1.0 | 0.11.9 | YES |
| RHTPA 2.1.1 | 0.11.9 | YES |

### Upstream Fix Status (Step 2.5)

The fix is already available upstream. Build tags v0.4.11 and v0.4.12 (corresponding to RHTPA 2.2.3 and 2.2.4) already ship quinn-proto 0.11.14 (the fixed version). The upstream fix PR is quinn-rs/quinn#2048. This means remediation uses the **dependency bump** variant (not upstream backport).

## Affects Versions Correction (Step 3)

- **Current (PSIRT-assigned)**: RHTPA 2.0.0
- **Proposed**: RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2
- **Rationale**: "RHTPA 2.0.0" does not correspond to any configured version stream. Lock file analysis at pinned commits confirms that versions 2.2.0, 2.2.1, and 2.2.2 within the issue's scoped stream (2.2.x) ship quinn-proto versions below the fix threshold of 0.11.14. Versions 2.2.3 and 2.2.4 are excluded because they already ship the fixed version.
- PROPOSAL: Update Affects Versions from [RHTPA 2.0.0] to [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2] with engineer confirmation.
- PROPOSAL: Post Affects Versions correction comment documenting the change and lock file evidence.

## Duplicate/Sibling Check (Step 4)

- Step 4.1 (Same-stream duplicates): No simulated sibling data provided; assuming no same-stream duplicates found.
- Step 4.2 (Cross-stream coordination): No simulated sibling data provided; assuming no existing sibling CVE issues found for the 2.1.x stream.
- Step 4.3 (Cross-CVE overlap): The Upstream Affected Component custom field is configured (customfield_10632) with value `quinn-proto`. No simulated overlap data provided; assuming no covering remediation task found for quinn-proto from a different CVE.
- Step 4.4 (Preemptive task reconciliation): No simulated preemptive task data provided; assuming no existing preemptive remediation tasks found.

## Version Lifecycle Check (Step 5)

No simulated lifecycle data provided. Assuming all affected versions (2.2.0, 2.2.1, 2.2.2) are within active support lifecycle per the product pages URL.

## Already Fixed Check (Step 6)

No resolved sibling Vulnerability issues found. The fix is not already tracked by another resolved issue. Proceed to remediation.

## Concurrent Triage Detection (Step 7)

- Upstream Affected Component field: customfield_10632 = `quinn-proto`
- JQL search for in-progress triages with the same component returned **zero results**
- No concurrent triages detected. Proceeding to remediation.

## Triage Decision

### Classification: Case A + Case B

This issue triggers **both** Case A (cross-stream impact) and Case B (affected versions requiring remediation).

**Case A applies** because:
- The issue is scoped to stream 2.2.x (per summary suffix `[rhtpa-2.2]`)
- The 2.1.x stream is also affected (both versions 2.1.0 and 2.1.1 ship quinn-proto 0.11.9)
- Case A creates proactive/preemptive remediation tasks for the 2.1.x stream (if no sibling CVE Jira exists for that stream)

**Case B applies** because:
- Within the scoped 2.2.x stream, versions 2.2.0, 2.2.1, and 2.2.2 are affected
- Ecosystem is Cargo (source dependency) with fix already available upstream
- This produces 2 tasks: dependency bump + downstream propagation

**Case C does NOT apply** because supported versions within the scoped stream are affected.

### Proposed Jira Mutations (all require engineer confirmation)

#### 1. Assignment and Status Transition (Step 0.8)
- PROPOSAL: Assign TC-8021 to current user
- PROPOSAL: Transition TC-8021 from New to Assigned

#### 2. Affects Versions Correction (Step 3)
- PROPOSAL: Update Affects Versions: [RHTPA 2.0.0] --> [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]
- PROPOSAL: Post correction comment with lock file evidence

#### 3. Cross-Stream Impact Comment (Case A)
- PROPOSAL: Post comment on TC-8021:
  "Cross-stream impact: quinn-proto < 0.11.14 also affects stream 2.1.x (versions 2.1.0, 2.1.1) based on lock file analysis. These streams are tracked by companion issues (see Related links) or may require separate PSIRT triage."

#### 4. Preemptive Remediation for 2.1.x Stream (Case A)

If no sibling CVE Jira exists for the 2.1.x stream, create preemptive remediation tasks:

- PROPOSAL: Create preemptive Task: "Bump quinn-proto to >= 0.11.14 in rhtpa-backend (rhtpa-2.1) [CVE-2026-31812]"
  - Labels: security-preemptive, CVE-2026-31812, ai-generated-jira
  - Link type: Related to TC-8021
  - Ecosystem: Cargo -- dependency bump variant
- PROPOSAL: Create preemptive Task: "Propagate quinn-proto fix to rhtpa-release.0.3.z (rhtpa-2.1) [CVE-2026-31812]"
  - Labels: security-preemptive, CVE-2026-31812, ai-generated-jira
  - Link type: Related to TC-8021
  - Blocked by the upstream bump task (Blocks link)

#### 5. Remediation Tasks for 2.2.x Stream (Case B)

Since the upstream fix is already available (quinn-proto 0.11.14 ships in builds v0.4.11+), use the dependency bump variant:

- PROPOSAL: Create Task: "Bump quinn-proto to >= 0.11.14 in rhtpa-backend (rhtpa-2.2) [CVE-2026-31812]"
  - Issue type: Task
  - Labels: CVE-2026-31812, ai-generated-jira
  - Link: Depend from TC-8021 to this task
  - Description: Per task-description-template.md, including:
    - CVE reference and fix threshold
    - Current version in affected builds (0.11.9 / 0.11.12)
    - Target version: >= 0.11.14
    - Implementation: `cargo update -p quinn-proto` on release/0.4.z branch
    - Upstream fix PR reference: quinn-rs/quinn#2048
    - Coordination guidance for upstream deployment context

- PROPOSAL: Create Task: "Propagate quinn-proto fix to rhtpa-release.0.4.z (rhtpa-2.2) [CVE-2026-31812]"
  - Issue type: Task
  - Labels: CVE-2026-31812, ai-generated-jira
  - Link: Depend from TC-8021 to this task
  - Blocked by the upstream bump task (Blocks link)
  - Description: Per task-description-template.md, including:
    - Downstream propagation of the quinn-proto bump
    - Update artifacts.lock.yaml to reference the new build tag
    - Affects versions: RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2

#### 6. Release Jira Orchestration (Step 7.5)
- PROPOSAL: Search for existing release Epic matching "RHTPA 2.2.* Release Tasks"
- PROPOSAL: If none found, create release Epic "RHTPA 2.2.5 Release Tasks" (next patch bump after 2.2.4) -- requires engineer confirmation of version
- PROPOSAL: Find or create release Task "RHTPA 2.2.5 CVE triage" as child of the release Epic
- PROPOSAL: Link remediation Tasks to release Task (Blocks)
- PROPOSAL: Link TC-8021 to release Task (Related)

#### 7. Post-Triage Actions
- PROPOSAL: Add label `ai-cve-triaged` to TC-8021
- PROPOSAL: Post summary comment on TC-8021 documenting:
  - Version impact table
  - Affects Versions correction
  - Remediation tasks created (dependency bump + downstream propagation for 2.2.x)
  - Preemptive tasks created for 2.1.x (if applicable)
  - Cross-stream impact notice
  - Release Jira references
  - @mention of the issue reporter (PSIRT analyst)
  - Comment Footnote per shared/comment-footnote.md

## Pre-Creation Checklist

- [x] **Task count per stream**: 2 tasks for 2.2.x stream (dependency bump + downstream propagation) -- matches Cargo source dependency classification
- [x] **Cross-stream coverage**: 2.1.x stream covered by preemptive tasks (if no sibling CVE Jira exists) -- Case A
- [x] **Link types**: "Depend" for tasks linked to TC-8021 (own CVE Jira); "Related" for preemptive tasks linked to TC-8021 (another stream's CVE); "Blocks" for upstream bump --> downstream propagation within a stream
- [x] **Preemptive labels**: Tasks for 2.1.x carry `security-preemptive` label
- [x] **Coordination guidance**: Each task includes upstream deployment context guidance
- [x] **Release Jira linking**: Remediation Tasks linked to release Task (Blocks); CVE linked to release Task (Related)
- [x] **Dedup consistency**: No dedup detected in Step 7.5.3 (no prior remediation tasks covering quinn-proto)
