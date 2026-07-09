# Feature-Gated Dependency -- VEX Justification Prompt

## Step 2.3.5 -- Dependency Scope Decision Tree (Feature-Gated Path)

The dependency chain analysis in Step 2.3.5 identified **rustls** as a feature-gated optional dependency behind the non-default **tls-rustls** feature flag. The default features are `["tls-native"]`, meaning rustls is NOT compiled or included in standard production builds.

### VEX Justification Prompt Presented to User

> The vulnerable dependency `rustls` is gated behind the `tls-rustls` feature, which is not enabled by default. Recommended VEX justification: **Vulnerable Code not in Execute Path**.
>
> Options:
> 1. Skip remediation -- apply VEX justification and close as not affected
> 2. Proceed with remediation -- create tasks despite the feature gate
>
> Choose (1/2):

### Context for the User

- **Library**: rustls
- **Feature flag**: tls-rustls
- **Default features**: `["tls-native"]` -- tls-rustls is NOT included
- **Recommended VEX justification**: Vulnerable Code not in Execute Path
- **Rationale**: Since the `tls-rustls` feature is not enabled by default, the rustls code path is never compiled into or executed in standard production builds. The vulnerable code is not in the execute path of the shipped product.

### Outcome Handling

**If the user chooses option 1 (Skip remediation):**
- Close the affected versions as not affected with VEX justification "Vulnerable Code not in Execute Path"
- Set VEX Justification custom field (customfield_12345) to "Vulnerable Code not in Execute Path"
- No remediation tasks are created for these versions
- If all versions are closed this way, the overall issue is closed as Not a Bug with VEX justification

**If the user chooses option 2 (Proceed with remediation):**
- Create standard remediation tasks (upstream backport + downstream propagation) without any label or priority modifications
- Follow the normal Case A remediation flow for Cargo ecosystem
- Tasks would use standard labels: `["ai-generated-jira", "Security", "CVE-2026-99002"]`
