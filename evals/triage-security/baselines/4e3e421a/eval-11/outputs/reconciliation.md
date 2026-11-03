# Step 4 – Duplicate, Sibling, Overlap, and Reconciliation Check: TC-8021

## 4.1 / 4.2 – Siblings

- The only known sibling for CVE-2026-55123 is **TC-8020** (stream `[rhtpa-2.2]`). The issue description and TC-8022's Related link identify it. It is a **different-stream companion tracker**, not a duplicate.
- 4.1: no same-stream (rhtpa-2.1) sibling is known, so there is no duplicate closure.
- 4.2: TC-8021 has no existing issue links, so no Related link to TC-8020 exists yet. Proposed action (needs confirmation): `create_link(inward: TC-8021, outward: TC-8020, type: "Related")`. Check Affects Versions overlap: TC-8021 claims only 2.1.x versions, and TC-8020 should carry only 2.2.x versions.

| Issue | Stream | Status | Affects Versions |
|---|---|---|---|
| TC-8020 | 2.2.x | (not provided) | (2.2.x versions expected) |
| TC-8021 (current) | 2.1.x | New | RHTPA 2.1.0, RHTPA 2.1.1 |

## 4.3 – Cross-CVE overlap

**Skipped.** The Upstream Affected Component, PS Component and Stream custom fields are not configured in Security Configuration. The issue carries values in customfield_10632/10669/10832, but the skill only uses configured fields.

## 4.4 – Preemptive task reconciliation

### 1. Search

```
jira.search_jql(
  "project = TC AND issuetype = Task AND labels = 'security-preemptive' AND labels = 'CVE-2026-55123' ORDER BY created DESC",
  fields: ["summary", "status", "labels", "issuelinks"]
)
```

Result (provided):

| Key | Summary | Status | Labels | Links |
|---|---|---|---|---|
| TC-8022 | Remediate CVE-2026-55123: bump tokio to 1.42.0 (rhtpa-2.1) | Open | ai-generated-jira, Security, CVE-2026-55123, security-preemptive | Related: TC-8020 (originating CVE Jira, [rhtpa-2.2]) |

### 2. Filter by stream

- Current issue stream suffix: `rhtpa-2.1`.
- TC-8022's summary contains `(rhtpa-2.1)`, so it **matches**.
- The CVE label matches (CVE-2026-55123).
- Status is Open, so the task is still active and can be reused.
- Its bump target (tokio 1.42.0) equals the fix threshold (1.42.0), so it covers this CVE.

### 3. Matching preemptive task found: reconciliation actions

These are proposed mutations. Interactive mode requires engineer confirmation for each. None were executed in this eval.

**a. Link TC-8021 to TC-8022 with "Depend"** (standard remediation linkage). TC-8021 has no existing links, so this is not a duplicate link.

```
jira.create_link(
  inwardIssue: "TC-8021",
  outwardIssue: "TC-8022",
  type: "Depend"
)
```

**b. Remove the `security-preemptive` label from TC-8022.** Only that label is removed. The other labels are kept.

```
current_labels = ["ai-generated-jira", "Security", "CVE-2026-55123", "security-preemptive"]
updated_labels = ["ai-generated-jira", "Security", "CVE-2026-55123"]
jira.edit_issue("TC-8022", fields={ "labels": updated_labels })
```

- The existing **Related** link TC-8022 to TC-8020 is **kept**. It records the cross-stream origin.

**c. Inform the engineer**

```
Existing preemptive remediation task TC-8022 found for this CVE and
stream. Created from cross-stream analysis of TC-8020
(linked via "Related").

Actions taken:
- Linked TC-8021 → TC-8022 with "Depend"
- Removed "security-preemptive" label from TC-8022

The preemptive task is now a standard remediation task for this CVE Jira.
Skipping new remediation task creation in Step 8.
```

**d. Record the reconciliation**

`reconciled_streams = { "2.1.x": "TC-8022" }`. Step 8 therefore skips remediation task creation for stream 2.1.x.

### Fullsend-mode equivalent (for reference only, not used here)

If the run were in mutation-authorized Fullsend mode, this step would serialize:
1. A `link` action: `link_type: "Depend"`, TC-8021 to TC-8022, marker `triage-security:tc-8021:link-depend:tc-8022`.
2. A `field-edit` action: TC-8022 labels set to `[ai-generated-jira, Security, CVE-2026-55123]`, marker `triage-security:tc-8021:remove-preemptive-label:tc-8022`.

### Notes / follow-ups for the engineer

- TC-8022 is described as a single "bump tokio to 1.42.0" task. The classification table expects 2 tasks per stream for Cargo (bump plus downstream propagation). The JQL returned only TC-8022. The engineer should check whether a companion downstream propagation task exists for 2.1.x. It may lack the `security-preemptive` label, or it may never have been created. If it is missing, it should be created as a standard (non-preemptive) task that is Blocked by TC-8022 and has a Depend link to TC-8021. The reconciliation rule does not create it automatically.
- TC-8022 remains Open and unassigned to this triage. Its description still carries the "Preemptive remediation" prefix. The procedure does not require editing the description, so the digest stays valid.
