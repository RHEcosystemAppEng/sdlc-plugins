# Feature-Gated Dependency -- VEX Justification Prompt

The vulnerable dependency `rustls` is gated behind the `tls-rustls` feature, which is not enabled by default. Recommended VEX justification: **Vulnerable Code not in Execute Path**.

Options:
1. Skip remediation -- apply VEX justification and close as not affected
2. Proceed with remediation -- create tasks despite the feature gate

Choose (1/2):

---

## Context

- **Library**: rustls
- **Feature flag**: tls-rustls
- **Default features**: tls-native (does NOT include tls-rustls)
- **Affected versions**: all 2.2.x versions ship rustls 0.23.4 (< 0.23.5)
- **VEX justification**: Vulnerable Code not in Execute Path

## Outcome if Option 1 (Skip remediation)

Close TC-8051 as "Not a Bug" with:
- Resolution: Not a Bug
- VEX Justification (customfield_12345): Vulnerable Code not in Execute Path
- Comment: "rustls 0.23.4 is present in Cargo.lock but gated behind the non-default `tls-rustls` feature flag. The product ships with `tls-native` enabled by default. The vulnerable code is not compiled into or executed by the default build. Closing with VEX justification: Vulnerable Code not in Execute Path."

No remediation tasks will be created.

## Outcome if Option 2 (Proceed with remediation)

Create standard remediation tasks for the 2.2.x stream to bump rustls from 0.23.4 to >= 0.23.5, following the normal Case A remediation flow (upstream backport task + downstream propagation subtask).
