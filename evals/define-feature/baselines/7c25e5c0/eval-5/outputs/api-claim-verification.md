# External API Claim Verification

## Detected Claim

**Section:** Requirements (Section 4)

**Claim:** "PR reviews cannot be updated after initial submission" / "The GitHub API does not support modifying a submitted review"

**Requirement row:** "PR reviews cannot be updated after initial submission so always create a new review"

**Notes from user:** "The GitHub API does not support modifying a submitted review"

## Verification Result

**Status: INCORRECT**

The GitHub REST API **does** support updating a submitted pull request review. The relevant endpoint is:

```
PUT /repos/{owner}/{repo}/pulls/{pull_number}/reviews/{review_id}
```

**Documentation reference:** https://docs.github.com/en/rest/pulls/reviews#update-a-review-for-a-pull-request

This endpoint accepts a `body` parameter to update the review's top-level comment body after it has been submitted. The API returns the updated review object on success (HTTP 200).

## Suggested Correction

The requirement and its notes should be revised to reflect that the GitHub API does support updating submitted reviews. Instead of always creating a new review, the implementation should update the existing review when one already exists for the current CI run.

**Original requirement:** "PR reviews cannot be updated after initial submission so always create a new review"
**Original notes:** "The GitHub API does not support modifying a submitted review"

**Corrected requirement:** "Update the existing PR review when re-running evals, or create a new review if none exists"
**Corrected notes:** "Use PUT /repos/{owner}/{repo}/pulls/{pull_number}/reviews/{review_id} to update an existing review; fall back to creating a new review if no prior review exists for this workflow"
