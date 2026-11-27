# TC-8001 — Affects Versions Correction (Step 3)

> Proposed only. No `getJiraIssueTypeMetaWithFields`, `edit_issue`, or `add_comment` call was made.

## 3.1 Discover available Jira versions

In a live run this calls:

```
jira.getJiraIssueTypeMetaWithFields(projectIdOrKey: "TC", issueTypeId: "10024")
```

It then filters `versions.allowedValues` to names starting with `RHTPA`. Version IDs are
**not hardcoded** and are shown below as `<id: RHTPA x.y.z>` placeholders, because they come
from that runtime lookup.

## 3.2 Compare and correct

- Issue scope: **2.2.x** (suffix `[rhtpa-2.2]`). Only 2.2.x versions go on this issue. 2.1.0 and
  2.1.1 are also affected, but they belong to the 2.1.x stream (Case A / companion tracker) and
  are **excluded** here.
- PSIRT value **RHTPA 2.0.0 is wrong**. There is no 2.0.x stream in the supportability matrix,
  and no lock file evidence links 2.0.0 to this issue.
- RHTPA 2.2.3 and 2.2.4 ship quinn-proto 0.11.14, so they are **not affected** and not added.
- The development stream could not be determined (no Jira version metadata), so no unreleased
  version is added.

```
Current:  [RHTPA 2.0.0]
Proposed: [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]
```

| Version | Action | Evidence |
|---|---|---|
| RHTPA 2.0.0 | **Remove** | Not in any configured stream. Misattributed by PSIRT. |
| RHTPA 2.2.0 | **Add** | `v0.4.5` Cargo.lock: quinn-proto 0.11.9 |
| RHTPA 2.2.1 | **Add** | `v0.4.8` Cargo.lock: quinn-proto 0.11.12 |
| RHTPA 2.2.2 | **Add** | Backend retag of 2.2.1 (`v0.4.8`), result carried forward |

If the 3.1 lookup finds that any of RHTPA 2.2.0/2.2.1/2.2.2 has no Jira version, flag it:
"RHTPA X.Y.Z is in the supportability matrix but has no matching Jira version — notify project
admin". Then continue with the versions that do exist.

### Proposed mutation (requires engineer confirmation; NOT performed)

```
jira.edit_issue("TC-8001", fields={
  "versions": [{"id": "<id: RHTPA 2.2.0>"}, {"id": "<id: RHTPA 2.2.1>"}, {"id": "<id: RHTPA 2.2.2>"}]
})
```

### Proposed comment (requires engineer confirmation; NOT posted)

No ProdSec Jira account ID is configured, so the comment has no @mention.

```
Corrected Affects Versions: [RHTPA 2.0.0] → [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2].
Based on lock file analysis at pinned commits from security-matrix.md
(quinn-proto 0.11.9 @ v0.4.5, 0.11.12 @ v0.4.8; 2.2.2 is a backend retag of 2.2.1).
RHTPA 2.2.3 and 2.2.4 ship quinn-proto 0.11.14 (fixed) and are not affected.
Scoped to stream 2.2.x per issue suffix [rhtpa-2.2].

---
<Comment Footnote per shared/comment-footnote.md, skill name: triage-security>
```
