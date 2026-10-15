# Triage Outcome: TC-8021

## Issue Summary

| Field | Value |
|-------|-------|
| Issue | TC-8021 |
| CVE | CVE-2026-55123 |
| Library | tokio |
| Affected range | versions before 1.42.0 |
| Fixed version | 1.42.0 |
| CVSS | 8.1 (High) |
| Stream scope | rhtpa-2.1 (2.1.x) |
| Ecosystem | Cargo |

## Outcome: Preemptive Task Reconciled -- No New Tasks Required

The triage of TC-8021 found that a preemptive remediation task (TC-8022) already exists for CVE-2026-55123 on stream 2.1.x. This task was created during the prior triage of TC-8020 (the same CVE scoped to stream `[rhtpa-2.2]`), when Step 8 Case A cross-stream impact analysis identified that stream 2.1.x was also affected but had no stream-specific CVE Jira.

### How Reconciliation Works

Step 4.4 of the triage-security skill checks for existing preemptive remediation tasks before creating new ones. The procedure is:

1. **Search** for tasks with labels `security-preemptive` and the current CVE ID (`CVE-2026-55123`).
2. **Filter** results to tasks whose summary matches the current issue's stream (`rhtpa-2.1`).
3. **Reconcile** by linking the new CVE Jira to the existing task and removing the preemptive label.

In this case, the JQL search returned TC-8022, whose summary "Remediate CVE-2026-55123: bump tokio to 1.42.0 (rhtpa-2.1)" matches the current issue's stream. Reconciliation proceeds.

### Proposed Jira Mutations

All mutations are presented for engineer confirmation -- none are executed automatically.

#### 1. Link TC-8021 to TC-8022 (Depend)

```
jira.create_link(
  inwardIssue: "TC-8021",
  outwardIssue: "TC-8022",
  type: "Depend"
)
```

This establishes TC-8022 as the remediation task for TC-8021 using the standard "Depend" linkage (same as would be used for a newly created remediation task).

#### 2. Remove `security-preemptive` label from TC-8022

```
jira.edit_issue("TC-8022", fields={
  "labels": ["ai-generated-jira", "Security", "CVE-2026-55123"]
})
```

With a proper CVE Jira now linked, TC-8022 is no longer preemptive. Removing the label converts it to a standard remediation task.

#### 3. Skip Step 8 remediation task creation

Because TC-8022 already provides remediation coverage for stream 2.1.x, Step 8 does not create new remediation tasks. The existing task covers the needed work: bumping tokio to >= 1.42.0 on the backend source repository's `release/0.3.z` branch.

#### 4. Post reconciliation comment on TC-8021

A comment documenting the reconciliation would be posted to TC-8021:

```
Existing preemptive remediation task TC-8022 found for CVE-2026-55123 on stream rhtpa-2.1.
Created from cross-stream analysis of TC-8020 (stream [rhtpa-2.2]), linked via "Related".

Actions taken:
- Linked TC-8021 -> TC-8022 with "Depend"
- Removed "security-preemptive" label from TC-8022

The preemptive task is now a standard remediation task for this CVE Jira.
Skipping new remediation task creation in Step 8.
```

#### 5. Add `ai-cve-triaged` label to TC-8021

```
jira.edit_issue("TC-8021", fields={
  "labels": ["CVE-2026-55123", "pscomponent:org/rhtpa-server", "ai-cve-triaged"]
})
```

#### 6. Post-triage summary comment on TC-8021

A summary comment would document the full triage result, including version impact (all 2.1.x versions affected), Affects Versions status, the reconciliation with TC-8022, and the existing link topology.

## Final Link Topology

```
TC-8020 (CVE Jira, stream rhtpa-2.2)
  |-- Related --> TC-8022 (remediation task for rhtpa-2.1) [from original Case A triage]

TC-8021 (CVE Jira, stream rhtpa-2.1) [current issue]
  |-- Depend --> TC-8022 (remediation task for rhtpa-2.1) [from Step 4.4 reconciliation]

TC-8022 (remediation task for rhtpa-2.1)
  Labels: ai-generated-jira, Security, CVE-2026-55123
  (security-preemptive label removed)
```

## Why This Is Correct

The reconciliation avoids creating duplicate remediation work. TC-8022 already contains the correct remediation instructions (bump tokio to 1.42.0 on the backend's release/0.3.z branch). Creating a second remediation task would produce conflicting work items for the same fix. Instead, the existing task is promoted from preemptive to standard status by:

- Adding the authoritative CVE-to-task linkage ("Depend" from TC-8021)
- Removing the `security-preemptive` marker that indicated it was provisional
- Retaining the original "Related" link to TC-8020, preserving the cross-stream traceability
