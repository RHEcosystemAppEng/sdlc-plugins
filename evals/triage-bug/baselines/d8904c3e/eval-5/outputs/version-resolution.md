# Step 4.5 -- Affects Version Resolution

## 4.5.1 -- Check Existing Field

The bug's `affectsVersions` field is **not populated** (recorded as "(none)" in Step 1
metadata). There are no existing versions to keep, replace, or augment. Proceeding to
sub-step 4.5.2.

## 4.5.2 -- Extract Version from Description

**Environment / Version section content:**
> Not sure which version -- using whatever is deployed on staging.

**Version extraction analysis:**

Scanned the Environment / Version text for version identifiers:

| Pattern Type | Pattern | Found | Match |
|---|---|---|---|
| Explicit version number | `\d+\.\d+(\.\d+)?` (e.g., `0.9.0`, `2.1.1`) | No | -- |
| Product-prefixed version | `[A-Z]+ \d+\.\d+` (e.g., `RHTPA 2.1.0`) | No | -- |
| Version keyword + number | `version \d+` (e.g., `version 1.2.3`) | No | -- |
| Build/commit identifiers | SHA, build number | No | -- |

The section contains only vague, non-actionable text:
- "Not sure which version" -- explicitly states uncertainty
- "whatever is deployed on staging" -- references an environment (staging) but
  provides no version identifier

**Result**: No version pattern can be extracted from the Environment / Version section.
The text is classified as vague/indeterminate. Skipping sub-steps 4.5.3 (Discover
Available Jira Versions), 4.5.4 (Match), and 4.5.5 (Confirm with User).

Proceeding directly to sub-step 4.5.6 (Flag Gap).

## 4.5.3 -- Discover Available Jira Versions

**Skipped** -- no version identifier was extracted in 4.5.2 to match against.

## 4.5.4 -- Match

**Skipped** -- no version identifier was extracted in 4.5.2.

## 4.5.5 -- Confirm with User

**Skipped** -- no match to confirm.

## 4.5.6 -- Flag Gap

**Trigger**: Version information could not be extracted from the bug description
(sub-step 4.5.2 found no actionable version text).

**Action**: Post comment on ACME-511:

> Affects Version could not be determined from the bug description -- please set
> manually.

The comment would be posted via:

```
jira.add_comment("ACME-511", "Affects Version could not be determined from the
bug description -- please set manually.")
```

With Comment Footnote appended (sdlc-workflow/triage-bug v0.13.7).

**Reason**: The reporter wrote "Not sure which version -- using whatever is deployed
on staging" in the Environment / Version section, which contains no extractable version
number, product-prefixed version string, or version keyword followed by a number. The
Affects Version field on ACME-511 remains unset and requires manual resolution by the
reporter or project maintainer.
