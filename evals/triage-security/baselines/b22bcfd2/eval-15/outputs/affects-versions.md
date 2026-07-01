# Step 3 -- Affects Versions Correction

## 3.1 -- Jira Version Discovery

Proposed dynamic discovery via `getJiraIssueTypeMetaWithFields` for project TC, issue type 10024.
Versions matching prefix "RHTPA" would be discovered at runtime (Important Rule 6 -- never hardcode Jira version IDs).

Expected version registry (from supportability matrix version names):

| Name | Released | Stream |
|------|----------|--------|
| RHTPA 2.1.0 | yes | 2.1.x |
| RHTPA 2.1.1 | yes | 2.1.x |
| RHTPA 2.2.0 | yes | 2.2.x |
| RHTPA 2.2.1 | yes | 2.2.x |
| RHTPA 2.2.2 | yes | 2.2.x |
| RHTPA 2.2.3 | yes | 2.2.x |
| RHTPA 2.2.4 | yes | 2.2.x |

## 3.2 -- Compare and Correct Affects Versions

**Issue stream scope**: 2.2.x (from summary suffix `[rhtpa-2.2]`)

The correction is scoped to the 2.2.x stream only. Although 2.1.x versions are also affected (see version impact table), those belong to a sibling issue for the 2.1.x stream -- they are not included here.

**Current Affects Versions (PSIRT-assigned)**: `[RHTPA 2.0.0]`

**Version impact (2.2.x stream only)**:
- RHTPA 2.2.0: YES (affected -- quinn-proto 0.11.9)
- RHTPA 2.2.1: YES (affected -- quinn-proto 0.11.12)
- RHTPA 2.2.2: YES (affected -- retag of 2.2.1)
- RHTPA 2.2.3: NO (not affected -- quinn-proto 0.11.14)
- RHTPA 2.2.4: NO (not affected -- quinn-proto 0.11.14)

**Proposed correction**:

```
Current: [RHTPA 2.0.0] -> Proposed: [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]
```

RHTPA 2.0.0 does not match any version in the supportability matrix and is not a valid version for this stream. The PSIRT-assigned value is incorrect.

The proposed Affects Versions include only the versions from the 2.2.x stream that are confirmed affected by lock file analysis at their pinned commits. Version names are referenced from the supportability matrix (Important Rule 6).

## Proposed Affects Versions Correction Comment

After engineer confirmation, the following comment would be posted to TC-8001:

---

Corrected Affects Versions: [RHTPA 2.0.0] -> [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2].

Based on lock file analysis at pinned commits from security-matrix.md:
- RHTPA 2.2.0 (tag v0.4.5): quinn-proto 0.11.9 -- affected (< 0.11.14)
- RHTPA 2.2.1 (tag v0.4.8): quinn-proto 0.11.12 -- affected (< 0.11.14)
- RHTPA 2.2.2 (tag v0.4.9): retag of 2.2.1 -- affected (same as 2.2.1)
- RHTPA 2.2.3 (tag v0.4.11): quinn-proto 0.11.14 -- NOT affected (fixed)
- RHTPA 2.2.4 (tag v0.4.12): quinn-proto 0.11.14 -- NOT affected (fixed)

Scoped to stream 2.2.x per issue suffix [rhtpa-2.2].

[ProdSec @mention: ADF mention node]

```json
{
  "type": "mention",
  "attrs": {
    "id": "557058:prodsec-mock-account-id",
    "text": "@prodsec-team"
  }
}
```

---

_[sdlc-workflow:triage-security]_

---

**Key behaviors demonstrated**:

1. **ProdSec @mention included**: The Affects Versions correction comment includes an @mention of the ProdSec contact using an ADF mention node with account ID `557058:prodsec-mock-account-id`, extracted from the Security Configuration. This @mention appears **before** the Comment Footnote.

2. **Version names from supportability matrix**: All version references use names from the supportability matrix (RHTPA 2.2.0, RHTPA 2.2.1, etc.) rather than hardcoded Jira version IDs (Important Rule 6).

3. **Scoped to issue stream**: Only 2.2.x versions are included in the correction, despite 2.1.x versions also being affected. The 2.1.x impact is handled by companion/sibling issues.
