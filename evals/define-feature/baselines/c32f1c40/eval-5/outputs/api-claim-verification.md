# External API Claim Verification

## Detected Claim

**Section:** Requirements (Section 4), Row 4

**Claim text:** "PR reviews cannot be updated after initial submission" with the note "The GitHub API does not support modifying a submitted review."

**Claim type:** Assertion that an external API lacks a specific capability.

## Verification

**API:** GitHub REST API

**Endpoint found:** `PUT /repos/{owner}/{repo}/pulls/{pull_number}/reviews/{review_id}`

**Documentation:** The GitHub REST API documentation for Pull Reviews confirms that a submitted review can be updated using the PUT method on the review resource endpoint. The endpoint accepts a `body` parameter to update the review's top-level comment text.

**Reference:** https://docs.github.com/en/rest/pulls/reviews#update-a-review-for-a-pull-request

## Verification Result: INCORRECT

The claim is **incorrect**. The GitHub REST API **does** support modifying a submitted review via:

```
PUT /repos/{owner}/{repo}/pulls/{pull_number}/reviews/{review_id}
```

This endpoint allows updating the body of an existing review after it has been submitted.

## Suggested Corrected Language

**Original requirement:** "PR reviews cannot be updated after initial submission so always create a new review"

**Original note:** "The GitHub API does not support modifying a submitted review"

**Corrected requirement:** "Update existing eval review if one already exists for the current run, or create a new review if none exists"

**Corrected note:** "Use PUT /repos/{owner}/{repo}/pulls/{pull_number}/reviews/{review_id} to update an existing review, or POST to create a new one"
