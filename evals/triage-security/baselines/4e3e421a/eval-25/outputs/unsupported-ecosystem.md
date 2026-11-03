# Unsupported Ecosystem Notification: TC-8040

> **Unsupported ecosystem**: Go modules is not yet supported for automated triage.
> Manual assessment is required.

## Details

| Item | Value |
|------|-------|
| Issue | TC-8040 (mock data key TC-8001) |
| CVE | CVE-2026-31812 |
| Vulnerable library | quinn-proto (affected < 0.11.14, fixed in 0.11.14) |
| Issue stream scope | 2.2.x (`[rhtpa-2.2]`) |
| Detected ecosystem | **Go modules** |
| Supported ecosystems (stream 2.2.x Ecosystem Mappings) | Cargo, RPM |
| Supported ecosystems (stream 2.1.x Ecosystem Mappings) | Cargo, RPM |

## Why automated triage stopped

The stream `security-matrix.md` Ecosystem Mappings tables decide which lock file to
inspect and which check command to run for each ecosystem. Go modules has no row in
either stream's table. As a result:

- No lock file path (e.g. `go.sum`) or check command is configured, so version
  impact analysis (Step 2) cannot run against pinned commits.
- Go modules is not in the ecosystem classification table, so the remediation task
  structure (2 tasks for a source dependency, 1 for a system package) is undefined.
- The skill does not guess dependency versions or invent a lock-file procedure.

Automated triage **stopped at Step 1 (Ecosystem detection)**. No later steps ran.

## Jira state: no changes made

- Affects Versions left as is (currently `RHTPA 2.0.0`. This does not match the
  PSIRT-claimed `rhtpa-2.2` stream and should be checked during manual assessment.)
- No `ai-cve-triaged` label added. The issue stays in the untriaged list.
- No remediation tasks, links, or comments created.

## Recommended next steps (manual)

1. **Assess manually**: for each supported 2.2.x version (2.2.0–2.2.4, where 2.2.2 is a
   backend retag of 2.2.1), check the Go module dependency at the pinned source tag.
   For example, inspect `go.sum` / `go.mod` read-only and compare against the affected
   range `< 0.11.14`. Also check the development stream at branch HEAD.
2. **Confirm the ecosystem**: `quinn-proto` and the RUSTSEC-2026-0042 reference suggest
   a Rust/Cargo crate. If Go modules was detected by mistake, re-run
   `/sdlc-workflow:triage-security TC-8040` once the ecosystem resolves to Cargo, which
   is supported.
3. **Add Go modules support (optional)**: add a `Go modules` row (Repository, Lock File
   such as `go.sum`, Check Command such as `git show <tag>:go.sum`, Upstream Branch) to
   each stream's Ecosystem Mappings table. Then add Go modules to the skill's ecosystem
   classification table (likely category: Source dependency, 2 tasks per stream).
4. **Refresh the matrix**: the security matrix was last updated 2026-06-28 (128 days
   ago). Run `/setup` (Step 10.6) before re-running triage.
