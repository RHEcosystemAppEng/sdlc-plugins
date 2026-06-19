# Implementation Plan for TC-9205: Add migration to drop status table column

## Task Summary

**Jira Key:** TC-9205
**Summary:** Add a database migration that drops the deprecated `status` column from the `advisory` table.
**Repository:** trustify-backend
**Target Branch:** TC-9005 (feature branch)
**Linked Issues:** is incorporated by TC-9005
**Labels:** ai-generated-jira

## Branch Operations

1. **Checkout the target feature branch:**
   ```
   git checkout TC-9005
   git pull
   ```

2. **Create the task branch from the feature branch:**
   ```
   git checkout -b TC-9205
   ```

   The task branch `TC-9205` is created FROM `TC-9005`, not from `main`. This is because the Target Branch field specifies `TC-9005`, indicating this task is part of a feature branch workflow where TC-9205 is incorporated by TC-9005.

## Files to Create

### 1. `migration/src/m0002_drop_advisory_status/mod.rs`
- New migration module implementing `MigrationTrait`
- `up` method: drops the `status` column from the `advisory` table using `TableAlterStatement`
- `down` method: re-adds the `status` column as a nullable string for rollback
- Follows the sibling pattern established in `migration/src/m0001_initial/mod.rs`

## Files to Modify

### 2. `migration/src/lib.rs`
- Register the new `m0002_drop_advisory_status` migration module
- Add it to the `vec![]` in the `migrations()` function, following the existing pattern of `m0001_initial` registration

## Files to Verify (no modification expected)

### 3. `entity/src/advisory.rs`
- Verify that this entity file no longer references the `status` column
- This is a pre-implementation verification step per the Implementation Notes

## Commit Message

```
feat(migration): add migration to drop advisory status column

Add database migration m0002_drop_advisory_status that drops the
deprecated `status` column from the `advisory` table. The column was
replaced by the `severity` enum field in a previous migration and is
no longer read or written by any service code.

The migration includes a rollback (down) method that re-adds the
column as a nullable string.

Implements TC-9205
```

With the trailer flag:
```
git commit --trailer="Assisted-by: Claude Code" -m "feat(migration): add migration to drop advisory status column

Add database migration m0002_drop_advisory_status that drops the
deprecated `status` column from the `advisory` table. The column was
replaced by the \`severity\` enum field in a previous migration and is
no longer read or written by any service code.

The migration includes a rollback (down) method that re-adds the
column as a nullable string.

Implements TC-9205"
```

## Push and PR Creation

```
git push -u origin TC-9205
```

```
gh pr create --base TC-9005 --title "feat(migration): add migration to drop advisory status column" --body "$(cat <<'EOF'
## Summary

Add database migration `m0002_drop_advisory_status` that drops the deprecated `status` column from the `advisory` table. The column was replaced by the `severity` enum field and is no longer referenced by any service or entity code.

- New migration file: `migration/src/m0002_drop_advisory_status/mod.rs`
- Migration registered in `migration/src/lib.rs`
- Rollback support: `down` method re-adds the column as a nullable string

Implements [TC-9205](https://redhat.atlassian.net/browse/TC-9205)

## Test Plan

- [ ] Migration runs successfully against a test database (`cargo test`)
- [ ] Rollback (down) re-adds the `status` column as a nullable string
- [ ] Existing advisory queries continue to work after column removal
- [ ] No service or entity code references the dropped `status` column
EOF
)"
```

**Critical:** The PR targets `--base TC-9005` (the feature branch), NOT `--base main`. This is because the Target Branch in the task description specifies TC-9005.

## Jira Updates

1. Update the Git Pull Request custom field (`customfield_10875`) with the PR URL in ADF format
2. Add a comment summarizing:
   - PR link
   - Changes made (new migration file, registration in lib.rs)
   - Confirmation that entity/src/advisory.rs does not reference the status column
3. Transition TC-9205 to "In Review"

## Self-Verification Checklist

- [ ] Scope containment: only `migration/src/m0002_drop_advisory_status/mod.rs` (created) and `migration/src/lib.rs` (modified) are changed
- [ ] `entity/src/advisory.rs` verified to not reference `status` column
- [ ] No sensitive patterns in diff
- [ ] Duplication check: no existing migration drops the same column
- [ ] Data-flow trace: migration up drops column, down re-adds it -- complete lifecycle
- [ ] Contract verification: `MigrationTrait` fully implemented (up + down methods)
- [ ] Sibling parity with `m0001_initial/mod.rs`: same structure, same trait implementation pattern
