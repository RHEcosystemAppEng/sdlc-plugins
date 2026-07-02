# Step 8 -- Triage Outcome for TC-8021

## Summary

CVE-2026-31812 affects quinn-proto versions before 0.11.14. The issue TC-8021 is scoped to the **2.2.x** stream (from summary suffix `[rhtpa-2.2]`). Lock file analysis shows that versions 2.2.0, 2.2.1, and 2.2.2 ship a vulnerable version of quinn-proto, while versions 2.2.3 and 2.2.4 already ship the fixed version (0.11.14). The 2.1.x stream is also affected (both 2.1.0 and 2.1.1 ship quinn-proto 0.11.9), triggering cross-stream impact handling.

## Concurrent Triage Check (Step 7)

No concurrent triages detected on upstream component "quinn-proto" -- proceeding directly to Case A/B/C branching.

## Case Determination

### Case A: Affected -- remediation required for scoped stream (2.2.x)

Versions 2.2.0, 2.2.1, and 2.2.2 in the scoped 2.2.x stream are affected:

| Version | quinn-proto | Affected? |
|---------|-------------|-----------|
| 2.2.0 | 0.11.9 | YES |
| 2.2.1 | 0.11.12 | YES |
| 2.2.2 | 0.11.12 | YES (retag of 2.2.1) |
| 2.2.3 | 0.11.14 | NO (fixed) |
| 2.2.4 | 0.11.14 | NO (fixed) |

Since affected versions exist within the scoped stream, this is **Case A: Affected**. Remediation tasks are required.

### Case B: Cross-stream impact -- 2.1.x also affected

The version impact analysis reveals that the **2.1.x** stream (outside TC-8021's scope) is also affected:

| Version | quinn-proto | Affected? |
|---------|-------------|-----------|
| 2.1.0 | 0.11.9 | YES |
| 2.1.1 | 0.11.9 | YES |

Per Case B, the following actions apply:
1. Post a cross-stream impact comment on TC-8021 noting that the 2.1.x stream is also affected.
2. Search for sibling CVE Jiras covering 2.1.x (same CVE label CVE-2026-31812, stream suffix `[rhtpa-2.1]`).
3. If no sibling exists for 2.1.x, create preemptive remediation tasks with the `security-preemptive` label and "Related" link type to TC-8021.
4. If a sibling already exists for 2.1.x, skip preemptive task creation for that stream (it will be triaged through its own CVE issue).

## Remediation Tasks (Case A -- scoped stream 2.2.x)

The ecosystem is **Cargo** (Rust crate). Per the skill's remediation rules, Cargo dependencies require **two tasks** per affected stream:

### Task 1: Upstream backport (source repo fix)

- **Type:** Task
- **Summary:** Bump quinn-proto to >= 0.11.14 in rhtpa-backend (CVE-2026-31812, rhtpa-2.2)
- **Target repository:** rhtpa-backend
- **Action:** Update quinn-proto dependency to version 0.11.14 or later in Cargo.toml/Cargo.lock
- **Upstream branch:** release/0.4.z
- **Upstream fix reference:** https://github.com/quinn-rs/quinn/pull/2048
- **Link to CVE Jira:** TC-8021 (link type: Depend)
- **Labels:** CVE-2026-31812, security

Note: The upstream fix is already available at branch HEAD of release/0.4.z -- versions 2.2.3 and 2.2.4 already carry quinn-proto 0.11.14. The remediation task targets versions 2.2.0 through 2.2.2 which were released with vulnerable versions. A point release or backport to the 0.4.z branch covering these versions needs the quinn-proto bump.

### Task 2: Downstream propagation (Konflux release repo update)

- **Type:** Subtask of Task 1
- **Summary:** Propagate quinn-proto fix to rhtpa-release.0.4.z (CVE-2026-31812, rhtpa-2.2)
- **Target repository:** rhtpa-release.0.4.z (Konflux release repo for 2.2.x)
- **Action:** Update the backend source tag reference in artifacts.lock.yaml to a tag that includes the quinn-proto bump
- **Blocked by:** Task 1 (upstream backport must land first)
- **Link to CVE Jira:** TC-8021 (link type: Depend)
- **Labels:** CVE-2026-31812, security

## Cross-Stream Preemptive Tasks (Case B -- 2.1.x stream)

If no sibling CVE Jira exists for 2.1.x:

### Preemptive Task 1: Upstream backport for 2.1.x

- **Summary:** Bump quinn-proto to >= 0.11.14 in rhtpa-backend (CVE-2026-31812, rhtpa-2.1) [preemptive]
- **Target repository:** rhtpa-backend
- **Upstream branch:** release/0.3.z
- **Labels:** CVE-2026-31812, security, security-preemptive
- **Link to TC-8021:** Related (not Depend, since this is preemptive)

### Preemptive Task 2: Downstream propagation for 2.1.x

- **Summary:** Propagate quinn-proto fix to rhtpa-release.0.3.z (CVE-2026-31812, rhtpa-2.1) [preemptive]
- **Target repository:** rhtpa-release.0.3.z
- **Labels:** CVE-2026-31812, security, security-preemptive
- **Blocked by:** Preemptive Task 1
- **Link to TC-8021:** Related (not Depend)

## Post-Triage Actions

1. Add label `ai-cve-triaged` to TC-8021.
2. Post a summary comment on TC-8021 documenting:
   - Version impact table (all streams)
   - Affects Versions correction: RHTPA 2.0.0 replaced with RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2
   - Triage outcome: Case A (affected) with Case B (cross-stream impact on 2.1.x)
   - Links to all remediation tasks created
   - @mention of the issue reporter
   - Comment Footnote per skill requirements
