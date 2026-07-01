# Jira create_issue Call Parameters

```
project_key: "TC"
issue_type_id: "10142"
summary: "Add bulk SBOM delete endpoint"
description: |
  ## Feature Overview

  Add a bulk delete endpoint for SBOMs that allows users to delete multiple
  SBOMs in a single API call. Currently users must delete SBOMs one at a
  time, which is impractical when cleaning up hundreds of test or outdated
  SBOMs. The endpoint should accept a list of SBOM IDs and return a summary
  of which deletions succeeded and which failed.

  ## Requirements

  | Requirement | Notes | Is MVP? |
  |---|---|---|
  | `DELETE /api/v2/sboms/bulk` accepts a JSON array of SBOM IDs | Maximum 100 IDs per request | Yes |
  | Return a response with per-ID success/failure status | Include error reason for each failed deletion | Yes |
  | Require the same permissions as single SBOM delete | Reuse existing authorization checks | Yes |
  | Validate all IDs before starting deletions | Return 400 if any ID is malformed | Yes |

additional_fields:
  priority:
    name: "Normal"
  labels:
    - "ai-generated-jira"
```

**Note:** `fixVersions` is NOT included in `additional_fields` because no default fixVersion is configured and the fixVersion prompt is suppressed (`Prompt for fixVersion: false`).

**Note:** `assignee` is NOT set because the user chose to leave the Feature unassigned.
