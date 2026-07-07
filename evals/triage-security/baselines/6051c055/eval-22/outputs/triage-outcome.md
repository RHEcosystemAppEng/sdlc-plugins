# Triage Outcome: TC-8021 (CVE-2026-31812 / quinn-proto)

## Summary

CVE-2026-31812 affects quinn-proto versions before 0.11.14. The issue is scoped to the
2.2.x stream via its summary suffix `[rhtpa-2.2]`. Version impact analysis shows:

- **2.2.x stream (in scope):** Versions 2.2.0, 2.2.1, and 2.2.2 shipped the vulnerable
  quinn-proto (0.11.9 or 0.11.12). However, the fix is already present in versions 2.2.3
  and 2.2.4, which ship quinn-proto 0.11.14. The latest shipped version is not affected.
- **2.1.x stream (cross-stream):** All versions (2.1.0, 2.1.1) ship quinn-proto 0.11.9
  and remain affected. The latest build (v0.3.12) still includes the vulnerable version.

## Concurrent Triage Detection (Step 7)

No concurrent triages detected for the `quinn-proto` upstream component. The JQL search
returned zero results. Proceeding directly to Case A/B/C branching without presenting
wait/skip/proceed options.

## Case Determination

### Case A: Affected -- remediation tasks for scoped stream (2.2.x)

Versions 2.2.0 through 2.2.2 in the 2.2.x stream shipped the vulnerable quinn-proto.
However, the vulnerability was already fixed starting in version 2.2.3 (build 0.4.11),
which ships quinn-proto 0.11.14. The latest shipped version (2.2.4 / build 0.4.12) also
ships the fixed version.

**No new remediation task is needed for the 2.2.x stream.** The fix is already present
in the most recent builds. The Affects Versions field should be corrected to accurately
record which versions were affected for tracking purposes.

### Case B: Cross-stream impact -- proactive remediation for 2.1.x

The issue is stream-scoped to 2.2.x, but version impact analysis reveals that the
**2.1.x stream** is also affected:

| Stream | Versions Affected | Latest Build | quinn-proto Version | Status |
|--------|-------------------|--------------|---------------------|--------|
| 2.1.x | 2.1.0, 2.1.1 | v0.3.12 | 0.11.9 | Still vulnerable |

Since the issue is scoped (has stream suffix `[rhtpa-2.2]`), Case B applies for the
2.1.x stream. The following actions are recommended:

1. **Post a cross-stream impact comment** on TC-8021:
   > Cross-stream impact: quinn-proto versions before 0.11.14 also affects stream 2.1.x
   > based on lock file analysis. Stream 2.1.x ships quinn-proto 0.11.9 in all versions
   > (2.1.0, 2.1.1). This stream is tracked by companion issues (see Related links) or
   > may require separate PSIRT triage.

2. **Check for existing companion CVE Jiras** for the 2.1.x stream by searching for
   sibling Vulnerability issues with label `CVE-2026-31812` and summary suffix
   `[rhtpa-2.1]`.

3. **If no companion CVE Jira exists for 2.1.x**, create proactive remediation tasks
   using the preemptive variant:
   - Labels include `security-preemptive` alongside standard labels
   - Link type is "Related" (not "Depend") to TC-8021
   - Two tasks for Cargo ecosystem:
     a. Upstream backport task: bump quinn-proto to >= 0.11.14 in rhtpa-backend on
        branch `release/0.3.z`
     b. Downstream propagation subtask: update the backend source reference in
        rhtpa-release.0.3.z to pick up the fixed version

4. **If a companion CVE Jira exists**, skip proactive task creation for 2.1.x --
   that stream will be triaged through its own CVE issue.

## Affects Versions Correction (Step 3)

The PSIRT-assigned Affects Versions is incorrect:

```
Current:  [RHTPA 2.0.0]
Proposed: [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]
```

Rationale:
- RHTPA 2.0.0 does not correspond to any configured version stream (no 2.0.x stream exists)
- Lock file analysis confirms versions 2.2.0, 2.2.1, and 2.2.2 shipped vulnerable
  quinn-proto (0.11.9 and 0.11.12, both < 0.11.14)
- Versions 2.2.3 and 2.2.4 are excluded because they ship the fixed version (0.11.14)
- Correction is scoped to the 2.2.x stream per the issue suffix `[rhtpa-2.2]`
- 2.1.x versions are not included because they belong to a different stream scope

## Post-Triage Actions

1. **Correct Affects Versions** from RHTPA 2.0.0 to RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2
   (requires engineer confirmation)
2. **Add `ai-cve-triaged` label** to TC-8021
3. **Post cross-stream impact comment** documenting the 2.1.x impact
4. **Create preemptive remediation tasks for 2.1.x** if no companion CVE Jira exists
   (two Cargo ecosystem tasks: upstream backport + downstream propagation)
5. **Post summary comment** on TC-8021 with version impact table, Affects Versions
   correction, triage outcome, and @mention of the reporter
6. All comments include the Comment Footnote per skill requirements
