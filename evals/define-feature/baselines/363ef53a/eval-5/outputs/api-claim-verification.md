# External API Claim Verification

## Detected Claim

**Section:** Requirements (Section 4)

**Claim:** "PR reviews cannot be updated after initial submission" / "The GitHub API does not support modifying a submitted review"

**Context:** The requirement states that because PR reviews cannot be updated, the workflow should always create a new review rather than updating an existing one.

## Verification Finding

**Result: INCORRECT**

The claim is factually wrong. The GitHub REST API does support updating a submitted pull request review.

## Evidence

The GitHub REST API provides the following endpoint for updating a submitted review:

```
PUT /repos/{owner}/{repo}/pulls/{pull_number}/reviews/{review_id}
```

This endpoint accepts a `body` parameter to update the review's top-level comment after it has been submitted. It is documented in the official GitHub REST API reference under Pull Request Reviews.

**Documentation reference:** https://docs.github.com/en/rest/pulls/reviews#update-a-review-for-a-pull-request

## Suggested Corrected Language

**Original requirement:** "PR reviews cannot be updated after initial submission so always create a new review"

**Original notes:** "The GitHub API does not support modifying a submitted review"

**Corrected requirement:** "Update the existing PR review when re-running evals on the same PR, or create a new review if none exists"

**Corrected notes:** "Use PUT /repos/{owner}/{repo}/pulls/{pull_number}/reviews/{review_id} to update an existing review"

The corrected language reflects the actual API capability and results in a better user experience -- reviewers see a single updated review rather than multiple stale reviews accumulating on the PR.
