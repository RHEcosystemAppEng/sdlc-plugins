# Triage Outcome for TC-8021

## Summary

CVE-2026-31812 affects the quinn-proto crate (versions before 0.11.14). The issue is scoped
to stream 2.2.x via the summary suffix `[rhtpa-2.2]`. Version impact analysis shows that
some versions within the scoped stream are affected and other streams outside the scope
are also affected.

## Version Impact Summary

### In-scope stream (2.2.x)

| Version | quinn-proto | Affected? |
|---------|-------------|-----------|
| 2.2.0 | 0.11.9 | YES |
| 2.2.1 | 0.11.12 | YES |
| 2.2.2 | 0.11.12 | YES (retag of 2.2.1) |
| 2.2.3 | 0.11.14 | NO (fixed) |
| 2.2.4 | 0.11.14 | NO (fixed) |

### Out-of-scope stream (2.1.x)

| Version | quinn-proto | Affected? |
|---------|-------------|-----------|
| 2.1.0 | 0.11.9 | YES |
| 2.1.1 | 0.11.9 | YES |

## Step 7 -- Concurrent Triage Detection

No concurrent triages detected on the quinn-proto component. The JQL search for in-progress
triages with `cf[10632] ~ 'quinn-proto'` returned zero results. Proceeding directly to
Case A/B/C branching without any warning or user interaction.

## Triage Decision: Case A + Case B

### Case A: Affected -- create remediation tasks for stream 2.2.x

The in-scope stream (2.2.x) has affected versions (2.2.0, 2.2.1, 2.2.2). This triggers
Case A: create remediation tasks.

Since quinn-proto is a **Cargo** (source dependency) ecosystem, two tasks are created:

1. **Upstream backport task**: Update quinn-proto from the affected version to >= 0.11.14
   in the rhtpa-backend source repository on the `release/0.4.z` branch. The upstream fix
   PR (quinn-rs/quinn#2048) provides the patch reference.

2. **Downstream propagation subtask**: After the upstream fix lands, update the pinned
   source reference in the rhtpa-release.0.4.z Konflux release repo (`artifacts.lock.yaml`)
   to pull in the new backend tag that includes the quinn-proto fix. This task is blocked
   by the upstream backport task.

Both tasks are linked to TC-8021 with a "Depend" link type.

### Case B: Cross-stream impact -- proactive remediation for stream 2.1.x

The version impact analysis reveals that stream **2.1.x** (outside this issue's scope) is
also affected: versions 2.1.0 and 2.1.1 both ship quinn-proto 0.11.9, which is below
the fix threshold of 0.11.14.

Actions for Case B:

1. **Post cross-stream impact comment** on TC-8021:
   > Cross-stream impact: quinn-proto < 0.11.14 also affects stream 2.1.x based on
   > lock file analysis. This stream is tracked by companion issues (see Related links)
   > or may require separate PSIRT triage.

2. **Check for existing CVE Jiras** for stream 2.1.x by searching for sibling Vulnerability
   issues with label CVE-2026-31812 and summary suffix `[rhtpa-2.1]`.

3. **If no sibling CVE Jira exists for 2.1.x**: Create proactive remediation tasks with
   the `security-preemptive` label and "Related" link type to TC-8021. These cover the
   upstream backport and downstream propagation for the 2.1.x stream (`release/0.3.z`
   branch, rhtpa-release.0.3.z Konflux repo).

4. **If a sibling CVE Jira already exists for 2.1.x**: Skip preemptive task creation for
   that stream -- it will be triaged through its own CVE issue.

### Affects Versions Correction

The PSIRT-assigned Affects Versions of "RHTPA 2.0.0" is incorrect (no 2.0.x stream exists).
The correction, scoped to stream 2.2.x, is:

- **Current**: RHTPA 2.0.0
- **Corrected**: RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2

Versions 2.2.3 and 2.2.4 are excluded because they already ship the fixed version
(quinn-proto 0.11.14).

## Post-Triage Actions

1. Add `ai-cve-triaged` label to TC-8021.
2. Post summary comment on TC-8021 documenting:
   - Version impact table
   - Affects Versions correction (RHTPA 2.0.0 replaced with RHTPA 2.2.0, 2.2.1, 2.2.2)
   - Remediation tasks created (upstream backport + downstream propagation for 2.2.x)
   - Cross-stream impact on 2.1.x and any preemptive tasks created
   - @mention of the issue reporter
   - Comment Footnote per shared/comment-footnote.md
