# Triage Outcome: TC-8020 (CVE-2026-31812 -- quinn-proto)

## Summary

TC-8020 is a PSIRT-created Vulnerability issue for CVE-2026-31812 affecting `quinn-proto` (Rust crate), scoped to stream 2.2.x via the summary suffix `[rhtpa-2.2]`. The vulnerability allows a denial-of-service via a QUIC transport frame that creates an excessive number of streams. The fix threshold is quinn-proto >= 0.11.14 (CVSS 7.5, High severity).

## Version Impact Summary

### Stream 2.2.x (in scope)

| Version | Build Tag | quinn-proto | Affected? |
|---------|-----------|-------------|-----------|
| RHTPA 2.2.0 | v0.4.5 | 0.11.9 | YES |
| RHTPA 2.2.1 | v0.4.8 | 0.11.12 | YES |
| RHTPA 2.2.2 | v0.4.9 | 0.11.12 (retag of 2.2.1) | YES |
| RHTPA 2.2.3 | v0.4.11 | 0.11.14 | NO (fixed) |
| RHTPA 2.2.4 | v0.4.12 | 0.11.14 | NO (fixed) |

### Stream 2.1.x (out of scope -- cross-stream)

| Version | Build Tag | quinn-proto | Affected? |
|---------|-----------|-------------|-----------|
| RHTPA 2.1.0 | v0.3.8 | 0.11.9 | YES |
| RHTPA 2.1.1 | v0.3.12 | 0.11.9 | YES |

## Triage Decision

**Outcome: Case A + Case B -- Affected versions exist with cross-stream impact, gated by Step 7 concurrent triage detection.**

### Step 3: Affects Versions Correction Required

The PSIRT-assigned Affects Versions (`RHTPA 2.0.0`) is incorrect. There is no 2.0.x stream in the configured Version Streams. The corrected Affects Versions, scoped to stream 2.2.x, are:

- **Current**: `[RHTPA 2.0.0]`
- **Proposed**: `[RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]`

Versions 2.2.3 and 2.2.4 are excluded because they already ship quinn-proto 0.11.14 (the fixed version). This correction requires engineer confirmation before the Jira update is executed.

### Step 7: Concurrent Triage Gate

Before creating remediation tasks, Step 7 detected that TC-8019 is actively being triaged by engineer-b@example.com and targets the same upstream component (`quinn-proto`). The engineer must choose:

1. **Wait** -- pause until TC-8019 completes, then re-run to detect overlap
2. **Skip** -- skip task creation, add explanatory Jira comment
3. **Proceed** -- create tasks with `concurrent-triage-overlap` label

This gate prevents duplicate remediation tasks when two triages target the same library concurrently.

### Step 8: Remediation Plan (contingent on Step 7 resolution)

If the engineer chooses to proceed:

**Case A -- Cross-stream impact**: Stream 2.1.x is also affected (all versions ship quinn-proto 0.11.9, well below the 0.11.14 fix threshold). A cross-stream impact comment is posted to TC-8020 noting that 2.1.x is impacted. If no sibling CVE Jira exists for stream 2.1.x, proactive remediation tasks are created with the `security-preemptive` label and linked to TC-8020 via "Related" link type.

**Case B -- Remediation tasks for stream 2.2.x**: Since quinn-proto is a Cargo (source dependency) ecosystem, two tasks are created per the ecosystem classification:

1. **Upstream backport task**: Bump quinn-proto from the current vulnerable versions (0.11.9 / 0.11.12) to >= 0.11.14 in the `rhtpa-backend` repository on branch `release/0.4.z`. Reference upstream fix PR: quinn-rs/quinn#2048. Lock file: `Cargo.lock`. Linked to TC-8020 via "Depend".

2. **Downstream propagation task** (blocked by upstream task via "Blocks" link): Update `artifacts.lock.yaml` in Konflux release repo `rhtpa-release.0.4.z` to reference the new backend build that includes the quinn-proto fix. Linked to TC-8020 via "Depend".

### Post-Triage Actions

After all remediation actions are complete:

1. Add the `ai-cve-triaged` label to TC-8020
2. Post a summary comment to TC-8020 documenting:
   - The version impact table (both streams)
   - The Affects Versions correction (RHTPA 2.0.0 replaced with RHTPA 2.2.0, 2.2.1, 2.2.2)
   - The triage outcome and concurrent triage detection result
   - Links to all created remediation tasks
   - @mention of the issue reporter (PSIRT analyst) via ADF mention node
   - Comment Footnote per shared/comment-footnote.md (skill: triage-security)
