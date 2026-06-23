# External API Claim Verification

## Detected Claim

Two related claims were detected in the **Requirements** section (Section 4, row 4):

1. **"PR reviews cannot be updated after initial submission"** (requirement text)
2. **"The GitHub API does not support modifying a submitted review"** (notes column)

These claims assert that the GitHub REST API lacks the capability to update or modify a pull request review after it has been submitted.

## Verification Result: INCORRECT

The claims are **factually incorrect**. The GitHub REST API does support updating a submitted pull request review.

### Evidence

The GitHub REST API provides the following endpoint for updating a review:

```
PUT /repos/{owner}/{repo}/pulls/{pull_number}/reviews/{review_id}
```

This endpoint accepts a `body` parameter and allows modification of the review body text after the review has been submitted. It is documented in the official GitHub REST API reference under Pull Request Reviews.

This means:
- PR reviews **can** be updated after initial submission.
- The GitHub API **does** support modifying a submitted review.
- The requirement to "always create a new review" is based on a false premise.

## Suggested Corrected Language

**Original requirement:**
> PR reviews cannot be updated after initial submission so always create a new review

**Original notes:**
> The GitHub API does not support modifying a submitted review

**Corrected requirement:**
> Update the existing PR review when re-running evals on the same PR, or create a new review if none exists

**Corrected notes:**
> Use `PUT /repos/{owner}/{repo}/pulls/{pull_number}/reviews/{review_id}` to update an existing review body. Create a new review with `POST` only when no prior eval review exists on the PR.
