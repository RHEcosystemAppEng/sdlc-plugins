# Feature-Gated Dependency -- VEX Justification Prompt

The vulnerable dependency `rustls` is gated behind the `tls-rustls` feature, which is not enabled by default. The product ships with the `tls-native` feature enabled by default. The `tls-rustls` feature must be explicitly opted into by the user at build time.

**Manifest evidence:**

```toml
# backend/Cargo.toml (v0.4.5+)
[dependencies]
rustls = { version = "0.23.4", optional = true }

[features]
default = ["tls-native"]
tls-native = ["dep:native-tls"]
tls-rustls = ["dep:rustls"]
```

Recommended VEX justification: **Vulnerable Code not Present**.

The vulnerable library (rustls) is declared as an optional dependency and is only included in the compiled binary when the non-default `tls-rustls` feature flag is explicitly enabled. Under the default feature set (`tls-native`), rustls is neither compiled nor linked into the shipped product. Because the dependency is not present in the default build, it cannot be exploited.

If the VEX Justification custom field is configured (customfield_12345), it should be set to: **Vulnerable Code not Present**.

Options:
1. **Skip remediation** -- apply VEX justification and close as not affected
2. **Proceed with remediation** -- create tasks despite the feature gate

Choose (1/2):
