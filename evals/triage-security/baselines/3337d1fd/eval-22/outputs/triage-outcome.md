# Step 8 -- Triage Outcome for TC-8021

## Summary

**CVE**: CVE-2026-31812
**Library**: quinn-proto
**Fix threshold**: >= 0.11.14
**Issue scope**: Stream 2.2.x (from summary suffix `[rhtpa-2.2]`)
**Ecosystem**: Cargo (source dependency)

## Version Impact Recap

### Scoped stream (2.2.x)

| Version | quinn-proto | Affected? | Notes |
|---------|-------------|-----------|-------|
| 2.2.0 | 0.11.9 | YES | |
| 2.2.1 | 0.11.12 | YES | |
| 2.2.2 | -- | YES | retag of 2.2.1 |
| 2.2.3 | 0.11.14 | NO | ships fixed version |
| 2.2.4 | 0.11.14 | NO | ships fixed version |

### Other streams (outside scope)

| Version | Stream | quinn-proto | Affected? |
|---------|--------|-------------|-----------|
| 2.1.0 | 2.1.x | 0.11.9 | YES |
| 2.1.1 | 2.1.x | 0.11.9 | YES |

## Step 7 Result

No concurrent triages detected on `quinn-proto` (zero JQL results). Proceeding to remediation.

## Triage Decision

### Case A applies: Affected versions exist in the scoped stream

Versions 2.2.0, 2.2.1, and 2.2.2 within the 2.2.x stream ship quinn-proto versions below the 0.11.14 fix threshold. Remediation is required.

Since this is a **Cargo** (source dependency) ecosystem, two remediation tasks would be created for stream 2.2.x:

1. **Upstream backport task**: Bump quinn-proto to >= 0.11.14 in the `backend` source repository on branch `release/0.4.z`.
   - Summary: "Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (rhtpa-2.2)"
   - Labels: `ai-generated-jira`, `Security`, `CVE-2026-31812`
   - Repository: backend
   - Target branch: release/0.4.z
   - Linked to TC-8021 via "Depend"

2. **Downstream propagation subtask**: Update the backend source reference in `rhtpa-release.0.4.z` to pick up the upstream fix.
   - Summary: "Propagate CVE-2026-31812 fix: update backend ref in rhtpa-release.0.4.z (rhtpa-2.2)"
   - Labels: `ai-generated-jira`, `Security`, `CVE-2026-31812`
   - Repository: rhtpa-release.0.4.z
   - Target branch: main
   - Blocked by the upstream backport task
   - Linked to TC-8021 via "Depend"

Note: Versions 2.2.3 and 2.2.4 already ship quinn-proto 0.11.14 and are NOT affected. The fix was picked up starting from backend tag v0.4.11.

### Case B applies: Cross-stream impact detected

This is a scoped issue (suffix `[rhtpa-2.2]`), so the cross-stream impact check applies. The version impact analysis shows that stream **2.1.x** is also affected:

- 2.1.0 ships quinn-proto 0.11.9 (affected)
- 2.1.1 ships quinn-proto 0.11.9 (affected)

**Cross-stream comment** would be posted on TC-8021:

> Cross-stream impact: quinn-proto < 0.11.14 also affects stream 2.1.x based on lock file analysis. This stream is tracked by a companion issue (see Related links) or may require separate PSIRT triage.

The skill would then check for existing sibling CVE Jiras for stream 2.1.x (searching for Vulnerability issues with label `CVE-2026-31812` and suffix `[rhtpa-2.1]`).

- **If a sibling CVE Jira exists for 2.1.x**: Skip task creation for that stream -- it will be triaged through its own issue.
- **If no sibling CVE Jira exists for 2.1.x**: Create **preemptive** remediation tasks for the 2.1.x stream:
  1. Upstream backport task (security-preemptive): bump quinn-proto to 0.11.14 on `release/0.3.z`
  2. Downstream propagation subtask (security-preemptive): update backend ref in `rhtpa-release.0.3.z`
  - Labels include `security-preemptive` alongside standard labels
  - Link type is "Related" (not "Depend") to TC-8021
  - When PSIRT creates a 2.1.x-specific CVE Jira, Step 4.4 reconciliation will link them and remove the `security-preemptive` label

### Affects Versions Correction (Step 3)

The PSIRT-assigned Affects Versions (`RHTPA 2.0.0`) is incorrect. The proposed correction, scoped to the 2.2.x stream:

```
Current: [RHTPA 2.0.0] --> Proposed: [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]
```

Rationale: RHTPA 2.0.0 does not correspond to any configured version stream. Lock file analysis confirms that versions 2.2.0, 2.2.1, and 2.2.2 ship vulnerable quinn-proto versions. Versions 2.2.3 and 2.2.4 ship the fixed version (0.11.14) and are excluded.

### Coordination Guidance

The Source Repositories table does not include a Deployment Context column. Per backward compatibility rules, the coordination guidance subsection is omitted from remediation task descriptions.

### Post-Triage Actions

1. Add `ai-cve-triaged` label to TC-8021
2. Post summary comment to TC-8021 documenting:
   - Version impact table
   - Affects Versions correction (RHTPA 2.0.0 --> RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2)
   - Remediation tasks created (upstream + downstream for 2.2.x)
   - Cross-stream impact on 2.1.x with preemptive tasks (if applicable)
   - @mention of the vulnerability issue reporter
3. Transition TC-8021 to In Progress
