# Unsupported Ecosystem Notification: TC-8040

> "**Unsupported ecosystem**: Go modules is not yet supported for automated triage.
> Manual assessment is required."

## Details

| Item | Value |
|------|-------|
| Issue | TC-8040 |
| CVE | CVE-2026-31812 |
| Vulnerable library | quinn-proto (affected < 0.11.14, fixed in 0.11.14) |
| Issue stream scope | 2.2.x (`[rhtpa-2.2]`) |
| Detected ecosystem | Go modules |
| Supported ecosystems (2.1.x, `rhtpa-release.0.3.z`) | Cargo, RPM |
| Supported ecosystems (2.2.x, `rhtpa-release.0.4.z`) | Cargo, RPM |

Go modules is not in the Ecosystem Mappings table of any configured stream's
`security-matrix.md`, so the skill has:

- no lock file path (for example `go.sum` / `go.mod`) to inspect at pinned commits,
- no check command for pulling dependency versions,
- no classification (source dependency or system package), so it cannot work out how many
  remediation tasks are needed per stream.

Without these, the skill cannot build a version impact table from evidence. The
skill does not invent dependency versions, so automated triage of this ecosystem
**stops here**.

## What was and was not done

- Step 0 (configuration validation) and Step 1 (data extraction, stream scope, ecosystem
  detection) finished. See `data-extraction.md`.
- **Not run:** Steps 1.5, 1.7, 2, 3, 4, 5, 6, 7, 7.5, 8.
- **No Jira changes were proposed or made.** Affects Versions, labels, links, comments, and
  status are unchanged by this triage. The `ai-cve-triaged` label was **not** added.

## Recommended manual next steps

1. **Check the ecosystem.** The description and references (RUSTSEC-2026-0042, the
   quinn-rs/quinn upstream PR, the "crate" wording) point to a Rust/Cargo library. If the
   Go modules result is wrong, re-run `/sdlc-workflow:triage-security TC-8040` with the
   right ecosystem. Cargo is supported in both streams.
2. **If the component really is Go**, assess it by hand: read `go.sum` / `go.mod` at the pinned
   source tags for every supported version (2.1.0, 2.1.1, 2.2.0 to 2.2.4, and the development
   stream at branch HEAD) and compare against the fix threshold (0.11.14).
3. **Fix Affects Versions by hand** once you know the impact. The current value is
   `RHTPA 2.0.0`, which does not match the issue's 2.2.x scope.
4. **To support Go modules in future**, add a `Go modules` row (lock file, check command,
   upstream branch) to each stream's `security-matrix.md` Ecosystem Mappings table. Then add
   Go modules to the skill's ecosystem classification table (likely "Source dependency").
5. **Separate warning:** both stream matrices were last updated 2026-06-28, 131 days ago.
   Consider refreshing them via `/setup` (Step 10.6) before the next triage.
6. **Due date passed:** the issue due date (2026-07-15) has already passed.

Would you like to stop here, or re-run triage with a different ecosystem?
