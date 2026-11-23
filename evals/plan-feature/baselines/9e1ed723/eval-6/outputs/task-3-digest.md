# Task 3 — Description digest comment

Target issue: TC-9011 (simulated key; Task 3)

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
        { "type": "text", "text": "[sdlc-workflow] Description digest: sha256-md:fb5f8dd3247929f9fbe29682c695ed278f5dad56522043bbc3387b2465d83097" }
      ]
    }
  ]
}
```

Rendered text:

[sdlc-workflow] Description digest: sha256-md:fb5f8dd3247929f9fbe29682c695ed278f5dad56522043bbc3387b2465d83097
