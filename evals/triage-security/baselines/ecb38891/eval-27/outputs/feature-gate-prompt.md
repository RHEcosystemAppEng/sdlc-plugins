# Feature-Gated Dependency -- VEX Justification Prompt

## Dependency Scope Decision Tree Result

The dependency scope analysis in Step 2.3.5 identified `rustls` as a **feature-gated optional dependency**:

- **Library**: rustls
- **Feature flag**: `tls-rustls`
- **Feature flag status**: Non-default (not included in the `default` features list)
- **Default features**: `["tls-native"]`
- **Implication**: The product ships with `tls-native` enabled by default; `rustls` is only compiled when a user explicitly enables the `tls-rustls` feature

## VEX Justification Prompt

The following prompt is presented to the engineer before proceeding with remediation:

---

> The vulnerable dependency `rustls` is gated behind the `tls-rustls` feature, which is not enabled by default. Recommended VEX justification: **Vulnerable Code not in Execute Path**.
>
> Options:
> 1. **Skip remediation** -- apply VEX justification and close as not affected
> 2. **Proceed with remediation** -- create tasks despite the feature gate
>
> Choose (1/2):

---

## Option 1: Skip Remediation

If the engineer chooses option 1 (Skip remediation):

- **Proposed action**: Close the Vulnerability issue as Not a Bug (not affected) with resolution "Not a Bug"
- **VEX Justification**: Set `customfield_12345` (VEX Justification custom field) to **Vulnerable Code not in Execute Path**
- **Rationale**: The rustls library is gated behind the non-default `tls-rustls` feature flag. Default builds do not include this feature, so the vulnerable code (certificate validation bypass in rustls < 0.23.5) is not reachable in the product as shipped. The `tls-native` feature is the default TLS backend.
- **No remediation tasks are created** for any version in the 2.2.x stream
- **Comment posted on TC-8051**: "All affected versions ship rustls 0.23.4, but rustls is an optional dependency gated behind the non-default `tls-rustls` feature flag. Default builds use `tls-native` and do not include rustls. VEX Justification: Vulnerable Code not in Execute Path."

## Option 2: Proceed with Standard Remediation

If the engineer chooses option 2 (Proceed with remediation):

- Standard remediation tasks are created for the 2.2.x stream following the source dependency ecosystem flow (2 tasks: upstream backport + downstream propagation)
- No `dev-dependency` label or priority override is applied -- this is standard remediation
- The tasks will bump rustls to >= 0.23.5

## Recommendation

The recommended choice is **Option 1 (Skip remediation)** based on the VEX justification **Vulnerable Code not in Execute Path**. The `tls-rustls` feature is non-default and the product ships with `tls-native` as the default TLS backend. The vulnerable code in rustls is not part of the production execution path.

However, this is presented as a proposal to the engineer. The engineer may choose to proceed with remediation (Option 2) if:
- There are known deployments using the `tls-rustls` feature
- The organization's security policy requires patching all optional dependencies regardless of feature gate status
- Future plans include enabling `tls-rustls` by default
