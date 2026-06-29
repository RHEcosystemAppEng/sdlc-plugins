# External API Claim Verification

## Detected Claim

The user input contains the following claims about the GitHub REST API:

1. **"PR reviews cannot be updated after initial submission"**
2. **"The GitHub API does not support modifying a submitted review"**

These claims appear in Section 4 (Requirements), row 4, as justification for always creating a new review rather than updating an existing one.

## Verification Result: INCORRECT

Both claims are **factually incorrect**. The GitHub REST API **does** support updating a submitted pull request review via:

```
PUT /repos/{owner}/{repo}/pulls/{pull_number}/reviews/{review_id}
```

This endpoint accepts a `body` parameter to update the review's top-level comment after submission. It is documented in the official GitHub REST API reference under "Pull request reviews."

## Impact on Requirements

The original requirement states:

> PR reviews cannot be updated after initial submission so always create a new review

This would lead to duplicate review comments accumulating on a PR each time evals are re-run (e.g., on subsequent pushes), creating noise for reviewers.

## Suggested Corrected Language

The requirement should be revised to:

> **PR reviews can be updated after submission** using `PUT /repos/{owner}/{repo}/pulls/{pull_number}/reviews/{review_id}`, so the implementation should update existing reviews rather than always creating new ones. When a prior eval review exists on the PR, update it in place; only create a new review if none exists yet.
