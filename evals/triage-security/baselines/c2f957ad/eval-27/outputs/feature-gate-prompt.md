# Feature-Gated Dependency: VEX Justification Prompt (TC-8051)

This prompt comes from the dependency scope decision tree in Step 2.3.5. It is shown to the engineer **before any remediation tasks are created**.

---

> The vulnerable dependency `rustls` is gated behind the `tls-rustls` feature, which is not enabled by default. Recommended VEX justification: **Vulnerable Code not in Execute Path**.
>
> Options:
> 1. Skip remediation — apply VEX justification and close as not affected
> 2. Proceed with remediation — create tasks despite the feature gate
>
> Choose (1/2):

---

## Supporting Context Shown With the Prompt

| Item | Value |
|------|-------|
| CVE | CVE-2026-99002 (rustls < 0.23.5, CVSS 8.1 High, certificate validation bypass) |
| Issue / scope | TC-8051, stream 2.2.x (`[rhtpa-2.2]`) |
| Locked version | rustls 0.23.4 in 2.2.0, 2.2.1, 2.2.2 (retag of 2.2.1), 2.2.3, 2.2.4 |
| Declaration | `backend/Cargo.toml`: `rustls = { version = "0.23.4", optional = true }` |
| Feature gate | `tls-rustls = ["dep:rustls"]` (non-default) |
| Default features | `default = ["tls-native"]`, so native-tls is used and rustls is not compiled |
| Other streams | 2.1.x does not have rustls in its lock file, so no cross-stream impact |
| VEX field | customfield_12345 (configured) |

## What Happens Next

- **Option 1:** all in-scope 2.2.x versions are marked not affected. No other stream is affected, so the recommendation is to close TC-8051 as **Not a Bug** with VEX Justification (customfield_12345) = **Vulnerable Code not in Execute Path**. Before running it, the engineer confirms a separate close recommendation covering the comment with the version impact table and footnote, the transition to Closed with resolution "Not a Bug", the VEX field, and the `ai-cve-triaged` label.
- **Option 2:** Case B applies. Create 2 standard Cargo remediation tasks for 2.2.x: dependency bump or upstream backport on `release/0.4.z` to rustls >= 0.23.5, plus downstream propagation in `rhtpa-release.0.4.z` (Blocks). Both link to TC-8051 with "Depend" and get **no** label or priority changes. Affects Versions is corrected to RHTPA 2.2.0 through 2.2.4.

## Notes for the Engineer

- Before choosing option 1, confirm that the Konflux build of `rhtpa-server` does not enable `tls-rustls` (for example through `--features tls-rustls` or `--all-features`). The fixtures show only the manifest defaults.
- The SKILL.md VEX table maps feature-flag cases to "Vulnerable Code not Present". The feature-gated decision tree in `version-impact-analysis.md` says to recommend **"Vulnerable Code not in Execute Path"**. This prompt follows the decision tree, which is the more specific procedure.
- No Jira mutation has been made. This eval writes to files only.
