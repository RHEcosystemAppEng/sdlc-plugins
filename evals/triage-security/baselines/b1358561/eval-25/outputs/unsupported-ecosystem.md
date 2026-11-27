# Unsupported Ecosystem Notification: TC-8040

> "**Unsupported ecosystem**: Go modules is not yet supported for automated triage.
> Manual assessment is required."

## Details

| Item | Value |
|---|---|
| Issue | TC-8040 |
| CVE | CVE-2026-31812 |
| Vulnerable library | quinn-proto (affected < 0.11.14, fixed in 0.11.14) |
| Issue stream scope | 2.2.x (`[rhtpa-2.2]`) |
| Detected ecosystem | Go modules |
| Supported ecosystems (Ecosystem Mappings) | 2.1.x: Cargo, RPM. 2.2.x: Cargo, RPM |

Go modules is not listed in the Ecosystem Mappings table of either stream's `security-matrix.md`. No lock file or check command is configured for it, so the skill cannot check dependency versions at the pinned commits. Automated triage for this ecosystem **has stopped**.

## What was not done

- No version impact analysis (Step 2). No lock files were inspected, and no affected/not-affected decision was made for any version.
- No Affects Versions correction (Step 3). The current value **RHTPA 2.0.0** is left unchanged, though it looks inconsistent with the `[rhtpa-2.2]` suffix.
- No duplicate, lifecycle, already-fixed, concurrent-triage, or release Jira checks (Steps 4–7.5).
- No remediation tasks, comments, labels (`ai-cve-triaged`), or other Jira mutations.

## Suggested next steps

1. **Manually assess** whether the 2.2.x releases (2.2.0–2.2.4, plus the development stream) ship the vulnerable dependency. Use the Go module files (`go.mod` / `go.sum`) at each pinned commit from the supportability matrix.
2. **Check the ecosystem detection.** The library is quinn-proto, a Rust crate with a RUSTSEC advisory, and Cargo *is* supported in both streams. If the Go modules result was wrong, re-run triage and it will proceed through the Cargo path.
3. **Or add Go modules support.** Add a row to each stream's Ecosystem Mappings table (Repository, Lock File, e.g. `go.sum`, Check Command, Upstream Branch). Define its category (source dependency) in the skill's ecosystem classification table, then re-run `/sdlc-workflow:triage-security TC-8040`.
4. Note that the due date (2026-07-15) has passed, and the security matrix is 152 days old (Last-Updated 2026-06-28). Refresh it before any re-run.
