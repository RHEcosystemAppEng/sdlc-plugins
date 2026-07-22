# Unsupported Ecosystem Notification

## Issue: TC-8040

**CVE**: CVE-2026-31812
**Library**: quinn-proto
**Detected Ecosystem**: Go modules
**Stream**: 2.2.x

---

**Unsupported ecosystem**: Go modules is not yet supported for automated triage. Manual assessment is required.

---

## Details

The triage-security skill determines the ecosystem from the vulnerable library name and component context, then validates it against the Ecosystem Mappings table in the stream's `security-matrix.md`. The 2.2.x stream's Ecosystem Mappings table lists the following supported ecosystems:

- **Cargo** -- Rust crates (lock file: `Cargo.lock`, check command: `git show <tag>:Cargo.lock`, upstream branch: `release/0.4.z`)
- **RPM** -- System packages (lock file: `rpms.lock.yaml`, check command: `git show <tag>:rpms.lock.yaml`)

The detected ecosystem **Go modules** does not appear in this table. Without a configured lock file path and check command for Go modules, the skill cannot:

1. Extract dependency versions from lock files at pinned commits (Step 2.3)
2. Build a version impact table (Step 2.4)
3. Perform Affects Versions correction (Step 3)
4. Create remediation tasks with the correct lock file references (Step 8)

## Recommended Actions

1. **Manual assessment** -- An engineer should manually inspect the Go module dependency (e.g., `go.sum` or `go.mod`) at each pinned commit in the supportability matrix to determine version impact.
2. **Add Go modules to Ecosystem Mappings** -- If Go modules are a recurring ecosystem for this product, update the `security-matrix.md` files for each stream to include a Go modules row in the Ecosystem Mappings table:
   ```
   | Go modules | <repository> | go.sum | git show <tag>:go.sum | <upstream-branch> |
   ```
   Then re-run `/triage-security TC-8040` to perform automated triage.
3. **Contact ProdSec** -- If the ecosystem classification is incorrect (e.g., quinn-proto is actually a Cargo crate, not a Go module), verify the ecosystem detection and re-run triage with the correct classification.

## Triage Status

Automated triage is **halted** at Step 1 (Ecosystem Detection). No Jira mutations have been performed. The issue remains in its current state (New, Unassigned, Affects Versions: RHTPA 2.0.0).
