# Unsupported Ecosystem Notification

## Issue: TC-8040 -- CVE-2026-31812 quinn-proto

**Unsupported ecosystem**: Go modules is not yet supported for automated triage. Manual assessment is required.

### Details

The ecosystem detection for the vulnerable library **quinn-proto** resolved to **Go modules**. However, the Ecosystem Mappings tables in the security-matrix.md files for the configured version streams only support the following ecosystems:

| Supported Ecosystem | Category |
|---------------------|----------|
| Cargo | Source dependency |
| RPM | System package |

**Go modules** does not appear in the Ecosystem Mappings table for any configured stream (2.1.x or 2.2.x). Without a mapping entry, the skill cannot determine:

- Which repository contains the Go module dependency
- Which lock file to inspect (e.g., `go.sum`)
- Which `git show` check command to use for version extraction
- Which upstream branch to check for fix availability

### Recommended Actions

1. **Manual assessment**: An engineer should manually verify whether quinn-proto (or its Go module equivalent) is present in the product's Go dependency tree and determine the version impact across supported product versions.

2. **Add Go modules to Ecosystem Mappings**: If Go module dependencies are part of the product build, update each stream's `security-matrix.md` to add a Go modules row to the Ecosystem Mappings table with the appropriate repository, lock file path (`go.sum`), check command, and upstream branch.

3. **Re-run triage**: After adding Go modules support to the Ecosystem Mappings, re-run `/sdlc-workflow:triage-security TC-8040` to complete automated triage.

### Triage Status

Automated triage has been **stopped** at Step 1 (Ecosystem Detection). No version impact analysis, Affects Versions correction, or remediation task creation has been performed. The issue remains in its current state in Jira.
