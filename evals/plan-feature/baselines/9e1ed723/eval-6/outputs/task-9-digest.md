# Task 9 — Description digest comment

Target issue: TC-9017 (simulated key; Task 9)

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
        { "type": "text", "text": "[sdlc-workflow] Description digest: sha256-md:d9f646beaf1f7d84fd3eb7d35e3bb10c0732c6e45bb7170f45a56fb65786fa09" }
      ]
    }
  ]
}
```

Rendered text:

[sdlc-workflow] Description digest: sha256-md:d9f646beaf1f7d84fd3eb7d35e3bb10c0732c6e45bb7170f45a56fb65786fa09
