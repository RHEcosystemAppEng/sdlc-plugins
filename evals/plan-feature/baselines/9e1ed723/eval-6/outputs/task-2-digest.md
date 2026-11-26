# Task 2 — Description digest comment

Target issue: TC-9010 (simulated key; Task 2)

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
        { "type": "text", "text": "[sdlc-workflow] Description digest: sha256-md:be1d3435e0226dbf841bfab1b11b408022c57828afebb6b84585322845f6f254" }
      ]
    }
  ]
}
```

Rendered text:

[sdlc-workflow] Description digest: sha256-md:be1d3435e0226dbf841bfab1b11b408022c57828afebb6b84585322845f6f254
