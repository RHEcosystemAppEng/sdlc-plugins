# Unsupported Ecosystem Notification — TC-8040

## Triage Halted: Unsupported Ecosystem

**Issue**: TC-8040
**CVE**: CVE-2026-31812
**Library**: quinn-proto
**Detected Ecosystem**: Go modules

**Unsupported ecosystem**: Go modules is not yet supported for automated triage. Manual assessment is required.

The Ecosystem Mappings tables in the configured security matrices for all version streams (2.1.x, 2.2.x) list only the following ecosystems:

| Ecosystem | Category |
|-----------|----------|
| Cargo | Source dependency |
| RPM | System package |

**Go modules** does not appear in any stream's Ecosystem Mappings table. Without a configured ecosystem mapping, the skill cannot determine:

- Which lock file to inspect (e.g., `go.sum`, `go.mod`)
- Which check command to use for dependency version extraction
- Which upstream branch to reference
- The remediation task structure (number of tasks per stream)

## Required Action

To enable automated triage for Go modules, the following steps are needed:

1. Add a Go modules row to each stream's `security-matrix.md` Ecosystem Mappings table, specifying:
   - Repository name
   - Lock file path (e.g., `go.sum`)
   - Check command (e.g., `git show <tag>:go.sum`)
   - Upstream branch
2. Update the ecosystem classification table to define Go modules' category (source dependency or system package) and its remediation task count per stream.
3. Re-run `/sdlc-workflow:triage-security TC-8040` after the configuration is updated.

Until then, this CVE requires manual version impact analysis and manual remediation task creation.
