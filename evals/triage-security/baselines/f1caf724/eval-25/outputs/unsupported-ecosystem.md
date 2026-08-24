# Unsupported Ecosystem Notification

## Issue: TC-8040 -- CVE-2026-31812 quinn-proto

**Unsupported ecosystem**: Go modules is not yet supported for automated triage. Manual assessment is required.

### Details

- **CVE**: CVE-2026-31812
- **Library**: quinn-proto
- **Detected ecosystem**: Go modules
- **Configured ecosystems** (from security-matrix.md Ecosystem Mappings):
  - Cargo (lock file: `Cargo.lock`)
  - RPM (lock file: `rpms.lock.yaml`)

### Why triage cannot proceed automatically

The triage-security skill determines which lock file to inspect and which parsing command to use based on the Ecosystem Mappings table in each stream's `security-matrix.md`. The detected ecosystem "Go modules" is not present in any configured stream's Ecosystem Mappings table.

Without a matching ecosystem entry, the skill cannot:

1. Identify the correct lock file (e.g., `go.sum` or `go.mod` for Go modules)
2. Determine the check command to extract dependency versions
3. Identify the upstream branch for fix verification
4. Classify the ecosystem category (source dependency vs. system package) for remediation task structure

### Recommended actions

1. **If Go modules should be supported**: Add a "Go modules" row to the Ecosystem Mappings table in the relevant stream's `security-matrix.md`, specifying the repository, lock file path (e.g., `go.sum`), check command, and upstream branch. Then re-run `/sdlc-workflow:triage-security TC-8040`.

2. **If the ecosystem detection is incorrect**: The library quinn-proto is actually a Rust crate (typically managed via Cargo, not Go modules). If the ecosystem was misidentified, re-evaluate the ecosystem classification. Quinn-proto would normally fall under the Cargo ecosystem, which IS supported.

3. **Manual assessment**: Proceed with manual version impact analysis by inspecting the appropriate dependency files at each pinned commit in the supportability matrix, then return to the skill for Steps 3-8 (Jira triage operations and remediation).
