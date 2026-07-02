# External API Claim Verification

## Claim Detected

**Section:** Requirements (Section 4, Row 4)

**Claim:** "PR reviews cannot be updated after initial submission so always create a new review" with the note "The GitHub API does not support modifying a submitted review."

**Pattern matched:** "X cannot be updated after creation" / "The API does not support Y"

## Verification

**API:** GitHub REST API

**Search query:** GitHub REST API update pull request review

**Official documentation:** https://docs.github.com/en/rest/pulls/reviews#update-a-review-for-a-pull-request

**Finding:** The GitHub REST API **does** support updating a submitted pull request review via:

```
PUT /repos/{owner}/{repo}/pulls/{pull_number}/reviews/{review_id}
```

This endpoint accepts a `body` parameter (string, required) and updates the body of an existing review. It is documented in the official GitHub REST API reference under Pulls > Reviews.

## Verdict

**INCORRECT** -- The claim that "The GitHub API does not support modifying a submitted review" is factually wrong. The `PUT /repos/{owner}/{repo}/pulls/{pull_number}/reviews/{review_id}` endpoint allows updating a review after submission.

## Corrected Language

**Original requirement:** "PR reviews cannot be updated after initial submission so always create a new review"
**Original notes:** "The GitHub API does not support modifying a submitted review"

**Corrected requirement:** "Update the existing eval review when re-running on the same PR, or create a new review if none exists"
**Corrected notes:** "Use PUT /repos/{owner}/{repo}/pulls/{pull_number}/reviews/{review_id} to update an existing review"

The user was asked to confirm this correction before proceeding.
