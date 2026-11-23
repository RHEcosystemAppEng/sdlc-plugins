# Task 6 — Description digest comment

Target issue: TC-9014 (simulated key; Task 6)

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
        { "type": "text", "text": "[sdlc-workflow] Description digest: sha256-md:7a80c6e124230f53f473555c13c760e42bfd334a89ee089f9ccdb996c1a5a2f3" }
      ]
    }
  ]
}
```

Rendered text:

[sdlc-workflow] Description digest: sha256-md:7a80c6e124230f53f473555c13c760e42bfd334a89ee089f9ccdb996c1a5a2f3
