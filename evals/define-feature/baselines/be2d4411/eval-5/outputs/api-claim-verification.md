# External API Claim Verification

## Claim Detected

**Section:** Requirements (Section 4)

**Claim:** "PR reviews cannot be updated after initial submission" / "The GitHub API does not support modifying a submitted review"

**Requirement row:** "PR reviews cannot be updated after initial submission so always create a new review"
**Notes column:** "The GitHub API does not support modifying a submitted review"

## Verification

**Source:** GitHub REST API official documentation

The GitHub REST API **does** support updating a submitted pull request review via:

```
PUT /repos/{owner}/{repo}/pulls/{pull_number}/reviews/{review_id}
```

This endpoint allows modifying the body of a previously submitted review. It accepts a `body` parameter (string, required) containing the updated text for the review.

**Documentation reference:** https://docs.github.com/en/rest/pulls/reviews#update-a-review-for-a-pull-request

## Result

**INCORRECT** -- The claim is factually wrong. The GitHub REST API does support modifying a submitted review via the PUT endpoint described above.

## Suggested Correction

The requirement "PR reviews cannot be updated after initial submission so always create a new review" should be revised to reflect the actual API capability. Suggested corrected language:

**Original requirement:** "PR reviews cannot be updated after initial submission so always create a new review"
**Original notes:** "The GitHub API does not support modifying a submitted review"

**Corrected requirement:** "Update existing PR review when re-running evals on the same PR, or create a new review if none exists"
**Corrected notes:** "Use PUT /repos/{owner}/{repo}/pulls/{pull_number}/reviews/{review_id} to update an existing review, or POST to create a new one"
