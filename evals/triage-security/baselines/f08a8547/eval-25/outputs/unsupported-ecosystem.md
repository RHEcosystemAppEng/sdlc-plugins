# Unsupported Ecosystem Notification

## Issue: TC-8040 -- CVE-2026-31812 quinn-proto

**Unsupported ecosystem**: Go modules is not yet supported for automated triage. Manual assessment is required.

### Context

- **CVE**: CVE-2026-31812
- **Vulnerable library**: quinn-proto
- **Detected ecosystem**: Go modules
- **Stream in scope**: 2.2.x (rhtpa-release.0.4.z)

### Supported Ecosystems for This Stream

The Ecosystem Mappings table in the 2.2.x stream's security-matrix.md lists the following supported ecosystems:

| Ecosystem | Category | Lock File | Remediation Tasks per Stream |
|-----------|----------|-----------|------------------------------|
| Cargo | Source dependency | `Cargo.lock` | 2 (upstream backport + downstream propagation) |
| RPM | System package | `rpms.lock.yaml` | 1 (Konflux release repo fix only) |

"Go modules" does not appear in this table and has no configured lock file path, check command, or upstream branch mapping.

### Why Triage Is Halted

Automated version impact analysis (Step 2) requires a configured lock file path and check command to determine which product versions ship the vulnerable dependency. Without an Ecosystem Mappings entry for Go modules, the skill cannot:

1. Identify which lock file to inspect (e.g., `go.sum`, `go.mod`)
2. Determine the correct `git show` command to extract dependency versions at pinned commits
3. Map the ecosystem to its remediation category (source dependency vs. system package)
4. Generate properly structured remediation tasks

### Recommended Actions

1. **Manual assessment**: An engineer should manually inspect the relevant lock files and determine whether any supported product versions ship a vulnerable version of quinn-proto via Go modules.
2. **Add ecosystem support**: If Go modules dependencies are present in this product, consider adding a Go modules row to the Ecosystem Mappings table in the stream's `security-matrix.md` via `/setup` (Step 10.6), specifying the lock file path (`go.sum`), check command, and upstream branch.
3. **Re-run triage**: After adding Go modules to the Ecosystem Mappings table, re-run `/sdlc-workflow:triage-security TC-8040` for automated triage.
