# Feature-Gated Dependency -- VEX Justification Prompt

## CVE-2026-99002: rustls (certificate validation bypass)

The vulnerable dependency `rustls` is gated behind the `tls-rustls` feature, which is not enabled by default. Recommended VEX justification: **Vulnerable Code not in Execute Path**.

The product ships with `default = ["tls-native"]`, which uses `native-tls` as the TLS backend. The `rustls` crate is only compiled and linked when a user explicitly enables the `tls-rustls` feature at build time. Under the default feature configuration, the rustls code is not present in the compiled binary.

Options:
1. **Skip remediation** -- apply VEX justification and close as not affected
2. **Proceed with remediation** -- create tasks despite the feature gate

Choose (1/2):

---

### Option 1 detail

If the user chooses option 1:
- VEX justification: **Vulnerable Code not in Execute Path**
- VEX justification custom field: `customfield_12345`
- Resolution: Close as "Not a Bug" with VEX justification applied
- Rationale: The vulnerable dependency `rustls` (0.23.4, below fix threshold 0.23.5) is an optional dependency gated behind the non-default `tls-rustls` feature flag. The default product configuration ships with `tls-native` enabled. The rustls code path is not compiled into or executed by the default product binary, so the vulnerability is not exploitable under the shipped configuration.

### Option 2 detail

If the user chooses option 2:
- Create standard remediation tasks (2 tasks for Cargo source dependency: upstream backport + downstream propagation) for the 2.2.x stream
- No label or priority modifications (standard remediation, not dev-dependency)
- Remediation target: bump `rustls` to >= 0.23.5 in `backend/Cargo.toml`
