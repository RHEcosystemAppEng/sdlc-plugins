# External API Claim Verification

## Claim Detected

**Section:** Requirements (Section 4)

**Claim:** "PR reviews cannot be updated after initial submission" / "The GitHub API does not support modifying a submitted review"

**Requirement row:** "PR reviews cannot be updated after initial submission so always create a new review" with note "The GitHub API does not support modifying a submitted review"

## Verification Result

**Status:** INCORRECT

The GitHub REST API **does** support updating a submitted pull request review. The relevant endpoint is:

```
PUT /repos/{owner}/{repo}/pulls/{pull_number}/reviews/{review_id}
```

**Documentation:** https://docs.github.com/en/rest/pulls/reviews#update-a-review-for-a-pull-request

This endpoint accepts a `body` parameter and allows modifying the review body after it has been submitted. The claim that "The GitHub API does not support modifying a submitted review" is factually incorrect.

## Suggested Correction

The original requirement:

> PR reviews cannot be updated after initial submission so always create a new review

Should be corrected to:

> Update existing PR reviews when re-running evals on the same PR, rather than creating duplicate reviews

This reflects the actual API capability and produces a better user experience (avoiding review spam on PRs with multiple eval runs).
