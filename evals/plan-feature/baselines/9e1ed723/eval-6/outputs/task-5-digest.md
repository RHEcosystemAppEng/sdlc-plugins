# Task 5 — Description digest comment

Target issue: TC-9013 (simulated key; Task 5)

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
        { "type": "text", "text": "[sdlc-workflow] Description digest: sha256-md:948b0e4cc63e07d8ad63ccf914a483c395c505267ab66062f6d92ad477eb492c" }
      ]
    }
  ]
}
```

Rendered text:

[sdlc-workflow] Description digest: sha256-md:948b0e4cc63e07d8ad63ccf914a483c395c505267ab66062f6d92ad477eb492c
