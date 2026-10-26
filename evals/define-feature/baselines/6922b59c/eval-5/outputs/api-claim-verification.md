# External API Claim Verification

## Detected Claim

**Section:** Requirements (Section 4)

**Claim:** "PR reviews cannot be updated after initial submission" / "The GitHub API does not support modifying a submitted review"

**Source Requirement Row:** "PR reviews cannot be updated after initial submission so always create a new review" with note "The GitHub API does not support modifying a submitted review"

## Verification Finding

**Result: INCORRECT**

The GitHub REST API **does** support updating a submitted pull request review. The endpoint is:

```
PUT /repos/{owner}/{repo}/pulls/{pull_number}/reviews/{review_id}
```

This endpoint accepts a `body` parameter to update the review's top-level comment text after submission. It is documented in the official GitHub REST API reference under Pull Request Reviews.

**Documentation Reference:** https://docs.github.com/en/rest/pulls/reviews#update-a-review-for-a-pull-request

## Suggested Corrected Language

**Original Requirement:** "PR reviews cannot be updated after initial submission so always create a new review"

**Original Notes:** "The GitHub API does not support modifying a submitted review"

**Corrected Requirement:** "Update the existing review when re-running evals on the same PR, or create a new review if none exists"

**Corrected Notes:** "Use PUT /repos/{owner}/{repo}/pulls/{pull_number}/reviews/{review_id} to update an existing review, or POST to create a new one"

The corrected language reflects the actual API capability: reviews can be updated after submission using the PUT endpoint. The feature design should prefer updating an existing review over creating duplicate reviews, which keeps the PR timeline cleaner for reviewers.
