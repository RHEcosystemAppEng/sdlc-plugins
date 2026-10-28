# Step 4.5 -- Affects Version Resolution

## 4.5.1 -- Check Existing Field

The bug's `affectsVersions` field is NOT populated (value: `(none)`).
No existing versions to keep, replace, or augment. Proceeding to extraction.

## 4.5.2 -- Extract Version from Description

**Environment / Version section content:**

> Not sure which version -- using whatever is deployed on staging.

**Extraction analysis:**

Searched for version patterns:
- Explicit version numbers (e.g., `0.9.0`, `2.1.1`): **none found**
- Product-prefixed versions (e.g., `RHTPA 2.1.0`): **none found**
- Version keywords followed by numbers (e.g., `version 1.2.3`): **none found**

The section contains only vague text. The phrase "whatever is deployed on staging"
does not identify a specific version. The word "version" appears but is not followed
by a numeric version identifier.

**Result**: No version pattern can be extracted from the Environment / Version section.

## 4.5.3 -- Discover Available Jira Versions

Skipped -- no version to match against. Per the skill specification, when no version
pattern can be extracted in sub-step 4.5.2, skip directly to sub-step 4.5.6
(gap flagging).

## 4.5.4 -- Match

Skipped -- no extracted version to match.

## 4.5.5 -- Confirm with User

Skipped -- no match to confirm.

## 4.5.6 -- Flag Gap

**Version could not be determined.** The Environment / Version section contains only
vague, non-specific text ("Not sure which version -- using whatever is deployed on
staging") with no extractable version identifier.

**Action**: Post comment on ACME-511:

> Affects Version could not be determined from the bug description -- please set manually.

The comment would be posted via:

```
jira.add_comment("ACME-511", "Affects Version could not be determined from the
bug description -- please set manually.")
```

with the Comment Footnote appended.

**Reason**: The reporter did not provide a specific version number. The phrase
"whatever is deployed on staging" is insufficiently precise to match against any
Jira project version. A human must determine the staging deployment version and
set the Affects Version field manually.
