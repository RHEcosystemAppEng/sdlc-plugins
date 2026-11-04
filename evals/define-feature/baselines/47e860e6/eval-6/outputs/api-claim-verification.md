# External API Claim Verification — Fallback Result

## Detected Claim

- **Section:** Requirements (Step 3d), row 4
- **API:** GitHub REST API (Pull Request Reviews)
- **Claim (requirement):** "PR reviews cannot be updated after initial submission so always create a new review"
- **Claim (notes):** "The GitHub API does not support modifying a submitted review"
- **Pattern matched:** "X cannot be updated / modified after creation" and "The API does not support Y"

## User Notification

> I detected a claim about an external API capability in the Requirements section: the
> GitHub REST API does not allow a pull request review to be updated after it is submitted.
> I will attempt to verify it against the official GitHub REST API documentation.

## Verification Attempt

- **WebSearch:** unavailable in this session — not performed
- **WebFetch:** unavailable in this session — not performed
- **Result:** **UNVERIFIED** — official documentation could not be consulted.

No confirmation or refutation is asserted. Verification status is neither "confirmed" nor
"incorrect"; the skill's fallback path applies.

## Fallback Prompt Presented to User

> "I detected a claim about an external API but cannot verify it right now
> (web tools unavailable). The claim is: **PR reviews cannot be updated after initial
> submission so always create a new review — the GitHub API does not support modifying a
> submitted review**. Would you like to proceed as-is, or verify it manually before continuing?"

## Suggested Manual Check

Before relying on this requirement, check the GitHub REST API documentation for Pull
Request Reviews (docs.github.com, "REST API endpoints for pull request reviews") and confirm
whether an endpoint exists to update a review's body after submission. If such an endpoint
exists, requirement row 4 should be revised (e.g., to update the existing eval review instead
of always creating a new one), since this assumption directly shapes downstream planning and
implementation.

## Outcome for This Run

The user was not able to provide a manual verification result in this eval session. The
original wording is retained unchanged (no content fabricated), and the claim is flagged as
unverified in the preview so it can be revisited before or during `/sdlc-workflow:plan-feature`.
