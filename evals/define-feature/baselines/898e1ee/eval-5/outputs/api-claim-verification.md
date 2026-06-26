# External API Claim Verification

## Detected Claim

The Requirements section (Section 4) contains the following assertion:

> **Requirement**: "PR reviews cannot be updated after initial submission so always create a new review"
> **Notes**: "The GitHub API does not support modifying a submitted review"

This claim asserts two things:
1. PR reviews cannot be updated after initial submission.
2. The GitHub REST API does not support modifying a submitted review.

## Verification Finding

**Status: INCORRECT**

The GitHub REST API **does** support updating a submitted pull request review. The endpoint is:

```
PUT /repos/{owner}/{repo}/pulls/{pull_number}/reviews/{review_id}
```

This endpoint allows the caller to update the body of a previously submitted review. It is documented in the GitHub REST API reference under Pull Request Reviews.

Therefore, the premise that "always create a new review" is based on a false constraint. The implementation should update an existing review rather than creating duplicate reviews on each CI run.

## Suggested Corrected Language

**Original requirement**: "PR reviews cannot be updated after initial submission so always create a new review"

**Corrected requirement**: "PR reviews can be updated after submission using `PUT /repos/{owner}/{repo}/pulls/{pull_number}/reviews/{review_id}`, so the implementation should update the existing review instead of creating a new one"

**Original notes**: "The GitHub API does not support modifying a submitted review"

**Corrected notes**: "The GitHub REST API supports updating a submitted review via `PUT /repos/{owner}/{repo}/pulls/{pull_number}/reviews/{review_id}`. Use this to update an existing eval review rather than posting duplicates."
