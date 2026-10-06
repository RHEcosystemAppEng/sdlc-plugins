# Feature-Gated Dependency -- VEX Justification Prompt

## Context

- **CVE**: CVE-2026-99002
- **Library**: rustls
- **Vulnerable version**: 0.23.4 (shipped in all 2.2.x versions)
- **Fixed version**: 0.23.5
- **Feature flag**: `tls-rustls`
- **Default features**: `["tls-native"]` (does NOT include `tls-rustls`)

## Prompt

The vulnerable dependency `rustls` is gated behind the `tls-rustls` feature, which is not enabled by default. The product ships with the `tls-native` feature enabled by default, meaning the rustls code path is not compiled into or executed by the default production binary. Recommended VEX justification: **Vulnerable Code not in Execute Path**.

Options:
1. Skip remediation -- apply VEX justification "Vulnerable Code not in Execute Path" and close as not affected
2. Proceed with remediation -- create tasks despite the feature gate

Choose (1/2):

## Outcome per choice

### Option 1: Skip remediation

- Set VEX Justification field (`customfield_12345`) to "Vulnerable Code not in Execute Path"
- Close the Vulnerability issue TC-8051 as "Not a Bug" (not affected)
- Post triage summary comment documenting the feature-gate evidence and VEX justification

### Option 2: Proceed with remediation

- Create standard remediation tasks for the 2.2.x stream (2 tasks: upstream backport + downstream propagation)
- Upstream task: bump rustls from 0.23.4 to >= 0.23.5 on the `release/0.4.z` branch
- Downstream task: propagate the fix to the Konflux release repo (blocked by upstream task)
- No label or priority modifications (standard remediation despite feature gate)
