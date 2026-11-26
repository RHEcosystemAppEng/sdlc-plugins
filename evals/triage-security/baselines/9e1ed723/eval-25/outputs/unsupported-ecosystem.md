# Unsupported Ecosystem Notification: TC-8040

> "**Unsupported ecosystem**: Go modules is not yet supported for automated triage.
> Manual assessment is required."

## Details

| Item | Value |
|------|-------|
| Issue | TC-8040 |
| CVE | CVE-2026-31812 |
| Vulnerable library | quinn-proto (affected < 0.11.14, fixed in 0.11.14) |
| Issue stream scope | 2.2.x (from summary suffix `[rhtpa-2.2]`) |
| Detected ecosystem | Go modules |
| Supported ecosystems (2.2.x Ecosystem Mappings) | Cargo, RPM |
| Supported ecosystems (2.1.x Ecosystem Mappings) | Cargo, RPM |

Automated triage stopped at **Step 1 (Ecosystem detection)**. Neither stream's
`security-matrix.md` Ecosystem Mappings table has a Go modules row. Without that row
there is no lock file path, check command, or upstream branch to use for Step 2 (Version
Impact Analysis). Go modules is also missing from the ecosystem classification table, so
the skill cannot work out the remediation task structure for Step 8.

## What was not done

- No version impact analysis. No lock files were inspected, and no affected or unaffected
  verdict was reached for any version.
- No Affects Versions correction. The current value is `RHTPA 2.0.0`. It does not match
  the 2.2 stream scope and should be reviewed during manual assessment.
- No duplicate/sibling, lifecycle, already-fixed, or concurrent-triage checks.
- No remediation tasks were created and no Jira comments were posted.
- The `ai-cve-triaged` label was **not** added. The issue stays in the untriaged queue.

## Recommended next steps (manual)

1. Confirm the ecosystem. The library name `quinn-proto` and the RUSTSEC-2026-0042
   reference point to a Rust crate (Cargo), which *is* supported. If Go modules was a
   misclassification, re-run `/sdlc-workflow:triage-security TC-8040` once the
   ecosystem is confirmed as Cargo.
2. If the component really does ship a Go module dependency, assess it by hand. For
   each supported version in streams 2.1.x and 2.2.x, check `go.sum`/`go.mod` at the
   pinned commit from the supportability matrix, and the branch HEAD for the
   development stream.
3. To support Go modules in future triages, add a `Go modules` row (repository,
   `go.sum` lock file, check command, upstream branch) to each stream's
   `security-matrix.md` Ecosystem Mappings table. Also add Go modules to the skill's
   ecosystem classification table, most likely as a source dependency.
4. Separately, the security matrix is stale. It was last updated on 2026-06-28, 148 days
   ago, against a 14-day threshold. Refresh it (`/setup` Step 10.6) before re-running
   triage.
