<!-- SYNTHETIC TEST DATA — mock GitHub PR review comments for cross-repository review feedback eval testing; simulates `gh api repos/{owner}/{repo}/pulls/{number}/reviews` and `gh api repos/{owner}/{repo}/pulls/{number}/comments` output -->

## Reviews (`gh api repos/trustify/trustify-ui/pulls/1450/reviews`)

```json
[
  {
    "id": 21001,
    "user": {
      "login": "reviewer-a",
      "id": 10001
    },
    "body": "The sort works, but it is in the wrong layer. See the inline comment.",
    "state": "CHANGES_REQUESTED",
    "submitted_at": "2026-11-12T09:15:00Z"
  }
]
```

## Review Comments (`gh api repos/trustify/trustify-ui/pulls/1450/comments`)

```json
[
  {
    "id": 60001,
    "pull_request_review_id": 21001,
    "user": {
      "login": "reviewer-a",
      "id": 10001
    },
    "body": "This ordering has to happen next to the data, not in the browser. Advisory rows come from `advisories()` in the shared query builder in `trustify/trustify`, which returns them without an `ORDER BY` — so the API, the exports and every other client still get an arbitrary order, and this `useMemo` only papers over it for this one page. Please add the `ORDER BY` (advisory date descending, then advisory ID) to that query with a backend test in `trustify/trustify`, and drop the in-memory sort here. `trustify/trustify` has no open PR for this yet.",
    "path": "src/pages/advisories/AdvisoryTable.tsx",
    "line": 18,
    "side": "RIGHT",
    "created_at": "2026-11-12T09:18:00Z",
    "updated_at": "2026-11-12T09:18:00Z",
    "in_reply_to_id": null
  }
]
```
