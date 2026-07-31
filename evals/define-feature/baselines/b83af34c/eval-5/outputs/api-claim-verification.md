# External API Claim Verification

## Detected Claim

**Section:** Requirements (Section 4)

**Claim text:** "PR reviews cannot be updated after initial submission" / "The GitHub API does not support modifying a submitted review"

**Context:** The requirement states that because PR reviews cannot be updated, the system should always create a new review rather than updating an existing one.

## Verification Finding

**Result: INCORRECT**

The claim is factually wrong. The GitHub REST API does support updating a submitted pull request review.

## Evidence

The GitHub REST API provides the following endpoint for updating a submitted review:

```
PUT /repos/{owner}/{repo}/pulls/{pull_number}/reviews/{review_id}
```

This endpoint accepts a `body` parameter to update the review's top-level comment text. It is documented in the official GitHub REST API reference under Pull Request Reviews.

**Documentation reference:** https://docs.github.com/en/rest/pulls/reviews#update-a-review-for-a-pull-request

The endpoint allows modifying the body of a previously submitted review, which directly contradicts the claim that "The GitHub API does not support modifying a submitted review."

## Suggested Corrected Language

**Original requirement:** "PR reviews cannot be updated after initial submission so always create a new review"

**Original notes:** "The GitHub API does not support modifying a submitted review"

**Corrected requirement:** "Update the existing PR review when re-running evals, or create a new review if none exists"

**Corrected notes:** "Use PUT /repos/{owner}/{repo}/pulls/{pull_number}/reviews/{review_id} to update an existing review"

The corrected language reflects the actual API capability and leads to a better user experience -- updating an existing review avoids cluttering the PR timeline with multiple review comments on successive eval runs.
