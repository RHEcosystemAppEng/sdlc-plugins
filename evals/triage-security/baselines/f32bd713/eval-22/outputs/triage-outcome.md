# Triage Outcome for TC-8021

## CVE Summary

- **CVE**: CVE-2026-31812
- **Library**: quinn-proto
- **Fix threshold**: 0.11.14
- **Ecosystem**: Cargo (source dependency)
- **Issue scope**: Stream 2.2.x (from summary suffix `[rhtpa-2.2]`)
- **CVSS**: 7.5 (High)

## Version Impact Summary

### Stream 2.2.x (in scope)

| Version | quinn-proto | Affected? |
|---------|-------------|-----------|
| 2.2.0 | 0.11.9 | YES |
| 2.2.1 | 0.11.12 | YES |
| 2.2.2 | 0.11.12 (retag of 2.2.1) | YES |
| 2.2.3 | 0.11.14 | NO |
| 2.2.4 | 0.11.14 | NO |

### Stream 2.1.x (cross-stream)

| Version | quinn-proto | Affected? |
|---------|-------------|-----------|
| 2.1.0 | 0.11.9 | YES |
| 2.1.1 | 0.11.9 | YES |

## Step-by-Step Triage Decisions

### Step 3 -- Affects Versions Correction

**Required.** PSIRT assigned `RHTPA 2.0.0`, which does not correspond to any configured version stream. The correct Affects Versions, scoped to the 2.2.x stream, are:

- `RHTPA 2.2.0`
- `RHTPA 2.2.1`
- `RHTPA 2.2.2`

Versions 2.2.3 and 2.2.4 are excluded because they ship quinn-proto 0.11.14, which is at or above the fix threshold.

### Step 4 -- Duplicate, Sibling, Overlap, and Reconciliation Check

#### Step 4.1/4.2 -- Sibling Detection

A JQL search for sibling Vulnerability issues with the CVE-2026-31812 label would be performed. Since this is simulated, we assume no siblings found (no other CVE-2026-31812 issues exist for other streams yet).

#### Step 4.3 -- Cross-CVE Overlap Detection

The Upstream Affected Component custom field (customfield_10632) is configured and set to `quinn-proto`. A search for other Vulnerability issues with the same component value would be performed. Assuming no covering remediation tasks are found from other CVEs, no overlap exists. Proceeding to Step 4.4.

#### Step 4.4 -- Preemptive Task Reconciliation

A search for existing preemptive tasks matching CVE-2026-31812 and the 2.2.x stream would be performed. Assuming no preemptive tasks exist, proceed to Step 5.

### Step 5 -- Version Lifecycle Check

Product pages URL: `https://access.example.com/product-life-cycle/rhtpa`

Assuming both 2.1.x and 2.2.x streams are within active support lifecycle. All affected versions are supported. Proceed to Step 6.

### Step 6 -- Already Fixed Check

No resolved sibling Vulnerability issues found for CVE-2026-31812 (no siblings detected in Step 4). Proceed to Step 7.

### Step 7 -- Concurrent Triage Detection

See `concurrent-triage.md` for full analysis. **Result: No concurrent triages detected.** Proceed to Step 8.

### Step 7.5 -- Release Jira Orchestration

For each affected stream within scope (2.2.x), find or create the release Jira structure:

1. Search for an existing release Epic matching `"RHTPA 2.2.* Release Tasks"`
2. If found, reuse it; if not, propose creation (e.g., `RHTPA 2.2.5 Release Tasks` based on next patch bump after 2.2.4)
3. Find or create a release Task `"RHTPA 2.2.5 CVE triage"` as a child of the Epic
4. Cross-CVE dedup check: inspect the release Task's Blocks links for existing remediation tasks covering quinn-proto -- assuming none found

### Step 8 -- Remediation Decision

#### Determination: Case A + Case B

**Case A applies** (cross-stream impact): The issue is scoped to 2.2.x, but the version impact analysis reveals that the 2.1.x stream is also affected (all versions ship quinn-proto 0.11.9, which is below the 0.11.14 fix threshold). A cross-stream impact comment would be posted to TC-8021.

**Case B applies** (affected versions exist): Within the 2.2.x scope, versions 2.2.0, 2.2.1, and 2.2.2 are affected. Remediation tasks are needed.

Case C does NOT apply -- supported versions are affected.

#### Case A: Cross-Stream Impact

Post a cross-stream impact comment on TC-8021:

> Cross-stream impact: quinn-proto < 0.11.14 also affects stream 2.1.x based on lock file analysis. Stream 2.1.x versions 2.1.0 and 2.1.1 both ship quinn-proto 0.11.9. These streams are tracked by companion issues (see Related links) or may require separate PSIRT triage.

Since no existing CVE Jira exists for 2.1.x (no sibling found in Step 4), create **preemptive remediation tasks** for the 2.1.x stream:
- 2 tasks (Cargo source dependency): preemptive dependency bump + preemptive downstream propagation
- Labels include `security-preemptive` alongside standard labels
- Link type is "Related" (not "Depend") to TC-8021

#### Case B: Remediation Tasks for 2.2.x

Since quinn-proto is a **Cargo** ecosystem (source dependency) and the upstream fix (0.11.14) is available (versions 2.2.3+ already ship it, and the upstream fix PR quinn-rs/quinn#2048 exists), the remediation uses the **dependency bump** variant:

**Task 1 -- Dependency bump (upstream source repo)**:
- Summary: `CVE-2026-31812: bump quinn-proto to 0.11.14 in rhtpa-backend (rhtpa-2.2)`
- Type: Task
- Labels: `CVE-2026-31812`, `security-remediation`, `ai-generated-jira`
- Description: Per task-description-template.md format, specifying:
  - Bump quinn-proto from current version to >= 0.11.14 via `cargo update -p quinn-proto`
  - Target branch: `release/0.4.z`
  - Fix threshold: 0.11.14
  - Affected versions: 2.2.0, 2.2.1, 2.2.2
  - Upstream fix PR reference: quinn-rs/quinn#2048
- Link: Depend from TC-8021 to this task
- Link: Blocks from this task to the release Task (Step 7.5)

**Task 2 -- Downstream propagation (Konflux release repo)**:
- Summary: `CVE-2026-31812: propagate quinn-proto fix to rhtpa-release.0.4.z (rhtpa-2.2)`
- Type: Task
- Labels: `CVE-2026-31812`, `security-remediation`, `ai-generated-jira`
- Description: Per task-description-template.md format, specifying:
  - Propagate the upstream fix to the Konflux release repo
  - Blocked by Task 1 (upstream bump must land first)
  - Target repo: rhtpa-release.0.4.z
- Link: Depend from TC-8021 to this task
- Link: Blocks from Task 1 to this task (upstream blocks downstream)
- Link: Blocks from this task to the release Task (Step 7.5)

#### Post-creation Linking

- Each remediation Task is linked to the release Task (Blocks)
- TC-8021 is linked to the release Task (Related)

### Post-Triage Summary

After all triage actions complete:

1. **Add label**: `ai-cve-triaged` to TC-8021
2. **Post summary comment** to TC-8021 documenting:
   - Version impact table (showing 2.2.0/2.2.1/2.2.2 affected, 2.2.3/2.2.4 not affected)
   - Affects Versions correction: RHTPA 2.0.0 -> RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2
   - Triage outcome: remediation tasks created (2 for 2.2.x scope, 2 preemptive for 2.1.x)
   - Links to all remediation tasks
   - Cross-stream impact on 2.1.x noted
   - Release Jira references
   - @mention of the issue reporter
   - Comment Footnote per shared/comment-footnote.md

## Pre-Creation Checklist

- [x] **Task count per stream**: Cargo (source dependency) = 2 tasks per stream (dependency bump + downstream propagation). 2 tasks for 2.2.x, 2 preemptive tasks for 2.1.x.
- [x] **Cross-stream coverage**: 2.1.x (outside issue scope) has no sibling CVE Jira, so preemptive tasks are created.
- [x] **Link types**: "Depend" for tasks linked to TC-8021 (their own CVE); "Related" for preemptive tasks linked to TC-8021 (another stream's CVE); "Blocks" for upstream -> downstream within a stream.
- [x] **Preemptive labels**: 2.1.x tasks carry `security-preemptive` label.
- [x] **Coordination guidance**: Each task includes guidance based on the `upstream` deployment context (default).
- [x] **Release Jira linking**: Non-preemptive remediation Tasks linked to release Task (Blocks); CVE linked to release Task (Related).
- [x] **Dedup consistency**: No streams marked as dedup'd in Step 7.5.3 -- all streams get new remediation tasks.
