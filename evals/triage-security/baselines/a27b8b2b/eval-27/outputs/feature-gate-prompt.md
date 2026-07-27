# Feature-Gated Dependency -- VEX Justification Prompt

## Dependency Scope Decision Tree Result

The dependency scope analysis in Step 2.3.5 identified `rustls` as a **feature-gated
optional dependency** behind the non-default `tls-rustls` feature flag. The default
feature set (`["tls-native"]`) does not include `tls-rustls`, so the vulnerable code
is not compiled into or executed by the default production build.

## VEX Justification Prompt

The following prompt is presented to the engineer before proceeding to remediation
task creation:

---

> The vulnerable dependency `rustls` is gated behind the `tls-rustls` feature,
> which is not enabled by default. Recommended VEX justification:
> **Vulnerable Code not in Execute Path**.
>
> Options:
> 1. **Skip remediation** -- apply VEX justification and close as not affected
> 2. **Proceed with remediation** -- create tasks despite the feature gate
>
> Choose (1/2):

---

## Option 1: Skip Remediation

If the user chooses option 1 (skip remediation):

1. The issue is closed as **not affected** with the VEX justification
   **Vulnerable Code not in Execute Path**.
2. Since the VEX Justification custom field (`customfield_12345`) is configured
   in the Security Configuration, set it to "Vulnerable Code not in Execute Path":
   ```
   jira.edit_issue("TC-8051", fields={
     "customfield_12345": "Vulnerable Code not in Execute Path"
   })
   ```
3. **No remediation tasks are created** for the affected versions in this stream.
4. A close comment is posted documenting the rationale:
   ```
   Closing as Not a Bug (not affected).

   The vulnerable dependency rustls (< 0.23.5) is present in the Cargo.lock
   for all 2.2.x versions (0.23.4), but it is an optional dependency gated
   behind the non-default "tls-rustls" feature flag. The product ships with
   "tls-native" as the default feature -- rustls code is not compiled into
   or executed by the production binary.

   VEX Justification: Vulnerable Code not in Execute Path

   Version impact:
   | Version | rustls | Affected? | Notes |
   |---------|--------|-----------|-------|
   | 2.2.0   | 0.23.4 | YES (feature-gated) | tls-rustls not in default features |
   | 2.2.1   | 0.23.4 | YES (feature-gated) | tls-rustls not in default features |
   | 2.2.2   | --     | YES (feature-gated) | retag of 2.2.1 |
   | 2.2.3   | 0.23.4 | YES (feature-gated) | tls-rustls not in default features |
   | 2.2.4   | 0.23.4 | YES (feature-gated) | tls-rustls not in default features |
   ```
5. The issue is transitioned to Closed with resolution "Not a Bug".

Note: If other streams were also affected, the overall issue closure depends on
whether those streams also choose to skip remediation. Each stream's decision is
independent -- if some streams skip via VEX justification but others proceed with
remediation, the issue remains open for the streams that need remediation.

## Option 2: Proceed with Standard Remediation

If the user chooses option 2 (proceed with remediation):

- Standard remediation tasks are created without any label or priority modifications.
- The feature-gate status is noted in the remediation task description for engineer context,
  but the tasks follow the normal Cargo (source dependency) two-task pattern:
  1. **Upstream backport task**: Bump rustls to >= 0.23.5 in the backend repository
     on the release/0.4.z branch.
  2. **Downstream propagation subtask**: Update the backend source reference in the
     Konflux release repo to pick up the upstream fix. Blocked by the upstream task.
- Labels: `["ai-generated-jira", "Security", "CVE-2026-99002"]` (standard labels,
  no dev-dependency label since this is not a dev-only dependency).
- Priority: inherited from the CVE severity (no override, since this is not a
  dev-dependency scenario).
