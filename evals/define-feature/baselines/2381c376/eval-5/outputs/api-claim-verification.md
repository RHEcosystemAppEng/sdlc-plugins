# External API Claim Verification

## Detected Claim

**Section:** Requirements (Section 4)

**Claim text:** "PR reviews cannot be updated after initial submission so always create a new review" with the note "The GitHub API does not support modifying a submitted review."

This asserts that the GitHub REST API lacks the ability to update a pull request review after it has been submitted.

## Verification Result: INCORRECT

The claim is **incorrect**. The GitHub REST API does support updating a submitted pull request review.

**Endpoint:** `PUT /repos/{owner}/{repo}/pulls/{pull_number}/reviews/{review_id}`

**Documentation:** https://docs.github.com/en/rest/pulls/reviews#update-a-review-for-a-pull-request

This endpoint accepts a `body` parameter and updates the body text of an existing review. It operates on reviews that have already been submitted, allowing their content to be modified after initial submission.

## Suggested Corrected Language

**Original Requirement:** "PR reviews cannot be updated after initial submission so always create a new review"
**Original Notes:** "The GitHub API does not support modifying a submitted review"

**Corrected Requirement:** "Update the existing PR review when re-running evals on the same PR, or create a new review if none exists"
**Corrected Notes:** "Use PUT /repos/{owner}/{repo}/pulls/{pull_number}/reviews/{review_id} to update an existing review, or POST to create a new one"
