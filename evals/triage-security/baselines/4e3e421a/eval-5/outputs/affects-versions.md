# Step 3 – Affects Versions Correction: TC-8005

## 3.1 Version discovery

Would call `getJiraIssueTypeMetaWithFields(projectIdOrKey: "TC", issueTypeId: "10024")`, filter `versions.allowedValues` by prefix `RHTPA`, and use the IDs it returns. No Jira call was made in this eval, so no version IDs are shown and none are hardcoded.

## 3.2 Comparison (scoped to stream 2.2.x per `[rhtpa-2.2]` suffix)

| | Value |
|---|---|
| Current (PSIRT) | `[RHTPA 2.0.0]` |
| Proposed | `[RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]` |

**Diff:** `Current: [RHTPA 2.0.0] → Proposed: [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]`

Rationale:
- **RHTPA 2.0.0 is wrong.** No 2.0.x stream exists in the Version Streams config or supportability matrix. PSIRT assigned it from scan metadata, not lock file evidence. Remove it.
- **Add 2.2.0, 2.2.1, 2.2.2.** Their rpms.lock.yaml ships openssl-libs 3.0.7-25.el9_3 / 3.0.7-27.el9_4, both < 3.0.7-28.el9_4. 2.2.2 is a retag of 2.2.1.
- **Exclude 2.2.3 and 2.2.4.** They ship 3.0.7-28.el9_4, the fixed version.
- **Exclude 2.1.0 and 2.1.1.** They are affected (3.0.7-24.el9) but belong to stream 2.1.x, outside this issue's scope. They are handled by Case A (cross-stream comment, plus a preemptive task if no sibling CVE Jira exists for 2.1.x).
- No development-stream (unreleased) version is added because none was identified for 2.2.x.
- If any of RHTPA 2.2.0, 2.2.1 or 2.2.2 has no matching Jira version, flag it to the project admin and continue.

## Proposed Jira mutation (requires engineer confirmation)

```
jira.edit_issue("TC-8005", fields={
  "versions": [{"id": "<id of RHTPA 2.2.0>"}, {"id": "<id of RHTPA 2.2.1>"}, {"id": "<id of RHTPA 2.2.2>"}]
})
```

## Proposed comment

```
Corrected Affects Versions: [RHTPA 2.0.0] → [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2].
Based on lock file analysis (rpms.lock.yaml) at pinned commits from security-matrix.md:
openssl-libs 3.0.7-25.el9_3 (2.2.0), 3.0.7-27.el9_4 (2.2.1, 2.2.2 retag) are < 3.0.7-28.el9_4;
2.2.3 and 2.2.4 ship 3.0.7-28.el9_4 (fixed).
Scoped to stream 2.2.x per issue suffix [rhtpa-2.2].

---
_Comment Footnote per shared/comment-footnote.md (skill: triage-security)_
```

(ProdSec Jira account ID not configured, so no @mention.)
