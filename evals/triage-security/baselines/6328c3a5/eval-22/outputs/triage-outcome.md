# Triage Outcome (Step 8) -- TC-8021

## Issue Summary

- **Issue**: TC-8021
- **CVE**: CVE-2026-31812
- **Library**: quinn-proto
- **Fix threshold**: >= 0.11.14
- **CVSS**: 7.5 (High)
- **Scoped stream**: 2.2.x

## Version Impact Summary

| Stream | Affected Versions | Latest Version Status |
|--------|-------------------|-----------------------|
| 2.2.x (scoped) | 2.2.0, 2.2.1, 2.2.2 | 2.2.3 and 2.2.4 ship quinn-proto 0.11.14 (FIXED) |
| 2.1.x (cross-stream) | 2.1.0, 2.1.1 | 2.1.1 ships quinn-proto 0.11.9 (STILL AFFECTED) |

## Affects Versions Correction

- **Before**: RHTPA 2.0.0 (incorrect -- no 2.0.x stream exists in Version Streams)
- **After**: RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2
- **Rationale**: Lock file analysis at pinned commits confirms only these three
  versions in the scoped 2.2.x stream ship quinn-proto < 0.11.14. Versions
  2.2.3 and 2.2.4 already include the fix (quinn-proto 0.11.14).

## Concurrent Triage (Step 7)

No concurrent triages detected on the `quinn-proto` upstream component
(customfield_10632). Proceeding without constraints.

## Triage Decision

### Case B: Affected versions exist in scoped stream

Supported versions within the 2.2.x stream are affected (2.2.0, 2.2.1, 2.2.2).
However, the latest released versions in this stream (2.2.3 and 2.2.4) already
ship quinn-proto 0.11.14, which is the fixed version. The upstream fix has
already been propagated to the downstream Konflux release repo in builds
v0.4.11 and v0.4.12.

**Remediation tasks for 2.2.x**: Since the fix is already present in the latest
released versions (2.2.3+), the vulnerability has already been remediated in
the 2.2.x stream. Customers on versions 2.2.0, 2.2.1, or 2.2.2 should upgrade
to version 2.2.3 or later to pick up the fix. The Affects Versions correction
documents which versions were affected. No new remediation engineering task is
required for the 2.2.x stream -- the fix is already shipped.

### Case A: Cross-stream impact (proactive remediation)

The issue is scoped to stream 2.2.x, but the version impact analysis reveals
that stream 2.1.x is also affected:

- 2.1.0 ships quinn-proto 0.11.9 (affected)
- 2.1.1 ships quinn-proto 0.11.9 (affected)

The latest version in 2.1.x (2.1.1) still ships a vulnerable quinn-proto version.
Unlike the 2.2.x stream, the 2.1.x stream has NOT yet picked up the fix.

**Cross-stream impact comment**: A comment should be posted to TC-8021 noting:

> Cross-stream impact: quinn-proto < 0.11.14 also affects stream 2.1.x based
> on lock file analysis. All versions in the 2.1.x stream (2.1.0, 2.1.1) ship
> quinn-proto 0.11.9 which is within the affected range. These streams are
> tracked by companion issues (see Related links) or may require separate
> PSIRT triage.

**Preemptive remediation for 2.1.x**: If no existing CVE Jira for CVE-2026-31812
exists scoped to stream 2.1.x (to be checked via Step 4 sibling search), then
proactive remediation tasks should be created for the 2.1.x stream with the
`security-preemptive` label and "Related" link type (per Case A procedure):

1. **Upstream dependency bump task** (2.1.x): Bump quinn-proto to >= 0.11.14 on
   the `release/0.3.z` upstream branch. Ecosystem: Cargo. Labels include
   `security-preemptive`, `CVE-2026-31812`, `ai-generated-jira`.
2. **Downstream propagation task** (2.1.x): Propagate the quinn-proto fix to the
   Konflux release repo `rhtpa-release.0.3.z`. Blocked by the upstream bump task.
   Labels include `security-preemptive`, `CVE-2026-31812`, `ai-generated-jira`.

If a sibling CVE Jira for 2.1.x already exists, skip preemptive task creation
for that stream -- it will be triaged through its own issue.

## Post-Triage Actions

1. **Correct Affects Versions**: RHTPA 2.0.0 -> RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2
2. **Add `ai-cve-triaged` label** to TC-8021
3. **Post cross-stream impact comment** documenting 2.1.x exposure
4. **Create preemptive remediation tasks** for 2.1.x (if no sibling CVE Jira exists)
5. **Post summary comment** to TC-8021 with:
   - Version impact table
   - Affects Versions correction record
   - Triage outcome: 2.2.x already fixed in 2.2.3+; 2.1.x affected
   - Links to any preemptive remediation tasks created
   - @mention of the issue reporter (PSIRT analyst)
6. **Transition** TC-8021 to reflect triage completion

## Ecosystem Classification

| Category | Ecosystem | Tasks per stream |
|----------|-----------|-----------------|
| Source dependency (fix available) | Cargo | 2 (dependency bump + downstream propagation) |

For the 2.2.x stream specifically, the fix is already in the latest release, so
no new remediation tasks are created. For the 2.1.x stream (preemptive), the
standard 2-task pattern applies since the fix has not yet been picked up.
