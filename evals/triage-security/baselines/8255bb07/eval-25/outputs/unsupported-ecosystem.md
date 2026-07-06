# Unsupported Ecosystem Notification

**Unsupported ecosystem**: Go modules is not yet supported for automated triage. Manual assessment is required.

## Details

- **Issue**: TC-8040
- **CVE**: CVE-2026-31812
- **Vulnerable library**: quinn-proto
- **Detected ecosystem**: Go modules
- **Configured ecosystems**: Cargo, RPM

The Ecosystem Mappings tables in the configured version streams (2.1.x, 2.2.x) do not include an entry for Go modules. Without an ecosystem mapping, the skill cannot determine the lock file path, check command, or repository to inspect for dependency versions.

Automated triage has stopped at Step 1 (Ecosystem Detection). No version impact analysis, Affects Versions correction, or remediation task creation has been performed.

## Required Action

A manual assessment is required to determine:

1. Which lock file or dependency manifest tracks Go module dependencies
2. Which versions of the vulnerable library (quinn-proto) are shipped in each supported product version
3. Whether any supported versions are affected and require remediation

Alternatively, add a Go modules entry to the Ecosystem Mappings table in the relevant `security-matrix.md` files and re-run triage.
