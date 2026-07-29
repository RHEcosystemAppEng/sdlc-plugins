# Unsupported Ecosystem Notification

## Notification to User

**Unsupported ecosystem**: Go modules is not yet supported for automated triage. Manual assessment is required.

## Context

- **Issue**: TC-8040
- **CVE**: CVE-2026-31812
- **Library**: quinn-proto
- **Detected ecosystem**: Go modules
- **Supported ecosystems** (from Ecosystem Mappings tables):
  - **Cargo** -- Rust crates (lock file: `Cargo.lock`)
  - **RPM** -- System packages (lock file: `rpms.lock.yaml`)

## Why Triage Cannot Proceed

The triage-security skill determines which supported product versions are affected by inspecting lock files at pinned source commits. Each ecosystem has a configured lock file path and check command in the stream's `security-matrix.md` Ecosystem Mappings table. Since "Go modules" is not listed in the Ecosystem Mappings table for any configured version stream (2.1.x or 2.2.x), the skill has no lock file path, check command, or upstream branch configured for this ecosystem.

Without these configuration entries, the skill cannot:

1. Determine which lock file to inspect (e.g., `go.sum` for Go modules)
2. Run the appropriate check command to extract the dependency version
3. Identify the upstream branch for fix verification
4. Classify the ecosystem category (source dependency vs. system package) for remediation task structure

## Recommended Actions

1. **Manual assessment**: An engineer should manually determine whether quinn-proto (Go modules) is present in the affected product versions and at what version.

2. **Add ecosystem support**: To enable automated triage for Go modules in the future, add a row to each stream's `security-matrix.md` Ecosystem Mappings table:

   ```
   | Go modules | <repository> | go.sum | git show <tag>:go.sum \| grep '<library>' | <upstream-branch> |
   ```

   Then update the ecosystem classification table in the skill to define whether Go modules is a "Source dependency" (producing 2 remediation tasks per stream) or another category.

3. **Re-run triage**: After adding Go modules to the Ecosystem Mappings tables, re-run `/sdlc-workflow:triage-security TC-8040` for automated version impact analysis.

## Triage Outcome

Automated triage is **stopped** at Step 1 (Ecosystem Detection). No Jira mutations were performed. The issue remains in its current state (New, Unassigned) pending manual assessment or ecosystem configuration update.
