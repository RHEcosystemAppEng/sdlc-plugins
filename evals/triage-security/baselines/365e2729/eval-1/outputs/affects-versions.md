# TC-8001 — Affects Versions Correction (Step 3)

> **Eval simulation.** No Jira call was made. The correction is **proposed** and
> needs engineer confirmation. It has **not** been applied.

## 3.1 — Jira version discovery (would run)

```
jira.getJiraIssueTypeMetaWithFields(projectIdOrKey: "TC", issueTypeId: "10024")
```

The step would filter `versions.allowedValues` by the prefix `RHTPA` and resolve version IDs at runtime. No IDs are hardcoded. This eval has no Jira response, so the IDs below are placeholders to be filled in from that call.

## 3.2 — Comparison (scoped to stream 2.2.x via the `[rhtpa-2.2]` suffix)

| | Affects Versions |
|---|---|
| **Current (PSIRT)** | `RHTPA 2.0.0` |
| **Proposed** | `RHTPA 2.2.0`, `RHTPA 2.2.1`, `RHTPA 2.2.2` |

**Diff:** `Current: [RHTPA 2.0.0] → Proposed: [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]`

Rationale:
- **RHTPA 2.0.0 is wrong.** No 2.0.x stream exists in the Version Streams table or the supportability matrix. PSIRT probably assigned it from scan time rather than dependency analysis. Remove it.
- **RHTPA 2.2.0, 2.2.1, 2.2.2** ship quinn-proto 0.11.9, 0.11.12, and 0.11.12 (2.2.2 is a retag of 2.2.1). All of these are below 0.11.14. Add them.
- **RHTPA 2.2.3 and 2.2.4 are excluded** because they ship 0.11.14, the fixed version.
- **RHTPA 2.1.0 and 2.1.1 are excluded** even though they are affected. They belong to stream 2.1.x, which is outside this issue's scope. They are reported as cross-stream impact (Step 8, Case A) and belong on a 2.1.x companion issue (Step 4).
- **Development version:** not identified (Step 2.2), so none is added.
- If any proposed version has no matching Jira version in the 3.1 results, flag it: "RHTPA X.Y.Z is in the supportability matrix but has no matching Jira version — notify project admin". Then continue.

## Proposed mutation (after engineer confirmation; NOT performed)

```
jira.edit_issue("TC-8001", fields={
  "versions": [{"id": "<id of RHTPA 2.2.0>"}, {"id": "<id of RHTPA 2.2.1>"}, {"id": "<id of RHTPA 2.2.2>"}]
})
```

## Proposed comment (after confirmation; NOT posted)

```
Corrected Affects Versions: [RHTPA 2.0.0] → [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2].
Based on lock file analysis at pinned commits from security-matrix.md
(quinn-proto 0.11.9 @ v0.4.5, 0.11.12 @ v0.4.8; 2.2.2 is a retag of 2.2.1;
2.2.3+ ship fixed 0.11.14).
Scoped to stream 2.2.x per issue suffix [rhtpa-2.2].

<Comment Footnote per shared/comment-footnote.md, skill name: triage-security>
```

No ProdSec Jira account ID is configured, so the comment carries no @mention.
