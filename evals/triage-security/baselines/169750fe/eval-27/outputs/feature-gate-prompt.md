# Feature-Gated Dependency -- VEX Justification Prompt

## Decision Point (Step 2.3.5 -- Dependency Scope Decision Tree)

The vulnerable dependency `rustls` is gated behind the `tls-rustls` feature, which is not enabled by default. Recommended VEX justification: **Vulnerable Code not in Execute Path**.

Options:
1. Skip remediation -- apply VEX justification and close as not affected
2. Proceed with remediation -- create tasks despite the feature gate

Choose (1/2):

---

## Context

- **Library**: rustls
- **Feature flag**: `tls-rustls`
- **Default features**: `["tls-native"]` (does NOT include `tls-rustls`)
- **CVE**: CVE-2026-99002
- **Shipped version**: 0.23.4 (affected range: < 0.23.5)
- **VEX Justification custom field**: customfield_12345

## If User Chooses Option 1 (Skip Remediation)

Close the Vulnerability issue TC-8051 as not affected:

1. Add comment explaining that rustls is an optional dependency behind the non-default `tls-rustls` feature flag and is not included in production builds under the default `tls-native` configuration.
2. Transition to Closed with resolution "Not a Bug".
3. Set VEX Justification field (customfield_12345) to: **Vulnerable Code not in Execute Path**.
4. Add label `ai-cve-triaged`.

## If User Chooses Option 2 (Proceed with Remediation)

Create standard remediation tasks (dependency bump + downstream propagation) for the 2.2.x stream without any label or priority modifications. Treat rustls as a regular affected dependency despite the feature gate.
