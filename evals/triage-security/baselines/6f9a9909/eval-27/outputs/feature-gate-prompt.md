# Feature-Gated Dependency -- VEX Justification Prompt

## Context

The vulnerable dependency `rustls` (CVE-2026-99002) is gated behind a non-default feature flag in the backend component. The dependency scope analysis from Step 2.3.5 shows:

- **Library**: rustls
- **Dependency type**: direct, optional (`optional = true`)
- **Feature gate**: `tls-rustls` (non-default)
- **Default features**: `["tls-native"]` -- does NOT include `tls-rustls`
- **Product default TLS backend**: native-tls (not rustls)
- **Affected versions**: all 2.2.x versions (2.2.0 through 2.2.4) ship rustls 0.23.4

## VEX Justification Prompt

The vulnerable dependency `rustls` is gated behind the `tls-rustls` feature, which is not enabled by default. Recommended VEX justification: **Vulnerable Code not in Execute Path**.

Options:
1. **Skip remediation** -- apply VEX justification and close as not affected
2. **Proceed with remediation** -- create tasks despite the feature gate

Choose (1/2):

## Expected Outcomes

### If Option 1 (Skip remediation):

- VEX Justification field (`customfield_12345`) set to: **Vulnerable Code not in Execute Path**
- Resolution: Close as "Not a Bug"
- Rationale: The `rustls` dependency is optional and gated behind the `tls-rustls` feature flag, which is not included in the default feature set. The product ships with `tls-native` enabled by default. Since the feature is not enabled in the default build configuration, the vulnerable code is not in the execute path for standard deployments.

### If Option 2 (Proceed with remediation):

- Create standard remediation tasks (2 tasks for Cargo source dependency: upstream backport + downstream propagation) for the 2.2.x stream
- No label or priority modifications (standard remediation, not dev-dependency handling)
- All 2.2.x versions (2.2.0--2.2.4) are affected and ship rustls 0.23.4 (fix threshold: 0.23.5)
