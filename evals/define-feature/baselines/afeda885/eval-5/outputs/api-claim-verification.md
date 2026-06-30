# External API Claim Verification

## Detected Claim

In **Section 4 -- Requirements**, the following claim was identified:

> "PR reviews cannot be updated after initial submission so always create a new review"
> Notes: "The GitHub API does not support modifying a submitted review"

This asserts that the GitHub REST API lacks the capability to update/modify a PR review after it has been submitted.

## Verification Finding

**Status: INCORRECT**

The GitHub REST API **does** support updating a submitted pull request review. The relevant endpoint is:

```
PUT /repos/{owner}/{repo}/pulls/{pull_number}/reviews/{review_id}
```

This endpoint accepts a JSON body with a `body` field to update the review's top-level comment text. It is documented in the official GitHub REST API documentation under "Pull request reviews."

**Documentation reference:** https://docs.github.com/en/rest/pulls/reviews#update-a-review-for-a-pull-request

## Suggested Corrected Language

**Original requirement:** "PR reviews cannot be updated after initial submission so always create a new review"
**Original notes:** "The GitHub API does not support modifying a submitted review"

**Corrected requirement:** "Update existing eval review on subsequent runs instead of creating duplicate reviews"
**Corrected notes:** "Use PUT /repos/{owner}/{repo}/pulls/{pull_number}/reviews/{review_id} to update a previously submitted review"

The corrected language reflects the actual API capability and produces a better user experience by avoiding duplicate reviews on the same PR.
