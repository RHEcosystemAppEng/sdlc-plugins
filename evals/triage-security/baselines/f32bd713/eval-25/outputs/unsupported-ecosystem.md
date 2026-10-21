# Unsupported Ecosystem Notification: TC-8040

## Triage Halted -- Unsupported Ecosystem

**Unsupported ecosystem**: Go modules is not yet supported for automated triage. Manual assessment is required.

### Context

- **Issue**: TC-8040
- **CVE**: CVE-2026-31812
- **Vulnerable library**: quinn-proto (versions before 0.11.14)
- **Detected ecosystem**: Go modules
- **Stream scope**: 2.2.x

### Supported Ecosystems

The following ecosystems are configured in the security matrix Ecosystem Mappings tables and are supported for automated triage:

| Ecosystem | Category | Remediation tasks per stream |
|-----------|----------|------------------------------|
| Cargo | Source dependency | 2 (upstream backport + downstream propagation, or dependency bump + downstream propagation if fix available) |
| RPM | System package | 1 (Konflux release repo fix only) |

### Why Triage Cannot Proceed

The ecosystem classification determines which lock file to inspect, which parsing command to use, and how many remediation tasks to create per affected stream. Since "Go modules" is not listed in any stream's Ecosystem Mappings table:

1. No lock file path is configured for Go module dependencies
2. No check command is defined for inspecting Go module versions
3. No upstream branch mapping exists for Go module repositories
4. The remediation task structure (number and type of tasks) is undefined for this ecosystem

### Recommended Actions

1. **Manual assessment**: A human engineer should manually assess the version impact of CVE-2026-31812 across supported product versions by inspecting Go module dependency files (e.g., `go.sum`, `go.mod`) at the pinned source commits in the supportability matrix.

2. **Add ecosystem support**: To enable automated triage for Go modules in the future, add a "Go modules" row to each stream's Ecosystem Mappings table in `security-matrix.md` with the appropriate:
   - Repository name
   - Lock file path (e.g., `go.sum`)
   - Check command (e.g., `git show <tag>:go.sum`)
   - Upstream branch

3. **Update classification table**: When adding Go modules to the Ecosystem Mappings, also define its category in the ecosystem classification table (source dependency vs. system package) to determine remediation task structure.
