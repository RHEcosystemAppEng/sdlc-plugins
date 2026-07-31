# Feature-Gated Dependency -- VEX Justification Prompt

## Dependency Scope Decision Tree Result

The dependency scope analysis (Step 2.3.5) identified `rustls` as a
**feature-gated optional dependency**. Per the dependency scope decision
tree, the following VEX justification prompt is presented to the user
before proceeding with remediation.

---

## VEX Justification Prompt

The vulnerable dependency `rustls` is gated behind the `tls-rustls`
feature, which is not enabled by default. Recommended VEX justification:
**Vulnerable Code not in Execute Path**.

Options:
1. Skip remediation -- apply VEX justification and close as not affected
2. Proceed with remediation -- create tasks despite the feature gate

Choose (1/2):

---

## Context for Decision

- **Library**: rustls
- **Feature flag**: tls-rustls
- **Default features**: ["tls-native"] (does NOT include tls-rustls)
- **Vulnerable version in lock file**: 0.23.4
- **Fixed version**: 0.23.5
- **Affected versions**: 2.2.0, 2.2.1, 2.2.2, 2.2.3, 2.2.4

The `rustls` crate is declared as `optional = true` in `backend/Cargo.toml`
and is gated behind the non-default `tls-rustls` feature flag. The product
ships with `tls-native` enabled by default, meaning rustls code is never
compiled into or executed by the default product build.

## Outcome if User Chooses Option 1 (Skip Remediation)

If the user chooses to skip remediation:

- The version is closed as **not affected** with VEX justification
  **"Vulnerable Code not in Execute Path"**
- The VEX Justification custom field (`customfield_12345`) is set to
  "Vulnerable Code not in Execute Path"
- No remediation tasks are created for any version in the 2.2.x stream
- The issue is transitioned to Closed with resolution "Not a Bug"
- A comment is posted documenting the VEX justification and the
  feature-gate evidence

Since ALL versions in the scoped stream (2.2.x) have rustls behind the
same non-default feature gate, skipping remediation applies to the entire
stream -- no versions require individual remediation.

## Outcome if User Chooses Option 2 (Proceed with Remediation)

If the user chooses to proceed with remediation:

- Standard remediation tasks are created per Case B (2 tasks per stream
  for Cargo ecosystem: upstream backport + downstream propagation)
- No label or priority modifications are applied (unlike dev-dependency
  handling)
- Tasks are created as normal despite the feature gate
