# Triage Outcome — TC-8021

## Triage Decision: Case A + Case B

TC-8021 is **affected** within its scoped stream (2.2.x) and has **cross-stream impact** on stream 2.1.x. This triggers both Case A (create remediation tasks for the in-scope stream) and Case B (cross-stream impact notification and possible preemptive remediation for the out-of-scope stream).

## Case A: Remediation Tasks for Stream 2.2.x (In-Scope)

The issue is scoped to stream 2.2.x via the summary suffix `[rhtpa-2.2]`. Within this stream, versions 2.2.0, 2.2.1, and 2.2.2 ship quinn-proto below the fix threshold of 0.11.14.

Versions 2.2.3 and 2.2.4 already ship quinn-proto 0.11.14 (the fixed version) and are **not affected**.

Since quinn-proto is a **Cargo** (source dependency) ecosystem, two remediation tasks would be created:

### Task 1: Upstream Backport Task (2.2.x)

- **Summary**: Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (rhtpa-2.2)
- **Repository**: rhtpa-backend
- **Target Branch**: release/0.4.z
- **Labels**: ai-generated-jira, Security, CVE-2026-31812
- **Description**: Update quinn-proto dependency to >= 0.11.14 in Cargo.lock on branch release/0.4.z. Affected versions: RHTPA 2.2.0, 2.2.1, 2.2.2. Upstream fix PR: quinn-rs/quinn#2048. Advisory: GHSA-2026-qp73-x4mq.
- **Link**: Depend on TC-8021 (parent Vulnerability issue)

### Task 2: Downstream Propagation Subtask (2.2.x)

- **Summary**: Propagate CVE-2026-31812 fix: update rhtpa-backend ref in rhtpa-release.0.4.z (rhtpa-2.2)
- **Repository**: rhtpa-release.0.4.z
- **Target Branch**: main
- **Labels**: ai-generated-jira, Security, CVE-2026-31812
- **Description**: Update rhtpa-backend reference in rhtpa-release.0.4.z to pick up the CVE-2026-31812 fix from the upstream backport task. Source pinning method: artifacts.lock.yaml (download URL contains tag).
- **Links**:
  - Depend on TC-8021 (parent Vulnerability issue)
  - Blocked by upstream backport task (Task 1)

### Coordination Guidance

The Source Repositories table does not include a Deployment Context column. Per backward-compatibility rules, coordination guidance is **omitted** from remediation task descriptions.

## Case B: Cross-Stream Impact on 2.1.x

The version impact analysis reveals that **stream 2.1.x** (outside this issue's scope) is also affected:

| Version | quinn-proto Version | Affected? |
|---------|---------------------|-----------|
| 2.1.0 | 0.11.9 | YES |
| 2.1.1 | 0.11.9 | YES |

### Cross-Stream Impact Comment

A comment would be posted to TC-8021:

> Cross-stream impact: quinn-proto (versions before 0.11.14) also affects stream 2.1.x based on lock file analysis. This stream is tracked by companion issues (see Related links) or may require separate PSIRT triage.

### Preemptive Remediation Check

A JQL search for sibling Vulnerability issues with the CVE-2026-31812 label and stream suffix `[rhtpa-2.1]` would determine whether a companion CVE Jira exists for stream 2.1.x:

- **If a companion CVE Jira exists for 2.1.x**: skip preemptive task creation for that stream (it will be triaged through its own issue).
- **If no companion CVE Jira exists for 2.1.x**: create preemptive remediation tasks for 2.1.x with the `security-preemptive` label and "Related" link type (not "Depend") to TC-8021. Two preemptive tasks would be created:
  1. Upstream backport: bump quinn-proto to 0.11.14 on branch release/0.3.z (labels: ai-generated-jira, Security, CVE-2026-31812, security-preemptive)
  2. Downstream propagation: update rhtpa-backend ref in rhtpa-release.0.3.z (labels: ai-generated-jira, Security, CVE-2026-31812, security-preemptive)

## Affects Versions Correction (Step 3)

The PSIRT-assigned Affects Versions is **RHTPA 2.0.0**, which is incorrect. There is no 2.0.x stream in the configured Version Streams. Scoped to the 2.2.x stream, the correct Affects Versions (based on lock file evidence) should be:

- **Current**: [RHTPA 2.0.0]
- **Proposed**: [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]

Versions 2.2.3 and 2.2.4 are excluded because they ship quinn-proto 0.11.14 (at or above the fix threshold).

The Jira version IDs would be discovered dynamically via `getJiraIssueTypeMetaWithFields` and the correction applied after engineer confirmation.

## Post-Triage Actions

1. **Add label** `ai-cve-triaged` to TC-8021
2. **Post summary comment** to TC-8021 documenting:
   - Version impact table (both streams)
   - Affects Versions correction (RHTPA 2.0.0 -> RHTPA 2.2.0, 2.2.1, 2.2.2)
   - Remediation tasks created (upstream + downstream for 2.2.x)
   - Cross-stream impact on 2.1.x
   - @mention of the issue reporter
   - Comment Footnote per shared/comment-footnote.md
3. **Transition** TC-8021 to In Progress
4. **Assign** TC-8021 to current user

## Step 7 Impact on Decision

Concurrent triage detection (Step 7) found **zero** in-progress triages on the same upstream component (quinn-proto). No concurrent triage warning was needed. The skill proceeded silently to Case A/B branching without presenting any options to the user.
