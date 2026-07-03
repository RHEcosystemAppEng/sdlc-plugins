# Unsupported Ecosystem Notification

## TC-8040 -- CVE-2026-31812 (quinn-proto)

**Unsupported ecosystem**: Go modules is not yet supported for automated triage. Manual assessment is required.

### Details

The vulnerability in `quinn-proto` (CVE-2026-31812, affected versions before 0.11.14, fixed in 0.11.14) was detected as belonging to the **Go modules** ecosystem. However, the Ecosystem Mappings tables in the configured version streams only support the following ecosystems:

| Stream | Supported Ecosystems |
|--------|---------------------|
| 2.1.x (rhtpa-release.0.3.z) | Cargo, RPM |
| 2.2.x (rhtpa-release.0.4.z) | Cargo, RPM |

**Go modules** does not appear in any stream's Ecosystem Mappings table. Without an ecosystem mapping, the skill cannot determine:

- Which lock file to inspect (e.g., `go.sum`, `go.mod`)
- Which repository contains the dependency
- Which check command to use for version extraction
- Which upstream branch to reference for fixes

### Required Action

Automated triage (Steps 2-8) cannot proceed for this ecosystem. The engineer must:

1. **Manually verify** whether the vulnerable library `quinn-proto` at a version below 0.11.14 is shipped in any supported product version.
2. **Assess version impact** by inspecting the appropriate dependency manifest (e.g., `go.sum` or `go.mod`) at each pinned source commit in the supportability matrix.
3. **Correct Affects Versions** in Jira based on the manual findings.
4. **Create remediation tasks** if any supported versions are affected, or close the issue as "Not a Bug" if none are affected.

Alternatively, if Go modules should be supported for automated triage in the future, add a `Go modules` row to the Ecosystem Mappings table in each stream's `security-matrix.md` with the appropriate repository, lock file path, check command, and upstream branch.
