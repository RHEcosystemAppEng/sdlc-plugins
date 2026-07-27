# Unsupported Ecosystem Notification

## TC-8040 -- CVE-2026-31812 (quinn-proto)

**Unsupported ecosystem**: Go modules is not yet supported for automated triage. Manual assessment is required.

### Context

- **CVE**: CVE-2026-31812
- **Library**: quinn-proto
- **Detected ecosystem**: Go modules
- **Stream scope**: 2.2.x (from summary suffix `[rhtpa-2.2]`)
- **Affected version range**: versions before 0.11.14
- **Fixed version**: 0.11.14

### Supported Ecosystems

The following ecosystems are currently configured in the security matrix Ecosystem Mappings tables:

| Ecosystem | Category | Remediation Tasks per Stream |
|-----------|----------|------------------------------|
| Cargo | Source dependency | 2 (upstream backport + downstream propagation) |
| RPM | System package | 1 (Konflux release repo fix) |

Go modules does not appear in any stream's Ecosystem Mappings table. To enable automated triage for Go modules:

1. Determine the category for Go modules (source dependency or system package)
2. Add a Go modules row to the Ecosystem Mappings table in each relevant stream's `security-matrix.md`, specifying the lock file path (e.g., `go.sum` or `go.mod`) and check command
3. Update the ecosystem classification table to define the remediation task structure
4. Re-run triage for this issue

### Triage Status

Automated triage has been **stopped** at Step 1 (Ecosystem Detection). No version impact analysis, Affects Versions correction, or remediation task creation has been performed. The issue remains in its current state (New, Unassigned) pending manual assessment or ecosystem configuration.
