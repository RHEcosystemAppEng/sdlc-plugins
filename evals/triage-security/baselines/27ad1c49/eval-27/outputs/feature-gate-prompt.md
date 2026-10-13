# Feature-Gate VEX Justification Prompt for TC-8051

## Context

- CVE: CVE-2026-99002
- Library: rustls
- Affected range: < 0.23.5
- Fixed version: 0.23.5
- Detected version: 0.23.4 (in 2.2.x stream, versions 2.2.0 through 2.2.4)
- Feature flag: `tls-rustls` (non-default, optional)
- Default features: `["tls-native"]`

## VEX Justification Prompt

The vulnerable dependency `rustls` is gated behind the `tls-rustls` feature, which is not enabled by default. Recommended VEX justification: **Vulnerable Code not in Execute Path**.

Options:
1. Skip remediation -- apply VEX justification and close as not affected
2. Proceed with remediation -- create tasks despite the feature gate

Choose (1/2):

## Justification Details

If option 1 is selected:
- VEX Justification value: **Vulnerable Code not in Execute Path**
- Rationale: The rustls crate is declared as an optional dependency (`optional = true`)
  in `backend/Cargo.toml` and is only included when the non-default feature `tls-rustls`
  is explicitly enabled. The product ships with `default = ["tls-native"]`, meaning
  rustls code is not compiled into the production binary. The vulnerable code path
  (certificate validation in rustls) cannot be reached in the default product configuration.
- Action: Set VEX Justification custom field (`customfield_12345`) to
  "Vulnerable Code not in Execute Path" and close the issue as "Not a Bug".

If option 2 is selected:
- Create standard remediation tasks (dependency bump + downstream propagation) for
  the 2.2.x stream without label or priority modifications.
- Remediation would bump rustls from 0.23.4 to >= 0.23.5 in `backend/Cargo.toml`.
