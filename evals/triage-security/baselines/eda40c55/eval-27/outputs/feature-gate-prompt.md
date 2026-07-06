# Feature-Gated Dependency -- VEX Justification Prompt

The vulnerable dependency `rustls` is gated behind the `tls-rustls` feature, which is not enabled by default. Recommended VEX justification: **Vulnerable Code not in Execute Path**.

Options:
1. Skip remediation -- apply VEX justification and close as not affected
2. Proceed with remediation -- create tasks despite the feature gate

Choose (1/2):

---

## Decision Outcomes

### If option 1 (Skip remediation):

- Close TC-8051 as **Not a Bug** (not affected)
- Set VEX Justification custom field (`customfield_12345`) to: **Vulnerable Code not in Execute Path**
- Add comment to TC-8051:

  > No remediation required. The vulnerable dependency `rustls` (version 0.23.4,
  > affected range: < 0.23.5) is an optional dependency gated behind the
  > non-default `tls-rustls` feature flag. The product ships with the `tls-native`
  > feature enabled by default -- `rustls` is not compiled or linked in the
  > default build configuration.
  >
  > VEX justification: Vulnerable Code not in Execute Path.
  >
  > Version impact analysis (2.2.x stream):
  >
  > | Version | rustls version | Affected? | Notes |
  > |---------|---------------|-----------|-------|
  > | 2.2.0 | 0.23.4 | YES | feature-gated (optional, non-default) |
  > | 2.2.1 | 0.23.4 | YES | feature-gated (optional, non-default) |
  > | 2.2.2 | -- | YES | retag of 2.2.1 |
  > | 2.2.3 | 0.23.4 | YES | feature-gated (optional, non-default) |
  > | 2.2.4 | 0.23.4 | YES | feature-gated (optional, non-default) |

- Add label `ai-cve-triaged` to TC-8051
- No remediation tasks are created

### If option 2 (Proceed with remediation):

- Create standard remediation tasks for the 2.2.x stream
- Two tasks (source dependency ecosystem -- Cargo):
  1. Upstream backport task: bump rustls from 0.23.4 to >= 0.23.5 in backend repository on release/0.4.z branch
  2. Downstream propagation subtask: update backend source reference in rhtpa-release.0.4.z Konflux release repo
- Link both tasks to TC-8051 with "Depend" link type
- No VEX justification applied; issue remains open for remediation tracking
