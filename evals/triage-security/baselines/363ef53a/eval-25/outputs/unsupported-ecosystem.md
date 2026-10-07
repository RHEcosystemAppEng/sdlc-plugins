# Unsupported Ecosystem Notification: TC-8040

## Triage Halted -- Unsupported Ecosystem

**Unsupported ecosystem**: Go modules is not yet supported for automated triage. Manual assessment is required.

### Context

- **Issue**: TC-8040
- **CVE**: CVE-2026-31812
- **Vulnerable library**: quinn-proto (versions before 0.11.14)
- **Detected ecosystem**: Go modules
- **Stream scope**: 2.2.x

### Why Triage Stopped

The triage-security skill determines the ecosystem from the vulnerable library name and component context. For TC-8040, the ecosystem detection resolved to **Go modules**. However, the 2.2.x stream's `security-matrix.md` Ecosystem Mappings table only lists the following ecosystems:

- **Cargo** -- Rust crates (lock file: `Cargo.lock`)
- **RPM** -- System packages (lock file: `rpms.lock.yaml`)

Go modules is not present in this table. Without an Ecosystem Mappings entry, the skill cannot determine:

1. Which **lock file** to inspect (e.g., `go.sum`, `go.mod`)
2. Which **check command** to use for extracting dependency versions
3. Which **upstream branch** to check for fix status

### Required Actions

To enable automated triage for Go modules, the following steps are needed:

1. **Add a Go modules row** to the Ecosystem Mappings table in the stream's `security-matrix.md`:

   | Ecosystem | Repository | Lock File | Check Command | Upstream Branch |
   |-----------|------------|-----------|---------------|-----------------|
   | Go modules | backend | `go.sum` | `git show <tag>:go.sum \| grep '<library>'` | `release/0.4.z` |

2. **Update the ecosystem classification table** in the skill definition to categorize Go modules as either a source dependency ecosystem (2 remediation tasks per stream) or a system package ecosystem (1 task per stream).

3. **Re-run triage** for TC-8040 after the Ecosystem Mappings are updated.

### Alternative: Manual Assessment

If adding Go modules support is not immediately feasible, perform manual assessment:

- Inspect the lock files manually to determine if `quinn-proto` is present as a Go dependency
- Check the version against the affected range (< 0.11.14)
- Create remediation tasks manually if affected versions are found
