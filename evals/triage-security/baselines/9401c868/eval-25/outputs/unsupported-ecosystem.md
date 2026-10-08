# Unsupported Ecosystem Notification

## Issue: TC-8040

**CVE**: CVE-2026-31812
**Library**: quinn-proto
**Detected Ecosystem**: Go modules
**Scoped Stream**: 2.2.x (rhtpa-release.0.4.z)

---

## Notification

**Unsupported ecosystem**: Go modules is not yet supported for automated triage. Manual assessment is required.

The detected ecosystem "Go modules" does not appear in the Ecosystem Mappings table for any configured version stream. The Ecosystem Mappings tables in the security matrix currently support:

- **Cargo** -- Rust crates, checked via `Cargo.lock`
- **RPM** -- System packages, checked via `rpms.lock.yaml`

"Go modules" is not listed, so the skill cannot determine which lock file to inspect, which parsing command to use, or how to structure remediation tasks for this ecosystem.

## Required Manual Steps

1. **Verify ecosystem classification**: Confirm whether the affected library (quinn-proto) truly belongs to the Go modules ecosystem, or whether ecosystem detection resolved incorrectly. Note: quinn-proto is typically a Rust crate in the Cargo ecosystem. If ecosystem detection is wrong, re-run triage with the correct ecosystem.

2. **If Go modules is correct**: Perform manual version impact analysis by:
   - Identifying the Go module lock file (e.g., `go.sum` or `go.mod`) in the affected repository
   - Checking the pinned version of quinn-proto at each release tag
   - Comparing against the fix threshold (0.11.14)

3. **To enable automated triage for Go modules in the future**: Add a "Go modules" row to the Ecosystem Mappings table in each stream's `security-matrix.md`, specifying:
   - Repository name
   - Lock file path (e.g., `go.sum`)
   - Check command (e.g., `git show <tag>:go.sum`)
   - Upstream branch
   - Update the ecosystem classification table in the skill to define whether Go modules is a "Source dependency" or "System package" category

## Triage Status

- **Step completed**: Step 1 (Data Extraction) -- completed successfully
- **Step halted at**: Step 1 (Ecosystem Detection) -- unsupported ecosystem
- **Steps not executed**: Steps 1.5 through 8 (External CVE Enrichment, Embargo Check, Version Impact Analysis, Affects Versions Correction, Duplicate Check, Lifecycle Check, Already Fixed Check, Concurrent Triage Detection, Release Jira Orchestration, Remediation)
- **Jira mutations performed**: None
- **Automated triage outcome**: Halted -- manual assessment required
