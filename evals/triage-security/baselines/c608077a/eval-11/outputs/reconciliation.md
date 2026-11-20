# TC-8021 — Step 4.4 Preemptive Task Reconciliation

## Context from Steps 4.1–4.3

- **4.1 Same-stream duplicates:** no other `[rhtpa-2.1]` Vulnerability issue for CVE-2026-55123 is known, so none were found.
- **4.2 Cross-stream siblings:** TC-8020 (CVE-2026-55123, stream `[rhtpa-2.2]`) is a companion tracker, **not a duplicate**. TC-8021 has no existing links, so a **Related** link TC-8021 ↔ TC-8020 is proposed. Each issue should carry only its own stream's versions: TC-8021 has RHTPA 2.1.x and TC-8020 is expected to have RHTPA 2.2.x, so no overlap is expected.
- **4.3 Cross-CVE overlap:** skipped. The Upstream Affected Component custom field is not configured in the project's Security Configuration.

## 4.4.1 – Search

```
jira.search_jql(
  "project = TC AND issuetype = Task AND labels = 'security-preemptive' AND labels = 'CVE-2026-55123' ORDER BY created DESC",
  fields: ["summary", "status", "labels", "issuelinks"]
)
```

Result (provided by the eval, not a live query):

| Key | Summary | Status | Labels | Links |
|---|---|---|---|---|
| TC-8022 | Remediate CVE-2026-55123: bump tokio to 1.42.0 (rhtpa-2.1) | Open | ai-generated-jira, Security, CVE-2026-55123, security-preemptive | Related → TC-8020 (originating CVE, `[rhtpa-2.2]`) |

## 4.4.2 – Filter by stream

| Check | Result |
|---|---|
| Current issue stream suffix | `rhtpa-2.1` |
| TC-8022 summary contains `(rhtpa-2.1)` | Yes, **match** |
| CVE label matches | Yes (CVE-2026-55123) |
| Still carries `security-preemptive` | Yes, not yet reconciled |
| Status | Open (still actionable, not Done or Closed) |
| Already linked to TC-8021? | No (TC-8021 has no links) |

**TC-8022 is the matching preemptive task for this CVE and stream.**

## 4.4.3 – Reconciliation actions (proposed; each needs engineer confirmation; not executed)

a. **Link TC-8021 → TC-8022 with "Depend"** (standard remediation linkage):
```
jira.create_link(inwardIssue: "TC-8021", outwardIssue: "TC-8022", type: "Depend")
```

b. **Remove the `security-preemptive` label from TC-8022**, keeping all other labels:
```
current_labels = ["ai-generated-jira", "Security", "CVE-2026-55123", "security-preemptive"]
updated_labels = ["ai-generated-jira", "Security", "CVE-2026-55123"]
jira.edit_issue("TC-8022", fields={"labels": updated_labels})
```

- The existing **Related** link TC-8022 ↔ TC-8020 is **kept**. It records where the task came from and is not removed.

c. **Engineer notification:**
```
Existing preemptive remediation task TC-8022 found for this CVE and
stream. Created from cross-stream analysis of TC-8020 (linked via "Related").

Actions taken:
- Linked TC-8021 → TC-8022 with "Depend"
- Removed "security-preemptive" label from TC-8022

The preemptive task is now a standard remediation task for this CVE Jira.
Skipping new remediation task creation in Step 8.
```

d. **Record the reconciliation:** `remediation_exists[2.1.x] = TC-8022`. Step 8 will skip task creation for 2.1.x.

## Notes / caveats

- **Downstream propagation task:** for Cargo, the preemptive variant also creates a downstream propagation subtask with the `security-preemptive` label and a Related link to TC-8020. The JQL returned **only TC-8022**. Either no preemptive downstream task exists, or it was not returned. The engineer should confirm. If one exists, it gets the same treatment (Depend link from TC-8021, label removed). If none exists, the downstream propagation task for 2.1.x is a gap to raise in Step 8. Without confirmation, the skill does not create a duplicate automatically.
- **Fullsend equivalent** (if mutation-authorized): a `link` action (`link_type: Depend`, TC-8021 → TC-8022, marker `triage-security:tc-8021:link-depend:tc-8022`) and a `field-edit` action removing `security-preemptive` from TC-8022 (marker `triage-security:tc-8021:remove-preemptive-label:tc-8022`). There are no direct Jira writes.
