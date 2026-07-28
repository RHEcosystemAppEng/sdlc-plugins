# VEX Justification Prompt -- Feature-Gated Dependency

## Dependency Scope Decision Tree Result

Step 2.3.5 identified **rustls** as a feature-gated optional dependency
behind the non-default **tls-rustls** feature flag. The default features
do NOT include `tls-rustls` -- the product ships with the `tls-native`
feature enabled by default, meaning rustls code is not compiled into or
executed by the default production binary.

Per the dependency scope decision tree for feature-gated optional
dependencies, the following VEX justification prompt is presented to the
engineer before proceeding:

---

## Prompt Presented to the Engineer

> The vulnerable dependency **rustls** is gated behind the **tls-rustls**
> feature, which is not enabled by default. Recommended VEX justification:
> **Vulnerable Code not in Execute Path**.
>
> Options:
> 1. **Skip remediation** -- apply VEX justification and close as not affected
> 2. **Proceed with remediation** -- create tasks despite the feature gate
>
> Choose (1/2):

---

## Option 1: Skip Remediation

If the engineer chooses option 1:

- The affected versions are closed as **not affected** with VEX
  justification **Vulnerable Code not in Execute Path**
- No remediation tasks are created for these versions
- If the VEX Justification custom field is configured (customfield_12345
  in this project), it is set to "Vulnerable Code not in Execute Path"
- The overall issue closure depends on whether other versions outside
  this scope are also affected. Since all 2.2.x versions have rustls
  behind the non-default feature gate, and the issue is scoped to the
  2.2.x stream only, the recommendation would be:

  **Proposed action**: Close TC-8051 as Not a Bug with resolution
  "Not a Bug" and VEX Justification "Vulnerable Code not in Execute
  Path".

  **Proposed comment**:
  > No supported 2.2.x versions ship rustls in the default build
  > configuration. The rustls dependency is gated behind the non-default
  > `tls-rustls` feature flag -- the product ships with `tls-native`
  > enabled by default. The vulnerable code path is not in the execute
  > path for the default product configuration.
  >
  > Version impact analysis:
  > | Version | rustls | Affected? | Feature Gate |
  > |---------|--------|-----------|-------------|
  > | 2.2.0 | 0.23.4 | YES (gated) | tls-rustls (non-default) |
  > | 2.2.1 | 0.23.4 | YES (gated) | tls-rustls (non-default) |
  > | 2.2.2 | -- | YES (gated) | retag of 2.2.1 |
  > | 2.2.3 | 0.23.4 | YES (gated) | tls-rustls (non-default) |
  > | 2.2.4 | 0.23.4 | YES (gated) | tls-rustls (non-default) |
  >
  > VEX Justification: Vulnerable Code not in Execute Path

  **Proposed Jira mutations** (require engineer confirmation):
  1. Set VEX Justification (customfield_12345) to "Vulnerable Code not in Execute Path"
  2. Add comment with version impact evidence and VEX justification
  3. Transition TC-8051 to Closed with resolution "Not a Bug"
  4. Add label `ai-cve-triaged`

## Option 2: Proceed with Standard Remediation

If the engineer chooses option 2:

- Standard remediation tasks are created without label or priority modifications
- Two tasks per stream (Cargo source dependency ecosystem):
  1. **Upstream backport task**: Bump rustls to >= 0.23.5 in rhtpa-backend
     on branch release/0.4.z
  2. **Downstream propagation subtask**: Update rhtpa-backend reference in
     rhtpa-release.0.4.z (blocked by upstream task)
- Labels: `["ai-generated-jira", "Security", "CVE-2026-99002"]`
- Link type: "Depend" to TC-8051
- No `dev-dependency` label or priority override (those apply to dev-only
  dependencies, not feature-gated ones)

---

## Key Context for the Decision

| Attribute | Value |
|-----------|-------|
| Library | rustls |
| Feature flag | tls-rustls |
| Default features | tls-native (rustls NOT included) |
| Shipped rustls version | 0.23.4 (all 2.2.x versions) |
| Fix threshold | 0.23.5 |
| Recommended VEX justification | Vulnerable Code not in Execute Path |
| Decision owner | Engineer (this is a confirmation gate, not an automated decision) |
