# Feature-Gated Dependency: VEX Justification Prompt (TC-8051)

Shown to the engineer after Step 2.3.5 and **before any remediation tasks are created**. It follows the "Feature-gated optional dependencies" branch of the dependency scope decision tree.

---

> The vulnerable dependency `rustls` is gated behind the `tls-rustls`
> feature, which is not enabled by default. Recommended VEX justification:
> **Vulnerable Code not in Execute Path**.
>
> Options:
> 1. Skip remediation — apply VEX justification and close as not affected
> 2. Proceed with remediation — create tasks despite the feature gate
>
> Choose (1/2):

---

## Supporting Evidence

| Item | Detail |
|------|--------|
| CVE | CVE-2026-99002 (CVSS 8.1 High): rustls < 0.23.5, certificate validation bypass |
| Issue scope | 2.2.x (`[rhtpa-2.2]`) |
| Versions in scope | 2.2.0, 2.2.1, 2.2.2 (retag of 2.2.1), 2.2.3, 2.2.4. All have rustls 0.23.4 in `Cargo.lock` |
| Declaration | `rustls = { version = "0.23.4", optional = true }` in backend/Cargo.toml |
| Gate | `tls-rustls = ["dep:rustls"]`, which is **not** in `default` |
| Default features | `default = ["tls-native"]` → native-tls. The product ships with native-tls, not rustls |
| Introduced | 2.2.0 (backend v0.4.5), as an alternative TLS backend |

## What Each Choice Does (no actions taken in this eval)

**Option 1: Skip remediation (VEX)**
- All in-scope 2.2.x versions are marked not affected with VEX justification **"Vulnerable Code not in Execute Path"**.
- No 2.2.x version is affected, and 2.1.x does not contain rustls, so the whole issue is closed under Case C: a comment with the version impact table and feature-gate rationale, a transition to Closed with resolution "Not a Bug", and `customfield_12345` (VEX Justification) set to "Vulnerable Code not in Execute Path".
- Affects Versions (currently RHTPA 2.2.0) is handled according to Step 3 for a not-affected outcome.
- The post-triage `ai-cve-triaged` label and summary comment are then applied.

**Option 2: Proceed with remediation**
- Standard Cargo source-dependency remediation for 2.2.x, linked "Depend" to TC-8051:
  1. Upstream task in rhtpa-backend, branch `release/0.4.z`: bump the direct optional dependency rustls to >= 0.23.5 in backend/Cargo.toml and Cargo.lock. If Step 2.5 shows HEAD already has the fix, use the dependency-bump variant instead.
  2. Downstream propagation subtask in rhtpa-release.0.4.z: update the backend tag pin in `artifacts.lock.yaml` to the fixed tag. Linked "Blocks" from the upstream task.
- **No** `dev-dependency` label and **no** priority override. The tasks use standard priority handling.
- Coordination guidance uses deployment context `upstream`.

Every Jira mutation in either path still needs the confirmation gate.
