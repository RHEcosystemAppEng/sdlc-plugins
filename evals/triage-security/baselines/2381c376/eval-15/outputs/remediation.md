# Step 8 — Post-Triage Summary: TC-8001

## Triage Outcome

**Case B (partial)**: Affected versions exist in the 2.2.x stream (RHTPA 2.2.0, 2.2.1, 2.2.2), but the fix is already present in later releases (RHTPA 2.2.3, 2.2.4 ship quinn-proto 0.11.14). The upstream branch `release/0.4.z` already contains the fix. No new remediation tasks are needed for the 2.2.x stream -- users should upgrade to RHTPA 2.2.3 or later.

**Case A (cross-stream impact)**: The 2.1.x stream is also affected (all versions ship quinn-proto 0.11.9). The upstream branch `release/0.3.z` does NOT have the fix. Since TC-8001 is scoped to 2.2.x, the 2.1.x impact is reported as cross-stream impact. Preemptive remediation tasks are proposed for the 2.1.x stream (pending sibling CVE Jira existence check).

## Proposed Actions

1. **Add label** `ai-cve-triaged` to TC-8001
2. **Post summary comment** (below)
3. **Cross-stream impact comment** noting 2.1.x is affected
4. **Preemptive remediation tasks for 2.1.x** (if no sibling CVE Jira exists for 2.1.x):
   - Upstream backport task: "Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (rhtpa-2.1)" with labels `[ai-generated-jira, Security, CVE-2026-31812, security-preemptive]`
   - Downstream propagation task: "Propagate CVE-2026-31812 fix: update backend ref in rhtpa-release.0.3.z (rhtpa-2.1)" with labels `[ai-generated-jira, Security, CVE-2026-31812, security-preemptive]`
   - Link type: "Related" to TC-8001 (preemptive, not "Depend")

## Post-Triage Summary Comment

```
Triage summary for CVE-2026-31812 (quinn-proto < 0.11.14, DoS via panic on large stream counts):

Version Impact:

| Version | Stream | quinn-proto | Affected? | Notes |
|---------|--------|-------------|-----------|-------|
| 2.1.0   | 2.1.x  | 0.11.9      | YES       |       |
| 2.1.1   | 2.1.x  | 0.11.9      | YES       |       |
| 2.2.0   | 2.2.x  | 0.11.9      | YES       |       |
| 2.2.1   | 2.2.x  | 0.11.12     | YES       |       |
| 2.2.2   | 2.2.x  | --          | YES       | retag of 2.2.1 |
| 2.2.3   | 2.2.x  | 0.11.14     | NO        | ships fixed version |
| 2.2.4   | 2.2.x  | 0.11.14     | NO        | ships fixed version |

Affects Versions correction: [RHTPA 2.0.0] -> [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]
(scoped to stream 2.2.x per issue suffix [rhtpa-2.2])

Triage outcome (2.2.x): Fix already present in RHTPA 2.2.3+ (quinn-proto 0.11.14).
No new remediation tasks created for this stream. Users on 2.2.0/2.2.1/2.2.2
should upgrade to 2.2.3 or later.

Cross-stream impact: quinn-proto < 0.11.14 also affects the 2.1.x stream
(versions 2.1.0, 2.1.1). The upstream branch release/0.3.z does not yet
include the fix. Preemptive remediation tasks proposed for stream 2.1.x.

@psirt-analyst
```

### ADF Comment Body (with reporter @mention and Comment Footnote)

```json
{
  "version": 1,
  "type": "doc",
  "content": [
    {
      "type": "paragraph",
      "content": [
        {
          "type": "text",
          "text": "Triage summary for CVE-2026-31812 (quinn-proto < 0.11.14, DoS via panic on large stream counts):"
        }
      ]
    },
    {
      "type": "heading",
      "attrs": { "level": 3 },
      "content": [
        {
          "type": "text",
          "text": "Version Impact"
        }
      ]
    },
    {
      "type": "table",
      "content": [
        {
          "type": "tableRow",
          "content": [
            { "type": "tableHeader", "content": [{ "type": "paragraph", "content": [{ "type": "text", "text": "Version" }] }] },
            { "type": "tableHeader", "content": [{ "type": "paragraph", "content": [{ "type": "text", "text": "Stream" }] }] },
            { "type": "tableHeader", "content": [{ "type": "paragraph", "content": [{ "type": "text", "text": "quinn-proto" }] }] },
            { "type": "tableHeader", "content": [{ "type": "paragraph", "content": [{ "type": "text", "text": "Affected?" }] }] },
            { "type": "tableHeader", "content": [{ "type": "paragraph", "content": [{ "type": "text", "text": "Notes" }] }] }
          ]
        },
        {
          "type": "tableRow",
          "content": [
            { "type": "tableCell", "content": [{ "type": "paragraph", "content": [{ "type": "text", "text": "2.1.0" }] }] },
            { "type": "tableCell", "content": [{ "type": "paragraph", "content": [{ "type": "text", "text": "2.1.x" }] }] },
            { "type": "tableCell", "content": [{ "type": "paragraph", "content": [{ "type": "text", "text": "0.11.9" }] }] },
            { "type": "tableCell", "content": [{ "type": "paragraph", "content": [{ "type": "text", "text": "YES" }] }] },
            { "type": "tableCell", "content": [{ "type": "paragraph", "content": [{ "type": "text", "text": "" }] }] }
          ]
        },
        {
          "type": "tableRow",
          "content": [
            { "type": "tableCell", "content": [{ "type": "paragraph", "content": [{ "type": "text", "text": "2.1.1" }] }] },
            { "type": "tableCell", "content": [{ "type": "paragraph", "content": [{ "type": "text", "text": "2.1.x" }] }] },
            { "type": "tableCell", "content": [{ "type": "paragraph", "content": [{ "type": "text", "text": "0.11.9" }] }] },
            { "type": "tableCell", "content": [{ "type": "paragraph", "content": [{ "type": "text", "text": "YES" }] }] },
            { "type": "tableCell", "content": [{ "type": "paragraph", "content": [{ "type": "text", "text": "" }] }] }
          ]
        },
        {
          "type": "tableRow",
          "content": [
            { "type": "tableCell", "content": [{ "type": "paragraph", "content": [{ "type": "text", "text": "2.2.0" }] }] },
            { "type": "tableCell", "content": [{ "type": "paragraph", "content": [{ "type": "text", "text": "2.2.x" }] }] },
            { "type": "tableCell", "content": [{ "type": "paragraph", "content": [{ "type": "text", "text": "0.11.9" }] }] },
            { "type": "tableCell", "content": [{ "type": "paragraph", "content": [{ "type": "text", "text": "YES" }] }] },
            { "type": "tableCell", "content": [{ "type": "paragraph", "content": [{ "type": "text", "text": "" }] }] }
          ]
        },
        {
          "type": "tableRow",
          "content": [
            { "type": "tableCell", "content": [{ "type": "paragraph", "content": [{ "type": "text", "text": "2.2.1" }] }] },
            { "type": "tableCell", "content": [{ "type": "paragraph", "content": [{ "type": "text", "text": "2.2.x" }] }] },
            { "type": "tableCell", "content": [{ "type": "paragraph", "content": [{ "type": "text", "text": "0.11.12" }] }] },
            { "type": "tableCell", "content": [{ "type": "paragraph", "content": [{ "type": "text", "text": "YES" }] }] },
            { "type": "tableCell", "content": [{ "type": "paragraph", "content": [{ "type": "text", "text": "" }] }] }
          ]
        },
        {
          "type": "tableRow",
          "content": [
            { "type": "tableCell", "content": [{ "type": "paragraph", "content": [{ "type": "text", "text": "2.2.2" }] }] },
            { "type": "tableCell", "content": [{ "type": "paragraph", "content": [{ "type": "text", "text": "2.2.x" }] }] },
            { "type": "tableCell", "content": [{ "type": "paragraph", "content": [{ "type": "text", "text": "—" }] }] },
            { "type": "tableCell", "content": [{ "type": "paragraph", "content": [{ "type": "text", "text": "YES" }] }] },
            { "type": "tableCell", "content": [{ "type": "paragraph", "content": [{ "type": "text", "text": "retag of 2.2.1" }] }] }
          ]
        },
        {
          "type": "tableRow",
          "content": [
            { "type": "tableCell", "content": [{ "type": "paragraph", "content": [{ "type": "text", "text": "2.2.3" }] }] },
            { "type": "tableCell", "content": [{ "type": "paragraph", "content": [{ "type": "text", "text": "2.2.x" }] }] },
            { "type": "tableCell", "content": [{ "type": "paragraph", "content": [{ "type": "text", "text": "0.11.14" }] }] },
            { "type": "tableCell", "content": [{ "type": "paragraph", "content": [{ "type": "text", "text": "NO" }] }] },
            { "type": "tableCell", "content": [{ "type": "paragraph", "content": [{ "type": "text", "text": "ships fixed version" }] }] }
          ]
        },
        {
          "type": "tableRow",
          "content": [
            { "type": "tableCell", "content": [{ "type": "paragraph", "content": [{ "type": "text", "text": "2.2.4" }] }] },
            { "type": "tableCell", "content": [{ "type": "paragraph", "content": [{ "type": "text", "text": "2.2.x" }] }] },
            { "type": "tableCell", "content": [{ "type": "paragraph", "content": [{ "type": "text", "text": "0.11.14" }] }] },
            { "type": "tableCell", "content": [{ "type": "paragraph", "content": [{ "type": "text", "text": "NO" }] }] },
            { "type": "tableCell", "content": [{ "type": "paragraph", "content": [{ "type": "text", "text": "ships fixed version" }] }] }
          ]
        }
      ]
    },
    {
      "type": "paragraph",
      "content": [
        {
          "type": "text",
          "text": "Affects Versions correction: [RHTPA 2.0.0] → [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2] (scoped to stream 2.2.x per issue suffix [rhtpa-2.2])."
        }
      ]
    },
    {
      "type": "heading",
      "attrs": { "level": 3 },
      "content": [
        {
          "type": "text",
          "text": "Triage Outcome (2.2.x)"
        }
      ]
    },
    {
      "type": "paragraph",
      "content": [
        {
          "type": "text",
          "text": "Fix already present in RHTPA 2.2.3+ (quinn-proto 0.11.14). No new remediation tasks created for this stream. Users on RHTPA 2.2.0, 2.2.1, or 2.2.2 should upgrade to RHTPA 2.2.3 or later."
        }
      ]
    },
    {
      "type": "heading",
      "attrs": { "level": 3 },
      "content": [
        {
          "type": "text",
          "text": "Cross-Stream Impact"
        }
      ]
    },
    {
      "type": "paragraph",
      "content": [
        {
          "type": "text",
          "text": "quinn-proto < 0.11.14 also affects the 2.1.x stream (versions 2.1.0, 2.1.1). The upstream branch release/0.3.z does not yet include the fix. Preemptive remediation tasks proposed for stream 2.1.x (pending sibling CVE Jira existence check)."
        }
      ]
    },
    {
      "type": "paragraph",
      "content": [
        {
          "type": "mention",
          "attrs": {
            "id": "557058:psirt-analyst-mock-id",
            "text": "@psirt-analyst"
          }
        }
      ]
    },
    {
      "type": "rule"
    },
    {
      "type": "paragraph",
      "content": [
        {
          "type": "text",
          "text": "This comment was AI-generated by "
        },
        {
          "type": "text",
          "text": "sdlc-workflow/triage-security",
          "marks": [
            {
              "type": "link",
              "attrs": {
                "href": "https://github.com/RHEcosystemAppEng/sdlc-plugins"
              }
            }
          ]
        },
        {
          "type": "text",
          "text": " v0.13.10."
        }
      ]
    }
  ]
}
```

## Proposed Jira Mutations (not executed)

### 1. Add `ai-cve-triaged` label to TC-8001

```
jira.edit_issue("TC-8001", fields={
  "labels": ["CVE-2026-31812", "pscomponent:org/rhtpa-server", "ai-cve-triaged"]
})
```

### 2. Post summary comment to TC-8001

Post the ADF comment body shown above, including the reporter @mention for `psirt-analyst` (account ID `557058:psirt-analyst-mock-id`) and the Comment Footnote.

### 3. Cross-stream impact comment

```
Cross-stream impact: quinn-proto < 0.11.14 also affects stream(s) 2.1.x
based on lock file analysis. These streams are tracked by companion issues
(see Related links) or may require separate PSIRT triage.
```

### 4. Preemptive remediation tasks for 2.1.x (if no sibling CVE Jira exists)

**Task 1 — Upstream backport:**
```
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (rhtpa-2.1)",
  description: <upstream-backport-template with preemptive prefix>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-31812", "security-preemptive"]
)

jira.create_link(
  inwardIssue: "TC-8001",
  outwardIssue: <upstream-task-key>,
  type: "Related"
)
```

**Task 2 — Downstream propagation:**
```
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Propagate CVE-2026-31812 fix: update backend ref in rhtpa-release.0.3.z (rhtpa-2.1)",
  description: <downstream-propagation-template with preemptive prefix>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-31812", "security-preemptive"]
)

jira.create_link(
  inwardIssue: <upstream-task-key>,
  outwardIssue: <downstream-task-key>,
  type: "Blocks"
)

jira.create_link(
  inwardIssue: "TC-8001",
  outwardIssue: <downstream-task-key>,
  type: "Related"
)
```
