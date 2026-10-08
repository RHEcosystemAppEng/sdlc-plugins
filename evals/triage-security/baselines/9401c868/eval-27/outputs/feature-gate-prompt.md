# Feature-Gated Dependency -- VEX Justification Prompt

The vulnerable dependency `rustls` is gated behind the `tls-rustls`
feature, which is not enabled by default. Recommended VEX justification:
**Vulnerable Code not in Execute Path**.

The default feature set is `["tls-native"]`, which uses `native-tls`
instead. The `tls-rustls` feature must be explicitly enabled by a
consumer to include `rustls` in the build. The product ships with
`tls-native` enabled by default -- `rustls` code is not compiled into
the default binary.

Options:
1. Skip remediation -- apply VEX justification and close as not affected
2. Proceed with remediation -- create tasks despite the feature gate

Choose (1/2):

---

If option 1 is chosen:
- VEX Justification: **Vulnerable Code not in Execute Path**
- VEX custom field: customfield_12345
- Resolution: Close as "Not a Bug" with VEX justification applied
- Rationale: rustls is an optional dependency gated behind the
  non-default `tls-rustls` feature flag. The default build ships with
  `tls-native` and does not include rustls. The vulnerable code is not
  present in the execute path of the default product configuration.

If option 2 is chosen:
- Create standard remediation tasks (dependency bump + downstream
  propagation) for the 2.2.x stream without label or priority
  modifications.
