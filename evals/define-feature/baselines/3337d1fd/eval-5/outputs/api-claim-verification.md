# External API Claim Verification

## Detected Claim

**Section:** Requirements (Section 4), Row 4

**Claim:** "PR reviews cannot be updated after initial submission" / "The GitHub API does not support modifying a submitted review"

**Category:** Assertion that an external API lacks a specific capability

## Verification

**Result:** INCORRECT

The GitHub REST API **does** support updating a submitted pull request review. The endpoint is:

```
PUT /repos/{owner}/{repo}/pulls/{pull_number}/reviews/{review_id}
```

This endpoint allows modifying the body of an already-submitted review. It is documented in the official GitHub REST API documentation under the Pull Request Reviews section.

**Evidence:** The `PUT` method on the reviews resource accepts a `body` parameter and updates the specified review in place. This directly contradicts the claim that "PR reviews cannot be updated after initial submission."

## Suggested Corrected Language

**Original requirement:** "PR reviews cannot be updated after initial submission so always create a new review"
**Original notes:** "The GitHub API does not support modifying a submitted review"

**Corrected requirement:** "Update the existing review when re-running evals on the same PR, or create a new review if none exists"
**Corrected notes:** "Use PUT /repos/{owner}/{repo}/pulls/{pull_number}/reviews/{review_id} to update an existing review"
