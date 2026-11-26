# Task 4 — Description digest comment

Target issue: TC-9012 (simulated key; Task 4)

Posted as a standalone ADF comment right after the issue is created, before any issue links or other comments. No footnote, per the description-digest protocol.

> Note: in a live run the digest is computed from the description as re-fetched from Jira (`jira.get_issue`). This eval has no Jira access, so it was computed with `scripts/sha256-digest.py` over the submitted description body (from `## Repository` onward).

```json
{
  "type": "doc",
  "version": 1,
  "content": [
    {
      "type": "paragraph",
      "content": [
        { "type": "text", "text": "[sdlc-workflow] Description digest: sha256-md:b23358f2763ad8c06b95b5f696662622ce0ae331fb03fe2af551c41c33882fa9" }
      ]
    }
  ]
}
```

Rendered text:

[sdlc-workflow] Description digest: sha256-md:b23358f2763ad8c06b95b5f696662622ce0ae331fb03fe2af551c41c33882fa9
