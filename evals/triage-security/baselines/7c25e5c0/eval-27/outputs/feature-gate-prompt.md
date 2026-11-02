# Step 2.3.5 — Feature-Gated Dependency: VEX Justification Prompt

## Dependency Scope Decision Tree — Feature-Gated Optional Dependency

The vulnerable dependency `rustls` is gated behind the `tls-rustls` feature, which is not enabled by default. The product ships with the `tls-native` feature enabled by default, meaning `rustls` is not compiled or included in production builds unless a downstream consumer explicitly opts in.

---

**VEX Justification Prompt:**

> The vulnerable dependency `rustls` is gated behind the `tls-rustls` feature, which is not enabled by default. Recommended VEX justification: **Vulnerable Code not in Execute Path**.
>
> Options:
> 1. **Skip remediation** — apply VEX justification and close as not affected
> 2. **Proceed with remediation** — create tasks despite the feature gate
>
> Choose (1/2):

---

### Option 1: Skip remediation

If the engineer chooses option 1:
- Close the affected versions as **not affected** with VEX Justification set to **Vulnerable Code not in Execute Path** (using configured field `customfield_12345`)
- The overall issue closure depends on whether other versions are also affected
- Since all 2.2.x versions share the same feature-gate status, the entire issue can be closed as Not a Bug with VEX justification if the engineer confirms

### Option 2: Proceed with standard remediation

If the engineer chooses option 2:
- Create standard Cargo remediation tasks (2 tasks: upstream backport + downstream propagation)
- No label or priority modifications (unlike dev-dependency handling)
- Remediation: bump rustls to >= 0.23.5 in Cargo.toml
- Standard labels: `["ai-generated-jira", "Security", "CVE-2026-99002"]`

---

### Context for the engineer

- **Library**: rustls
- **Feature flag**: tls-rustls
- **Default features**: ["tls-native"] — does NOT include tls-rustls
- **CVE severity**: CVSS 8.1 (High) — certificate validation bypass
- **Risk if feature is enabled by a downstream consumer**: High — TLS certificate validation bypass could allow MITM attacks
- **Risk if feature is NOT enabled (default)**: Code is not compiled; vulnerability is not exploitable
