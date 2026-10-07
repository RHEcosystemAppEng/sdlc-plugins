# Feature-Gated Dependency -- VEX Justification Prompt

## Context

The vulnerable dependency `rustls` (CVE-2026-99002, affected versions < 0.23.5) is gated behind the `tls-rustls` feature flag, which is **not** enabled by default. The product ships with the `tls-native` feature enabled by default. Although rustls 0.23.4 appears in the Cargo.lock for all 2.2.x versions, it is an optional dependency that is not compiled into the production binary under the default feature configuration.

## VEX Justification Prompt

The vulnerable dependency `rustls` is gated behind the `tls-rustls` feature, which is not enabled by default. Recommended VEX justification: **Vulnerable Code not in Execute Path**.

Options:
1. Skip remediation -- apply VEX justification and close as not affected
2. Proceed with remediation -- create tasks despite the feature gate

Choose (1/2):

## Recommended VEX Justification

- **Value**: Vulnerable Code not in Execute Path
- **Rationale**: The rustls crate is declared as `optional = true` in backend/Cargo.toml and is gated behind the non-default `tls-rustls` feature flag. The default feature set is `["tls-native"]`, so rustls is not compiled into the production binary. The vulnerable code path (certificate validation in rustls < 0.23.5) is never executed in the default product configuration.
- **Custom field**: customfield_12345

## If user selects option 1 (Skip remediation)

- Set VEX Justification custom field (customfield_12345) to "Vulnerable Code not in Execute Path"
- Close the issue as "Not a Bug" (not affected) for all 2.2.x versions
- Post comment documenting the feature gate evidence and VEX justification

## If user selects option 2 (Proceed with remediation)

- Create standard remediation tasks (2 tasks per stream: dependency bump + downstream propagation) for the 2.2.x stream without any label or priority modifications
- Remediation would bump rustls to >= 0.23.5 even though the feature is not enabled by default
