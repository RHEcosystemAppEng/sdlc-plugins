# External API Claim Verification

## Detected Claim

**Section:** Requirements (Section 4)

**Claim text:** "PR reviews cannot be updated after initial submission" / "The GitHub API does not support modifying a submitted review"

**Claim type:** Assertion that an external API lacks a specific capability

## Verification

**Status:** INCORRECT

**Finding:** The GitHub REST API does support updating a submitted pull request review. The endpoint is:

```
PUT /repos/{owner}/{repo}/pulls/{pull_number}/reviews/{review_id}
```

This endpoint allows modifying the body of an already-submitted review. It is documented in the official GitHub REST API documentation under the Pull Request Reviews section.

**Documentation reference:** https://docs.github.com/en/rest/pulls/reviews#update-a-review-for-a-pull-request

## Suggested Corrected Language

**Original requirement:** "PR reviews cannot be updated after initial submission so always create a new review"

**Original notes:** "The GitHub API does not support modifying a submitted review"

**Corrected requirement:** "Update the existing eval review when re-running, or create a new review if none exists"

**Corrected notes:** "Use PUT /repos/{owner}/{repo}/pulls/{pull_number}/reviews/{review_id} to update an existing review"

The corrected language reflects the actual API capability: reviews can be updated after submission using the PUT endpoint, so the implementation should update existing reviews rather than always creating new ones.
