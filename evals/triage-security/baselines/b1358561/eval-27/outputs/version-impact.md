# Step 2 – Version Impact Analysis: TC-8051 (CVE-2026-99002, rustls < 0.23.5)

The data comes from the fixtures. `security-matrix-mock.md` stands in for both streams' `security-matrix.md` and the `git show <tag>:Cargo.lock` output. `vuln-issue-feature-gated.md` stands in for the manifest inspection in Step 2.3.5. No git or Jira commands were run.

## 2.1 – Matrix load and staleness

- Both streams were loaded (2.1.x = rhtpa-release.0.3.z, 2.2.x = rhtpa-release.0.4.z).
- Format check passed. Supportability Matrix, Ecosystem Mappings, Source Pinning Method, and Forward Pointer are all present, and the Ecosystem Mappings columns match the template.
- **Staleness warning (Step 0.3):** `Last-Updated: 2026-06-28T10:00:00Z` is 152 days before today (2026-11-27), well past the 14-day threshold. In interactive mode the engineer would choose Refresh / Proceed / Stop. This eval proceeds with the current matrix, so releases after 2.2.4 may be missing.

## 2.2 – Development stream

The development stream could not be determined. That requires `getJiraIssueTypeMetaWithFields` to find unreleased RHTPA versions, and Jira calls are prohibited here. No branch-HEAD lock data is in the fixtures, so the dev stream is listed as **not verified** rather than guessed.

## 2.3 / 2.4 – Version impact table

```
Version Impact for CVE-2026-99002 (rustls < 0.23.5):
```

### In scope: 2.2.x stream (issue scope `[rhtpa-2.2]`)

| Version | Build | backend tag | rustls (Cargo.lock) | In affected range? | Affected? | Notes |
|---------|-------|-------------|---------------------|--------------------|-----------|-------|
| 2.2.0 | 0.4.5 | `v0.4.5` | 0.23.4 | YES (< 0.23.5) | YES, feature-gated | Optional dep, non-default `tls-rustls` feature. rustls first appears here. |
| 2.2.1 | 0.4.8 | `v0.4.8` | 0.23.4 | YES | YES, feature-gated | Optional dep, non-default `tls-rustls` feature |
| 2.2.2 | 0.4.9 | `v0.4.8` | — | YES | YES, feature-gated | same as 2.2.1 (backend retag of 2.2.1; lock check skipped, result carried forward) |
| 2.2.3 | 0.4.11 | `v0.4.11` | 0.23.4 | YES | YES, feature-gated | Optional dep, non-default `tls-rustls` feature |
| 2.2.4 | 0.4.12 | `v0.4.12` | 0.23.4 | YES | YES, feature-gated | Optional dep, non-default `tls-rustls` feature |
| dev (unreleased) | — | branch HEAD | not verified | — | not verified | Needs Jira unreleased-version lookup and a HEAD lock read; neither is available in this eval |

### Out of scope (cross-stream context only): 2.1.x stream

| Version | Build | backend tag | rustls (Cargo.lock) | Affected? | Notes |
|---------|-------|-------------|---------------------|-----------|-------|
| 2.1.0 | 0.3.8 | `v0.3.8` | not present | NO | Not in Cargo.lock (only native-tls was available in 2.1.x) |
| 2.1.1 | 0.3.12 | `v0.3.12` | not present | NO | Not in Cargo.lock |

Every shipped 2.2.x lock file has rustls 0.23.4, which is inside the affected range. So the lock file says the vulnerable version is resolved. Cargo records optional dependencies in Cargo.lock even when their feature is off. The manifest shows rustls is compiled only when the non-default `tls-rustls` feature is enabled, which the default product build does not do. **No cross-stream impact:** 2.1.x does not ship rustls, so Case A does not apply.

## 2.3.5 – Dependency chain context

```
Dependency chain for rustls:
  backend (workspace) → rustls
  Type: direct dependency (optional)
  Profile: feature-gated. rustls is declared with optional = true behind the
           non-default feature "tls-rustls". Default features = ["tls-native"]
           (native-tls), so the default/shipped build does NOT compile rustls.

Feature declaration (backend/Cargo.toml, v0.4.5+):
  [dependencies]
  rustls = { version = "0.23.4", optional = true }

  [features]
  default    = ["tls-native"]
  tls-native = ["dep:native-tls"]
  tls-rustls = ["dep:rustls"]

First appeared: 2.2.0 (backend v0.4.5, added as an alternative TLS backend)
Not present in: 2.1.x (only native-tls was available)

Remediation (if pursued): direct dependency, so a simple bump.
  Bump rustls to >= 0.23.5 in backend/Cargo.toml and Cargo.lock
  (e.g. `cargo update -p rustls --precise 0.23.5`) on release/0.4.z, then
  propagate the new backend tag to rhtpa-release.0.4.z.
```

**Scope decision (dependency scope decision tree):** this is a **feature-gated optional dependency**, not dev-only or build-only. Per the decision tree, the engineer must be offered the VEX justification **"Vulnerable Code not in Execute Path"** before any remediation tasks are created. See `feature-gate-prompt.md`. The `dev-dependency` label and the Normal-priority override do **not** apply.

## 2.5 – Upstream fix status

| Stream | Ecosystem | Upstream Branch | Version at HEAD | Fixed? |
|--------|-----------|-----------------|-----------------|--------|
| 2.2.x | Cargo | release/0.4.z | not verified (no branch-HEAD data in fixture; `git -C ... show` not run) | Unknown |

If the engineer goes ahead with remediation, the upstream branch has to be checked first. If it already ships rustls >= 0.23.5, use the dependency bump + downstream propagation variant. If not, use upstream backport + downstream propagation. Either way it is two tasks for 2.2.x.

## Implications for later steps (preview, nothing executed)

- **Step 3 (Affects Versions):** PSIRT set only RHTPA 2.2.0. Lock evidence shows 0.23.4 in 2.2.0 through 2.2.4. If the engineer picks remediation (option 2), the proposed correction is RHTPA 2.2.0, 2.2.1, 2.2.2, 2.2.3, 2.2.4. If the engineer picks the VEX close (option 1), none of the 2.2.x versions is affected in the default build.
- **Step 8:** the outcome depends on the feature-gate prompt. Option 1 gives Case C: close as Not a Bug and set customfield_12345 to "Vulnerable Code not in Execute Path". Option 2 gives Case B: two remediation tasks for 2.2.x with no label or priority changes.

Waiting for the engineer to confirm this table before Step 3.
