# Unsupported Ecosystem Notification

## Issue: TC-8040

**CVE**: CVE-2026-31812
**Library**: quinn-proto
**Detected Ecosystem**: Go modules
**Stream**: 2.2.x

---

**Unsupported ecosystem**: Go modules is not yet supported for automated triage. Manual assessment is required.

---

## Detail

Ecosystem detection for the vulnerable library `quinn-proto` (component `pscomponent:org/rhtpa-server`) resolved to **Go modules**. However, the Ecosystem Mappings table for stream **2.2.x** (and all configured version streams) only includes the following ecosystems:

| Ecosystem | Repository | Lock File | Check Command | Upstream Branch |
|-----------|------------|-----------|---------------|-----------------|
| Cargo | backend | `Cargo.lock` | `git show <tag>:Cargo.lock` | `release/0.4.z` |
| RPM | -- | `rpms.lock.yaml` | `git show <tag>:rpms.lock.yaml` | -- |

Since **Go modules** does not appear in any stream's Ecosystem Mappings table, the skill cannot determine:

- Which lock file to inspect (e.g., `go.sum`, `go.mod`)
- Which check command to run for dependency version extraction
- Which upstream branch to check for fix status

## Required Action

Automated version impact analysis (Step 2), remediation task creation (Step 8), and all dependent triage steps cannot proceed for this ecosystem. The following manual steps are required:

1. **Manual dependency assessment** -- Determine whether the vulnerable library (`quinn-proto` versions before 0.11.14) is present in the product's Go module dependency tree for each supported version in stream 2.2.x.
2. **Manual version impact analysis** -- If the library is present, check each supported version's dependency version against the fix threshold (0.11.14).
3. **Manual remediation** -- If affected versions are found, create remediation tasks manually or add the Go modules ecosystem to the Ecosystem Mappings table in `security-matrix.md` and re-run `/triage-security TC-8040`.

## How to Add Ecosystem Support

To enable automated triage for Go modules in future, add a row to each stream's `security-matrix.md` Ecosystem Mappings table:

```
| Go modules | <repository> | <lock-file-path> | <check-command> | <upstream-branch> |
```

For example:

```
| Go modules | backend | go.sum | git show <tag>:go.sum | main |
```

After adding the ecosystem mapping, re-run the triage:

```
/sdlc-workflow:triage-security TC-8040
```

Automated triage has been stopped at Step 1 (Ecosystem Detection). No Jira mutations, version impact analysis, or remediation tasks have been created.
