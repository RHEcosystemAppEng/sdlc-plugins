# Triage Outcome for TC-8020

## Triage Decision: Case B (Affected) + Case A (Cross-Stream Impact)

TC-8020 (CVE-2026-31812 / quinn-proto) requires remediation. Some supported versions in the issue's scoped stream (2.2.x) ship vulnerable versions of quinn-proto, and the cross-stream analysis reveals that the 2.1.x stream is also fully affected.

## Version Impact Summary

### In-scope stream: 2.2.x

| Product Version | quinn-proto | Affected? |
|-----------------|-------------|-----------|
| 2.2.0 | 0.11.9 | YES |
| 2.2.1 | 0.11.12 | YES |
| 2.2.2 | 0.11.12 (retag) | YES |
| 2.2.3 | 0.11.14 | NO (fixed) |
| 2.2.4 | 0.11.14 | NO (fixed) |

### Cross-stream: 2.1.x

| Product Version | quinn-proto | Affected? |
|-----------------|-------------|-----------|
| 2.1.0 | 0.11.9 | YES |
| 2.1.1 | 0.11.9 | YES |

## Step 3 -- Affects Versions Correction

**PSIRT assigned**: RHTPA 2.0.0
**Correct Affects Versions** (scoped to 2.2.x stream): RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2

The PSIRT-assigned Affects Version is wrong -- "RHTPA 2.0.0" does not correspond to any configured version stream (there is no 2.0.x stream). Based on lock file evidence, the affected versions within the 2.2.x stream are 2.2.0, 2.2.1, and 2.2.2. Versions 2.2.3 and 2.2.4 ship quinn-proto 0.11.14 (the fixed version) and are not affected.

**PROPOSAL**: Update Affects Versions from `[RHTPA 2.0.0]` to `[RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]` using dynamically discovered Jira version IDs from Step 3.1.

**PROPOSAL**: Post Affects Versions correction comment to TC-8020 documenting the change and lock file evidence.

## Step 4 -- Duplicate, Sibling, Overlap, and Reconciliation Check

- **Step 4.1/4.2 (Sibling detection)**: A JQL search for sibling Vulnerability issues with label CVE-2026-31812 would be performed. Any same-stream siblings would trigger duplicate handling; different-stream siblings would be linked as companions.
- **Step 4.3 (Cross-CVE overlap)**: With customfield_10632 configured and set to `quinn-proto`, a search for other Vulnerability issues with the same upstream component would be performed. If TC-8019 (the concurrent triage) has already created remediation tasks that bump quinn-proto to >= 0.11.14, those would cover this CVE's fix threshold and no new remediation tasks would be needed.
- **Step 4.4 (Preemptive task reconciliation)**: A search for existing preemptive tasks with label `CVE-2026-31812` and `security-preemptive` would be performed.

## Step 5 -- Version Lifecycle Check

A lifecycle check against the Product pages URL (https://access.example.com/product-life-cycle/rhtpa) would be performed to verify that RHTPA 2.2.x and 2.1.x versions are still within their support lifecycle.

## Step 6 -- Already Fixed Check

Resolved sibling issues for CVE-2026-31812 would be checked. If no resolved siblings exist (or if resolved siblings do not cover the affected versions), triage proceeds to Step 7.

## Step 7 -- Concurrent Triage Detection

**Concurrent triage detected.** TC-8019 (In Progress, assigned to engineer-b@example.com) is actively triaging a different CVE that also affects `quinn-proto`. See outputs/concurrent-triage.md for the full analysis.

**PROPOSAL**: If the engineer chooses to proceed (Option 3), add the `concurrent-triage-overlap` label to TC-8020 before continuing to remediation.

## Step 8 -- Remediation (Case B + Case A)

Assuming the engineer proceeds past the concurrent triage gate:

### Case A: Cross-Stream Impact (scoped issue)

The issue is scoped to 2.2.x, but version impact analysis shows stream 2.1.x is also affected (all versions ship quinn-proto 0.11.9, which is below the fix threshold 0.11.14).

**PROPOSAL**: Post cross-stream impact comment to TC-8020:
> Cross-stream impact: quinn-proto < 0.11.14 also affects stream 2.1.x based on lock file analysis. Stream 2.1.x versions (2.1.0, 2.1.1) all ship quinn-proto 0.11.9. These streams are tracked by companion issues (see Related links) or may require separate PSIRT triage.

If no existing CVE Jira covers 2.1.x for this CVE, preemptive remediation tasks would be created for stream 2.1.x with the `security-preemptive` label and "Related" link type to TC-8020.

### Case B: Remediation Tasks for 2.2.x (in-scope stream)

Since quinn-proto is a **Cargo** (source dependency) ecosystem and the fix (0.11.14) is already available (the upstream fix PR quinn-rs/quinn#2048 exists and versions 2.2.3+ already ship the fix), this is the **dependency bump** variant. Two tasks per affected stream:

#### Task 1: Dependency Bump (upstream source repo)

**PROPOSAL**: Create Jira Task:
- **Summary**: `CVE-2026-31812: bump quinn-proto to >= 0.11.14 in rhtpa-backend (rhtpa-2.2)`
- **Issue Type**: Task
- **Labels**: `CVE-2026-31812`, `security`, `ai-generated-jira`
- **Description**: Per task-description-template.md format, including:
  - CVE reference and advisory links
  - Affected version range (< 0.11.14)
  - Target fix version (>= 0.11.14)
  - Lock file evidence showing current version at affected commits
  - Dependency chain information from Step 2.3.5
  - Implementation notes: `cargo update -p quinn-proto` on `release/0.4.z` branch
  - Coordination guidance based on `upstream` deployment context
- **Link**: Depend from TC-8020 to this task

#### Task 2: Downstream Propagation (Konflux release repo)

**PROPOSAL**: Create Jira Task:
- **Summary**: `CVE-2026-31812: propagate quinn-proto fix to rhtpa-release.0.4.z (rhtpa-2.2)`
- **Issue Type**: Task
- **Labels**: `CVE-2026-31812`, `security`, `ai-generated-jira`
- **Description**: Per task-description-template.md format, including:
  - Reference to the upstream bump task (Blocks relationship)
  - Instructions to update artifacts.lock.yaml to pick up the new backend tag
  - Verification steps to confirm quinn-proto >= 0.11.14 in the new build
- **Link**: Depend from TC-8020 to this task; Blocks from upstream task to this task

### Release Jira Linking (Step 7.5)

If a release Epic and release Task exist (or are created) for the 2.2.x stream, both remediation tasks would be linked:
- Remediation Tasks -> release Task (Blocks)
- TC-8020 -> release Task (Related)

### Post-Triage Summary

**PROPOSAL**: Add the `ai-cve-triaged` label to TC-8020.

**PROPOSAL**: Post a summary comment to TC-8020 documenting:
1. Version impact table (2.2.x: 2.2.0-2.2.2 affected, 2.2.3-2.2.4 not affected)
2. Affects Versions correction (RHTPA 2.0.0 -> RHTPA 2.2.0, 2.2.1, 2.2.2)
3. Triage outcome: Case B remediation with Case A cross-stream notice
4. Links to created remediation tasks
5. Concurrent triage note (TC-8019 on same component)
6. Reporter @mention (ADF mention node with reporter's account ID)
7. Comment Footnote per shared/comment-footnote.md (skill: triage-security)

## Complete PROPOSED Jira Mutations Summary

All mutations are PROPOSALS pending engineer confirmation:

| # | Operation | Target | Details |
|---|-----------|--------|---------|
| 1 | Assign issue | TC-8020 | Assign to current user |
| 2 | Transition | TC-8020 | New -> Assigned |
| 3 | Field edit | TC-8020 | Affects Versions: [RHTPA 2.0.0] -> [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2] |
| 4 | Comment | TC-8020 | Affects Versions correction with lock file evidence |
| 5 | Field edit | TC-8020 | Add label `concurrent-triage-overlap` (if Option 3 chosen) |
| 6 | Comment | TC-8020 | Cross-stream impact notice (2.1.x also affected) |
| 7 | Create Task | New | Dependency bump task for 2.2.x stream |
| 8 | Create Task | New | Downstream propagation task for 2.2.x stream |
| 9 | Link (Depend) | TC-8020 -> Task 7 | Standard remediation linkage |
| 10 | Link (Depend) | TC-8020 -> Task 8 | Standard remediation linkage |
| 11 | Link (Blocks) | Task 7 -> Task 8 | Upstream blocks downstream |
| 12 | Field edit | TC-8020 | Add label `ai-cve-triaged` |
| 13 | Comment | TC-8020 | Post-triage summary with version impact table |

If no existing CVE Jira covers 2.1.x:
| 14 | Create Task | New | Preemptive dependency bump for 2.1.x (security-preemptive) |
| 15 | Create Task | New | Preemptive downstream propagation for 2.1.x (security-preemptive) |
| 16 | Link (Related) | TC-8020 -> Task 14 | Preemptive linkage |
| 17 | Link (Related) | TC-8020 -> Task 15 | Preemptive linkage |
| 18 | Comment | TC-8020 | Preemptive task listing |
