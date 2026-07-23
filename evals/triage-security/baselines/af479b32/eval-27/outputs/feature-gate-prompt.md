# Feature-Gated Dependency -- VEX Justification Prompt

The vulnerable dependency `rustls` is gated behind the `tls-rustls` feature, which is not enabled by default. The default feature set is `["tls-native"]`, meaning the product ships with native-tls as its TLS backend. The `tls-rustls` feature must be explicitly opted into at compile time.

Recommended VEX justification: **Vulnerable Code not in Execute Path**.

Options:
1. Skip remediation -- apply VEX justification and close as not affected
2. Proceed with remediation -- create tasks despite the feature gate

Choose (1/2):

---

## Context

- **Library**: rustls
- **CVE**: CVE-2026-99002
- **Affected range**: versions before 0.23.5
- **Installed version**: 0.23.4
- **Feature flag**: `tls-rustls` (non-default, optional)
- **Default features**: `["tls-native"]`
- **VEX Justification custom field**: customfield_12345

## If option 1 is chosen

- Set VEX Justification field (`customfield_12345`) to: **Vulnerable Code not in Execute Path**
- Close the Vulnerability issue TC-8051 with resolution "Not a Bug"
- Add comment documenting: "The vulnerable dependency rustls is gated behind the non-default feature flag `tls-rustls`. The default build uses `tls-native`. Under default features, rustls code is not compiled into the product binary. VEX justification: Vulnerable Code not in Execute Path."

## If option 2 is chosen

- Proceed with standard remediation task creation (Case A)
- Create upstream backport task: bump rustls to >= 0.23.5 on branch `release/0.4.z` in rhtpa-backend
- Create downstream propagation subtask: update backend source reference in rhtpa-release.0.4.z
- No label or priority modifications (feature-gated deps that proceed to remediation use standard handling)
