# Unsupported Ecosystem Notification

> **Unsupported ecosystem**: Go modules is not yet supported for automated triage.
> Manual assessment is required.

## Details

- **CVE**: CVE-2026-31812
- **Issue**: TC-8040
- **Detected ecosystem**: Go modules
- **Vulnerable library**: quinn-proto
- **Affected range**: < 0.11.14
- **Fixed version**: 0.11.14

The detected ecosystem (Go modules) does not appear in the Ecosystem Mappings table of any configured version stream's `security-matrix.md`. The configured ecosystems are:

- Cargo
- RPM

Because Go modules is not a supported ecosystem, the following automated triage steps are **not performed**:

- Step 2 — Version Impact Analysis (no lock file path or check command configured for Go modules)
- Step 3 — Affects Versions Correction
- Step 4 — Duplicate / Sibling / Overlap Check
- Step 5 — Version Lifecycle Check
- Step 6 — Already Fixed Check
- Step 7 — Concurrent Triage Detection
- Step 7.5 — Release Jira Orchestration
- Step 8 — Remediation Task Creation

**Action required**: A human engineer must manually assess the version impact and remediation path for this Go modules dependency.
