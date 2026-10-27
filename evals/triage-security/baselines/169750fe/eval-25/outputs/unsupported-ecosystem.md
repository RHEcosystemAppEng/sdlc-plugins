# Unsupported Ecosystem Notification

**Unsupported ecosystem**: Go modules is not yet supported for automated triage. Manual assessment is required.

## Details

- **CVE**: CVE-2026-31812
- **Issue**: TC-8040
- **Vulnerable Library**: quinn-proto
- **Detected Ecosystem**: Go modules
- **Supported Ecosystems (2.2.x stream)**: Cargo, RPM

Automated version impact analysis, remediation task creation, and all subsequent triage steps (Steps 2--8) cannot proceed because the Go modules ecosystem is not configured in the stream's Ecosystem Mappings table.

## Required Action

A manual assessment is required to determine:

1. Whether the vulnerable library (quinn-proto) is present in the product's Go module dependencies
2. Which supported product versions ship a vulnerable version
3. What remediation steps are needed

To enable automated triage for Go modules in the future, add a Go modules row to the Ecosystem Mappings table in the relevant `security-matrix.md` files, specifying the repository, lock file (e.g., `go.sum`), check command, and upstream branch.
