# Affects Version Resolution -- ACME-511 (Step 4.5)

## Sub-step 4.5.1 -- Check Existing Field

The `affectsVersions` Jira field on ACME-511 was recorded in Step 1 as **empty**
(not populated). No existing version values to keep, replace, or augment.

Proceeding directly to sub-step 4.5.2.

## Sub-step 4.5.2 -- Extract Version from Description

The **Environment / Version** section content extracted in Step 1:

> "Not sure which version -- using whatever is deployed on staging."

### Version Pattern Search

Scanning for recognizable version identifiers:

| Pattern | Example | Found |
|---------|---------|-------|
| Bare version number | `0.9.0`, `2.1.1` | No |
| Product-prefixed version | `ACME 2.1.0`, `RHTPA 0.9.0` | No |
| Version keyword + number | `version 1.2.3` | No |
| Named release | `v3`, `release-4` | No |

**Result**: No version pattern found. The text "Not sure which version -- using
whatever is deployed on staging" is entirely vague -- it explicitly states the
reporter does not know the version and provides no numeric or named identifier
that could be matched against Jira versions.

**Decision**: Cannot extract a version. Skip sub-steps 4.5.3, 4.5.4, and 4.5.5.
Proceed to sub-step 4.5.6 (gap flagging).

## Sub-step 4.5.6 -- Flag Gap

Version information cannot be determined from the bug description. The
Environment / Version section contains only a vague acknowledgement of uncertainty
("Not sure which version") with no actionable version identifier.

**Action in live execution**: Post the following comment on ACME-511 via
`jira.add_comment`:

```
Affects Version could not be determined from the bug description -- please set manually.
```

(Comment would include the `sdlc-workflow/triage-bug` ADF footnote.)

**The `affectsVersions` field on ACME-511 remains unset.** A human triager must
set this field manually once the affected version is known (e.g., by checking
the staging deployment version or asking the reporter to confirm).

## Summary

| Check | Outcome |
|-------|---------|
| `affectsVersions` pre-populated | No |
| Version text in description | "Not sure which version -- using whatever is deployed on staging." |
| Version pattern extractable | No -- vague text, no version number |
| Jira version lookup performed | Skipped (no extractable version to match) |
| Action taken | Gap flagged; comment posted on bug; field left unset |
