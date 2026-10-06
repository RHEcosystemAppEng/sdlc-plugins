# External API Claim Verification

## Detected Claim

In **Section 4 — Requirements**, the following claim about the GitHub REST API was detected:

> **"PR reviews cannot be updated after initial submission so always create a new review — The GitHub API does not support modifying a submitted review."**

This matches the pattern: _"X cannot be updated / modified after creation"_ and _"The API does not support Y"_.

## Verification Attempt

Attempted to verify the claim against official GitHub REST API documentation.

**Tools used:** WebSearch, WebFetch
**Result:** Unavailable — web tools are not accessible in the current environment.

## Fallback Result

I detected a claim about an external API but cannot verify it right now (web tools unavailable). The claim is: **"PR reviews cannot be updated after initial submission — the GitHub API does not support modifying a submitted review."** Would you like to proceed as-is, or verify it manually before continuing?

**Status:** UNVERIFIED

The requirement row referencing this claim has been flagged in the Feature description with an **UNVERIFIED CLAIM** marker so that reviewers are aware the assertion has not been validated against official documentation.

## Recommendation

Before implementation, manually verify this claim by checking the GitHub REST API documentation for PR reviews. Specifically, check whether a `PUT /repos/{owner}/{repo}/pulls/{pull_number}/reviews/{review_id}` endpoint exists, which would allow updating a submitted review.
