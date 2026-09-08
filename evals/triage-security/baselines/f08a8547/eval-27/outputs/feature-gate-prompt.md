# Feature-Gated Dependency -- VEX Justification Prompt

## Context

CVE-2026-99002 affects `rustls` versions before 0.23.5 (certificate validation
bypass). All 2.2.x versions ship rustls 0.23.4, which is within the affected
range. However, the dependency chain analysis (Step 2.3.5) reveals that rustls
is gated behind a non-default feature flag.

**Manifest evidence:**
```toml
[dependencies]
rustls = { version = "0.23.4", optional = true }

[features]
default = ["tls-native"]
tls-native = ["dep:native-tls"]
tls-rustls = ["dep:rustls"]
```

The default features enable `tls-native` only. The `tls-rustls` feature must be
explicitly enabled by consumers to include rustls in the build. The product ships
with `tls-native` enabled by default.

## VEX Justification Prompt

The vulnerable dependency `rustls` is gated behind the `tls-rustls` feature, which is not enabled by default. Recommended VEX justification: **Vulnerable Code not in Execute Path**.

Options:
1. Skip remediation -- apply VEX justification and close as not affected
2. Proceed with remediation -- create tasks despite the feature gate

Choose (1/2):

## Outcome Details

### If option 1 (Skip remediation):
- VEX Justification: **Vulnerable Code not in Execute Path**
- VEX Justification custom field: `customfield_12345`
- Resolution: Close as "Not a Bug" with the VEX justification applied
- Rationale: The vulnerable code (rustls) is only compiled and linked when the
  non-default `tls-rustls` feature is explicitly enabled. The default build
  configuration uses `tls-native` and does not include rustls in the binary.
  Therefore, the vulnerable code is not in the execute path for default builds.

### If option 2 (Proceed with remediation):
- Create standard remediation tasks (2 tasks per stream for Cargo ecosystem):
  1. Upstream backport task: bump rustls to >= 0.23.5 on branch `release/0.4.z`
  2. Downstream propagation task: update backend reference in rhtpa-release.0.4.z
- No label or priority modifications (standard remediation despite the feature gate)
