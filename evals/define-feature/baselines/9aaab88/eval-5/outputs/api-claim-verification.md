# External API Claim Verification

## Detected Claims

### Claim 1

**Source**: Requirements table, row 4

**Claimed text**: "PR reviews cannot be updated after initial submission"

**Additional context**: "The GitHub API does not support modifying a submitted review"

### Verification Result: INCORRECT

The GitHub REST API **does** support updating a submitted pull request review. The endpoint is:

```
PUT /repos/{owner}/{repo}/pulls/{pull_number}/reviews/{review_id}
```

This endpoint allows modifying the body of a previously submitted review. It is documented in the GitHub REST API reference under Pull Request Reviews.

**Evidence**: The `PUT /repos/{owner}/{repo}/pulls/{pull_number}/reviews/{review_id}` endpoint accepts a `body` parameter and updates the top-level review comment of an existing, already-submitted review. This means the requirement's premise -- that reviews are immutable after submission -- is factually wrong.

### Impact on Requirements

The fourth requirement ("PR reviews cannot be updated after initial submission so always create a new review") is based on an incorrect premise. Creating a new review every time is unnecessary and would clutter the PR timeline with duplicate reviews. Instead, the implementation should:

1. Check whether a review from the CI bot already exists on the PR.
2. If yes, update the existing review using `PUT /repos/{owner}/{repo}/pulls/{pull_number}/reviews/{review_id}`.
3. If no, create a new review using `POST /repos/{owner}/{repo}/pulls/{pull_number}/reviews`.

### Suggested Corrected Language

**Original**: "PR reviews cannot be updated after initial submission so always create a new review | The GitHub API does not support modifying a submitted review"

**Corrected**: "Update an existing bot review if one already exists; otherwise create a new review | Use PUT /repos/{owner}/{repo}/pulls/{pull_number}/reviews/{review_id} to update an existing review, or POST to create a new one"
