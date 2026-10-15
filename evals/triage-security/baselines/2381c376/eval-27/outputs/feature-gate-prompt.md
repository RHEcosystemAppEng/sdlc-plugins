# Feature-Gated Dependency -- VEX Justification Prompt

## Context

CVE-2026-99002 affects `rustls` versions before 0.23.5. All 2.2.x product versions ship rustls 0.23.4 in the Cargo.lock, which is within the affected range.

However, `rustls` is an **optional dependency** gated behind the non-default `tls-rustls` feature flag. The product's default feature set is `["tls-native"]`, which uses `native-tls` instead. The `tls-rustls` feature must be explicitly enabled by a consumer to compile and link the `rustls` crate into the binary.

Under the default build configuration that the product ships with, `rustls` code is not included in the production binary.

## VEX Justification Prompt

The vulnerable dependency `rustls` is gated behind the `tls-rustls` feature, which is not enabled by default. Recommended VEX justification: **Vulnerable Code not in Execute Path**.

Options:
1. **Skip remediation** -- apply VEX justification and close as not affected
2. **Proceed with remediation** -- create tasks despite the feature gate

Choose (1/2):

## Rationale for Recommended Justification

| VEX Justification Value | Applicability |
|--------------------------|---------------|
| Component not Present | Not applicable -- rustls IS present in the Cargo.lock; it is a declared optional dependency |
| Vulnerable Code not Present | Partially applicable -- the code is conditionally compiled only when the feature is enabled |
| **Vulnerable Code not in Execute Path** | **Recommended** -- the dependency exists in the manifest but is behind a non-default feature gate; the shipped product does not enable or execute this code path |
| Inline Mitigations already Exist | Not applicable -- no runtime mitigations are in place |

The recommended justification is **Vulnerable Code not in Execute Path** because:
- The `rustls` crate is declared as `optional = true` in the Cargo manifest
- The `tls-rustls` feature that activates it is **not** in the default feature set
- The product ships with `tls-native` as the default TLS backend
- Under the default configuration, rustls code is never compiled into or executed by the product binary

## Proposed Actions (if user chooses option 1 -- Skip remediation)

The following Jira mutations would be proposed (not executed):

1. **Set VEX Justification field** (`customfield_12345`) to "Vulnerable Code not in Execute Path" on TC-8051
2. **Add comment** to TC-8051:
   > "No remediation required. The vulnerable dependency `rustls` (< 0.23.5) is an optional dependency gated behind the non-default `tls-rustls` feature flag. The product ships with `tls-native` enabled by default; `rustls` code is not compiled into or executed by the shipped binary.
   >
   > VEX justification: Vulnerable Code not in Execute Path.
   >
   > Version impact: all 2.2.x versions ship rustls 0.23.4, but the dependency is feature-gated and inactive under the default build profile."
3. **Transition** TC-8051 to Closed with resolution "Not a Bug"
4. **Add label** `ai-cve-triaged` to TC-8051

## Proposed Actions (if user chooses option 2 -- Proceed with remediation)

Standard Case B remediation would proceed: create two tasks per affected stream (dependency bump + downstream propagation) for the 2.2.x stream. No label or priority modifications (feature-gated dependencies that proceed to remediation are treated as standard, unlike dev-only dependencies which get `dev-dependency` label and Normal priority).
