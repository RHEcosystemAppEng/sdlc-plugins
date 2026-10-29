# Feature-Gate VEX Justification Prompt

## Context

CVE: **CVE-2026-99002**
Library: **rustls** (versions before 0.23.5)
Issue: **TC-8051**
Stream: **2.2.x**

The vulnerable dependency `rustls` is gated behind the `tls-rustls` feature,
which is not enabled by default. The default feature set is `["tls-native"]`.
The product ships with the `tls-native` feature enabled; `tls-rustls` is an
opt-in alternative TLS backend that consumers must explicitly enable.

## Prompt Presented to User

The vulnerable dependency `rustls` is gated behind the `tls-rustls` feature, which is not enabled by default. Recommended VEX justification: **Vulnerable Code not in Execute Path**.

Options:
1. Skip remediation -- apply VEX justification and close as not affected
2. Proceed with remediation -- create tasks despite the feature gate

Choose (1/2):

## Option 1 Outcome: Skip Remediation

If the user chooses option 1:

- **VEX Justification field** (`customfield_12345`): set to "Vulnerable Code not in Execute Path"
- **Resolution**: Close as "Not a Bug" (not affected)
- **Rationale**: The vulnerable library `rustls` is an optional dependency gated
  behind the non-default `tls-rustls` feature flag. The default product build
  uses the `tls-native` feature and does not compile, link, or ship rustls.
  The vulnerable code is not present in the default execution path.
- **Comment (PROPOSAL)**: "No supported versions ship rustls in their default
  build configuration. The `rustls` crate is an optional dependency gated behind
  the `tls-rustls` feature flag, which is not enabled by default. The product
  ships with `tls-native` enabled. VEX justification: Vulnerable Code not in
  Execute Path."
- **Affects Versions correction (PROPOSAL)**: All 2.2.x versions would be removed
  from Affects Versions since the vulnerable code is not in the default execution
  path, or retained with the VEX justification depending on PSIRT policy.

## Option 2 Outcome: Proceed with Remediation

If the user chooses option 2:

- Standard remediation tasks are created without label or priority modifications
- Two tasks per affected stream (source dependency ecosystem -- Cargo):
  1. Upstream dependency bump: bump rustls from 0.23.4 to >= 0.23.5 in
     backend/Cargo.toml
  2. Downstream propagation: update the source tag/commit reference in the
     Konflux release repo (`rhtpa-release.0.4.z`) to pick up the fix
- Tasks are linked to TC-8051 with "Depend" link type

## PROPOSAL Notice

All Jira mutations described above are **proposals only** and have not been
executed. They require engineer confirmation before execution.
