# Step 4.4 -- Preemptive Task Reconciliation: TC-8021

## Overview

Step 4.4 checks whether a proactive remediation task already exists for this CVE and stream, created by a prior Step 7 Case B run on a different stream's CVE Jira. This avoids creating duplicate remediation tasks when PSIRT later files a stream-specific CVE Jira for a stream that was already covered proactively.

## JQL Search

The search for preemptive tasks matching CVE-2026-55123:

```
project = TC AND issuetype = Task AND labels = 'security-preemptive' AND labels = 'CVE-2026-55123' ORDER BY created DESC
```

**Result**: 1 match found.

## Matching Preemptive Task

| Field | Value |
|-------|-------|
| **Key** | TC-8022 |
| **Summary** | Remediate CVE-2026-55123: bump tokio to 1.42.0 (rhtpa-2.1) |
| **Status** | Open |
| **Labels** | ai-generated-jira, Security, CVE-2026-55123, security-preemptive |
| **Issue Links** | Related: TC-8020 (originating CVE Jira, stream [rhtpa-2.2]) |

## Stream Filtering

- Current issue TC-8021 stream suffix: `[rhtpa-2.1]` -- stream **2.1.x**
- Preemptive task TC-8022 summary contains: `(rhtpa-2.1)` -- **matches** the current issue's stream
- **Conclusion**: TC-8022 is a valid preemptive task match for this CVE and stream

## Origin of the Preemptive Task

TC-8022 was created during the triage of TC-8020 (CVE-2026-55123 for stream [rhtpa-2.2]). During that triage:

1. Step 2 version impact analysis revealed that both the 2.2.x and 2.1.x streams were affected by the tokio vulnerability
2. Step 7 Case B identified that the 2.1.x stream had no dedicated CVE Jira at that time
3. A preemptive remediation task (TC-8022) was created for stream 2.1.x with:
   - The `security-preemptive` label to mark it as proactive
   - A "Related" link to TC-8020 (the originating CVE Jira from stream 2.2.x)
   - A description noting the preemptive nature and originating issue

Now that PSIRT has filed TC-8021 as the stream-specific CVE Jira for 2.1.x, the preemptive task must be reconciled.

## Reconciliation Actions (PROPOSED)

Per Step 4.4 procedure, the following Jira mutations are proposed:

### Action 1: Link TC-8021 to TC-8022 with "Depend"

```
PROPOSED: jira.create_link(
  inwardIssue: "TC-8021",
  outwardIssue: "TC-8022",
  type: "Depend"
)
```

**Rationale**: The standard remediation linkage is "Depend" -- the CVE Jira (TC-8021) depends on the remediation task (TC-8022) for resolution. This replaces the "Related" link that TC-8022 previously had only to the originating cross-stream CVE (TC-8020). TC-8022 now has a proper "Depend" link from its own stream's CVE Jira.

### Action 2: Remove `security-preemptive` label from TC-8022

```
PROPOSED: jira.edit_issue("TC-8022", fields={
  "labels": ["ai-generated-jira", "Security", "CVE-2026-55123"]
})
```

**Rationale**: The `security-preemptive` label is removed because TC-8022 is no longer preemptive -- it is now linked to the proper stream-specific CVE Jira (TC-8021). The task transitions from a proactive/provisional status to a standard remediation task. The remaining labels (`ai-generated-jira`, `Security`, `CVE-2026-55123`) are preserved.

### Action 3: Inform the engineer

```
Existing preemptive remediation task TC-8022 found for this CVE and stream.
Created from cross-stream analysis of TC-8020 (linked via "Related").

Actions taken:
- Linked TC-8021 -> TC-8022 with "Depend"
- Removed "security-preemptive" label from TC-8022

The preemptive task is now a standard remediation task for this CVE Jira.
Skipping new remediation task creation in Step 7.
```

### Action 4: Record reconciliation

Mark that remediation already exists for the 2.1.x stream so Step 7 skips task creation for this stream. The existing task TC-8022 covers the required work:
- It targets the same library (tokio), same fixed version (1.42.0), and same stream (rhtpa-2.1)
- No new remediation tasks need to be created

## Existing Link Preservation

The "Related" link between TC-8022 and TC-8020 (the originating CVE from stream 2.2.x) remains intact. This preserves the audit trail showing how and why the preemptive task was originally created. TC-8022 will now have two links:
- **Depend** from TC-8021 (the proper CVE Jira for stream 2.1.x) -- new
- **Related** to TC-8020 (the originating CVE Jira from stream 2.2.x) -- existing, preserved

## Impact on Subsequent Steps

- **Step 5 (Version Lifecycle Check)**: Proceeds normally -- affected versions (2.1.0, 2.1.1) must still be verified against the product lifecycle
- **Step 6 (Already Fixed Check)**: Proceeds normally -- check resolved siblings for coverage
- **Step 7 (Remediation)**: **Skips task creation for stream 2.1.x** because the reconciliation recorded that TC-8022 already provides remediation coverage. The skill proceeds directly to post-triage summary.
