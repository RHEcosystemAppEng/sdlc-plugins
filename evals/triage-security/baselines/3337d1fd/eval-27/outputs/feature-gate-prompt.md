# Feature-Gated Dependency -- VEX Justification Prompt

## Context

The vulnerable dependency `rustls` (CVE-2026-99002) is gated behind the `tls-rustls` feature, which is not enabled by default. The default feature set is `["tls-native"]`, meaning the product ships with `native-tls` as the TLS backend. The `rustls` code is not compiled into or executed by the default product build.

## Prompt Presented to User

> The vulnerable dependency `rustls` is gated behind the `tls-rustls`
> feature, which is not enabled by default. Recommended VEX justification:
> **Vulnerable Code not in Execute Path**.
>
> Options:
> 1. Skip remediation -- apply VEX justification and close as not affected
> 2. Proceed with remediation -- create tasks despite the feature gate
>
> Choose (1/2):

## VEX Justification Details

- **VEX Justification value**: Vulnerable Code not in Execute Path
- **VEX Justification custom field**: customfield_12345
- **Rationale**: The `rustls` crate is an optional dependency declared with `optional = true` in `backend/Cargo.toml`. It is gated behind the non-default feature flag `tls-rustls`. The product's default feature configuration is `default = ["tls-native"]`, which uses the `native-tls` crate instead. Since the `tls-rustls` feature is not enabled in default builds, the rustls code is not compiled into the production binary and the vulnerable code path (certificate validation bypass) is not in the execute path.

## Outcome Handling

- **If the user chooses option 1 (Skip remediation):** Close the Vulnerability issue TC-8051 as "Not a Bug" with resolution "Not a Bug". Set the VEX Justification custom field (`customfield_12345`) to "Vulnerable Code not in Execute Path". Add a comment documenting the rationale: all 2.2.x versions ship rustls 0.23.4 (within the affected range), but the dependency is behind the non-default `tls-rustls` feature flag and is not included in production builds.

- **If the user chooses option 2 (Proceed with remediation):** Create standard remediation tasks (upstream backport + downstream propagation) for the 2.2.x stream without any label or priority modifications. The tasks would bump rustls to >= 0.23.5 on the `release/0.4.z` branch.
