# Unsupported Ecosystem Notification

## Triage Halted: TC-8001 (CVE-2026-31812)

**Unsupported ecosystem**: Go modules is not yet supported for automated triage. Manual assessment is required.

### Context

- **CVE**: CVE-2026-31812
- **Library**: quinn-proto
- **Detected ecosystem**: Go modules
- **Configured ecosystems** (from security-matrix.md Ecosystem Mappings):
  - **Cargo** -- Rust crates, lock file `Cargo.lock`
  - **RPM** -- System packages, lock file `rpms.lock.yaml`

### Why triage cannot proceed

The triage-security skill determines the ecosystem from the vulnerable library name and component context, then looks up the corresponding lock file path, check command, and upstream branch from the Ecosystem Mappings table in the stream's security-matrix.md. The detected ecosystem "Go modules" does not appear in the Ecosystem Mappings table for either configured version stream (2.1.x or 2.2.x). Without this mapping, the skill cannot:

1. Identify which lock file to inspect for dependency versions
2. Determine the correct `git show` command to extract pinned versions
3. Classify the remediation task structure (source dependency vs. system package)
4. Proceed with version impact analysis (Step 2)

### Required action

To enable automated triage for Go modules vulnerabilities:

1. Add a "Go modules" row to the Ecosystem Mappings table in each stream's security-matrix.md, specifying:
   - Repository name
   - Lock file path (e.g., `go.sum` or `go.mod`)
   - Check command (e.g., `git show <tag>:go.sum`)
   - Upstream branch
2. Update the ecosystem classification table to define whether Go modules is a source dependency or system package ecosystem
3. Re-run `/triage-security TC-8001`

Alternatively, perform manual version impact analysis for this CVE by inspecting the relevant Go dependency files in each supported version's pinned source commits.
