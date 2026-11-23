# Task 8 — Description digest comment

Target issue: TC-9016 (simulated key; Task 8)

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
        { "type": "text", "text": "[sdlc-workflow] Description digest: sha256-md:0fece94a7c2b3aa39966e6eab0de2d18db761acf413e0b4d41678f9e7f9ccade" }
      ]
    }
  ]
}
```

Rendered text:

[sdlc-workflow] Description digest: sha256-md:0fece94a7c2b3aa39966e6eab0de2d18db761acf413e0b4d41678f9e7f9ccade
