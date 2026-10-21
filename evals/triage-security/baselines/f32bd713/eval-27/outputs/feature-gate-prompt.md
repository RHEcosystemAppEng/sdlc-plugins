# Feature-Gate VEX Justification Prompt: CVE-2026-99002

## Context

- **CVE**: CVE-2026-99002
- **Library**: rustls
- **Affected versions**: before 0.23.5
- **Version found**: 0.23.4 (all 2.2.x versions)
- **Feature flag**: `tls-rustls`
- **Default features**: `["tls-native"]` -- does NOT include `tls-rustls`

## Prompt to User

The vulnerable dependency `rustls` is gated behind the `tls-rustls` feature, which is not enabled by default. Recommended VEX justification: **Vulnerable Code not in Execute Path**.

Options:
1. Skip remediation -- apply VEX justification and close as not affected
2. Proceed with remediation -- create tasks despite the feature gate

Choose (1/2):

## Rationale

rustls is declared as an optional dependency (`optional = true`) in the backend workspace's Cargo.toml. It is activated only when the `tls-rustls` feature flag is explicitly enabled. The default feature set is `["tls-native"]`, which uses native-tls instead. Under the default build configuration that the product ships with, rustls is not compiled into the binary and its code paths are never executed.

This matches the VEX justification category **Vulnerable Code not in Execute Path**: the package is present in the lock file (Cargo.lock includes it for resolution purposes), but the vulnerable code path is not included in the default product build and is never invoked at runtime unless a user explicitly opts in via the `tls-rustls` feature flag.

## Outcomes by Choice

### Option 1: Skip remediation (VEX justification)

- Set VEX Justification custom field (`customfield_12345`) to: **Vulnerable Code not in Execute Path**
- Close the Vulnerability issue TC-8051 with resolution "Not a Bug"
- Add comment documenting the feature-gate analysis and VEX rationale
- No remediation tasks created for the 2.2.x stream

### Option 2: Proceed with remediation

- Create standard remediation tasks for the 2.2.x stream despite the feature gate
- No label or priority modifications (unlike dev-dependency handling)
- Two tasks: dependency bump (rustls to >= 0.23.5) + downstream propagation
