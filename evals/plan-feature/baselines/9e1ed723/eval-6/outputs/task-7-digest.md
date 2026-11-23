# Task 7 — Description digest comment

Target issue: TC-9015 (simulated key; Task 7)

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
        { "type": "text", "text": "[sdlc-workflow] Description digest: sha256-md:b05e49c02ce1633adb5a70aea98573b381d2d896b0f920e9b1b2a1d523383fc8" }
      ]
    }
  ]
}
```

Rendered text:

[sdlc-workflow] Description digest: sha256-md:b05e49c02ce1633adb5a70aea98573b381d2d896b0f920e9b1b2a1d523383fc8
