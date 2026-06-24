# External API Claim Verification

## Claim Detected

**Section:** Requirements (Section 4)

**Claim:** "PR reviews cannot be updated after initial submission so always create a new review" / "The GitHub API does not support modifying a submitted review"

**Category:** API limitation claim — asserts that an external API lacks a specific capability.

## Verification Attempt

**Tools used:** WebSearch, WebFetch

**Result:** UNAVAILABLE — web tools are not available in the current environment.

## Fallback Applied

Per the define-feature skill's External API Claim Verification fallback procedure:

> I detected a claim about an external API but cannot verify it right now
> (web tools unavailable). The claim is: **"The GitHub API does not support
> modifying a submitted review — PR reviews cannot be updated after initial
> submission."** Would you like to proceed as-is, or verify it manually
> before continuing?

**Status:** UNVERIFIED — This claim has not been confirmed or refuted. It is included in the Feature description as provided by the user, but should be independently verified against the official GitHub REST API documentation before implementation begins.

**Recommendation:** Before implementing, check the GitHub REST API documentation for endpoints related to updating pull request reviews (e.g., `PUT /repos/{owner}/{repo}/pulls/{pull_number}/reviews/{review_id}`). The claim may be incorrect — the GitHub API may support updating submitted reviews.
