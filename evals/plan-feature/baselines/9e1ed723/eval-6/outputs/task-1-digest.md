# Task 1 — Description digest comment

Target issue: TC-9009 (simulated key; Task 1)

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
        { "type": "text", "text": "[sdlc-workflow] Description digest: sha256-md:4b179f6f6d1208a70db86158ae471ff9a3e8f2cd2b204f978a08bae586a7d915" }
      ]
    }
  ]
}
```

Rendered text:

[sdlc-workflow] Description digest: sha256-md:4b179f6f6d1208a70db86158ae471ff9a3e8f2cd2b204f978a08bae586a7d915
