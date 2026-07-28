# Step 4.5 – Affects Version Resolution: ACME-500

## 4.5.1 – Check Existing Field

During Step 1, the `affectsVersions` (`versions`) field on ACME-500 was recorded as already
populated with one value: **0.9.0**.

Because the field is non-empty, the skill detects the existing value and presents the following
prompt to the user **before** attempting any version extraction or Jira API lookup:

---

```
Affects Version/s is already set: [0.9.0]

Options:
1. Keep — leave the current value and skip to Step 5
2. Replace — clear and set a new value
3. Augment — add additional versions alongside the current ones

Choose (1/2/3):
```

---

### Behavior for Each Choice

#### Option 1 – Keep (skip remaining sub-steps)
The existing value `0.9.0` is left unchanged on ACME-500.
The skill skips sub-steps 4.5.2 through 4.5.6 and proceeds directly to Step 5 (Generate Task).

**This is the recommended default** — the existing value was presumably set by the reporter or
project tooling and accurately reflects the affected version.

#### Option 2 – Replace (clear and set new value)
The skill clears the existing `0.9.0` value and proceeds to sub-steps 4.5.2–4.5.5 to resolve
a replacement version.

- **Sub-step 4.5.2**: Parse the `### **Environment / Version**` section of the bug description
  for version identifiers. However, **this section is absent** from ACME-500's description body.
  No version pattern can be extracted.
  → Skip to sub-step 4.5.6 (gap flagging).

- **Sub-step 4.5.6**: Post a gap comment on ACME-500:
  > "Affects Version could not be determined from the bug description — please set manually."
  The field is left as-is (still showing `0.9.0`) pending manual update by the assignee.

#### Option 3 – Augment (add versions alongside existing)
The skill proceeds to sub-steps 4.5.2–4.5.5 to discover additional versions to add.

- **Sub-step 4.5.2**: Parse `### **Environment / Version**` section — **absent** from description.
  No additional version text to extract.
  → Skip to sub-step 4.5.6 (gap flagging for additional version).

- **Sub-step 4.5.6**: Post a gap comment noting that no additional version could be determined
  from the description. The existing `0.9.0` value is preserved unchanged.

---

## Decision Rationale

The existing `Affects Version/s: 0.9.0` value was set on the issue prior to triage. Per
Step 4.5.1 of the triage-bug skill, the skill MUST detect this pre-existing value and
surface it to the user rather than silently overwriting it or assuming it is stale. This
ensures human oversight of version metadata, which may have been deliberately set by the
reporter, QE, or project management.

The skill does **not**:
- Silently overwrite the existing value with a newly extracted version
- Skip to Step 5 without showing the user what is already set
- Proceed with version discovery (4.5.2–4.5.5) without first asking the user about the
  existing populated field

## Summary

| Sub-step | Action |
|----------|--------|
| 4.5.1    | Existing value `0.9.0` detected → prompt presented to user (Keep/Replace/Augment) |
| 4.5.2    | Would be skipped on "Keep"; would find no extractable version on "Replace"/"Augment" (section absent) |
| 4.5.3    | Would be called only on "Replace" or "Augment" to list available Jira versions |
| 4.5.4    | Not reached (no version extracted from description) |
| 4.5.5    | Not reached |
| 4.5.6    | Would fire on "Replace"/"Augment" due to missing Environment/Version section |
