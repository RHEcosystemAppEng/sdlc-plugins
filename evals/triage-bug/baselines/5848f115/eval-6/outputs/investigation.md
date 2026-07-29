# Step 3 -- Codebase Investigation: ACME-500

## Target Repository

| Field | Value |
|---|---|
| Repository | acme-backend |
| Role | Rust backend service |
| Serena Instance | serena_backend |
| Path | /home/dev/repos/acme-backend |

The **Component** field is `sdlc-workflow`, and the Steps to Reproduce reference the `plan-feature` skill, pointing to the `plugins/sdlc-workflow/skills/plan-feature/` directory within the acme-backend repository.

## Code Intelligence Note

Per CLAUDE.md: "No Serena MCP servers are configured. Code intelligence is not available." Investigation uses Read/Grep/Glob fallback.

## Affected Code Paths

### 1. Convention Heading Extraction (Root Cause Location)

**File:** `plugins/sdlc-workflow/skills/plan-feature/SKILL.md`
**Section:** Convention conformance analysis

```python
for line in conventions_content.split('\n'):
    if line.startswith('## '):
        section_name = line[3:]  # Extracts heading text after "## "
        conventions[section_name] = current_section_content
```

**Finding:** The heading extraction at `line[3:]` does NOT strip trailing whitespace. When the heading line is `## Migration Patterns  \n`, the extracted section name becomes `"Migration Patterns  "` (with two trailing spaces). This is the primary defect location.

### 2. Convention-Aware Task Enrichment (Failure Manifestation)

**File:** `plugins/sdlc-workflow/skills/plan-feature/SKILL.md`
**Section:** Convention-aware task enrichment

```python
if convention_name in discovered_conventions:
    notes.append(f"Per CONVENTIONS.md {convention_name}: {action}")
```

**Finding:** The `convention_name` lookup uses an exact match against `discovered_conventions`. When the key in the dictionary has trailing whitespace (`"Migration Patterns  "`) but the lookup key does not (`"Migration Patterns"`), the match fails silently. No warning or error is logged -- the convention is simply skipped.

### 3. Existing Test Coverage

**File:** `evals/plan-feature/files/conventions-mock.md`

**Finding:** The existing eval fixture for plan-feature conventions does NOT include trailing whitespace on headings. This edge case is not covered by current evals, explaining why the bug was not caught during development.

### 4. CONVENTIONS.md at Repository Root

The repository does not have a `CONVENTIONS.md` at its root. No conventions to carry forward to the task's Implementation Notes from the target repository itself.

## Persistence-Impact Analysis

The buggy function's output (the `conventions` dictionary with section names as keys) is used to generate task descriptions in Jira. Task descriptions are persisted in Jira (external system), but the bug only affects future task generation -- it does not corrupt stored data in the repository's database.

**Persistence boundary:** The convention data flows to Jira task descriptions via the `notes.append()` call, but the bug causes the convention to be omitted entirely rather than storing an incorrect value. Once the code is fixed, newly generated tasks will correctly include the conventions.

**Conclusion:** No data migration is needed. The fix corrects future behavior. Previously generated tasks that are missing convention references would need manual review, but this is outside the scope of a code fix.

## Summary of Affected Files

| File | Symbol/Area | Role |
|---|---|---|
| `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` | Convention heading extraction (`line[3:]`) | Primary defect -- missing `.strip()` |
| `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` | Convention-aware task enrichment (`convention_name in discovered_conventions`) | Failure manifestation -- silent skip |
| `evals/plan-feature/files/conventions-mock.md` | Eval fixture | Missing edge case coverage |

## Existing Test Patterns

The eval directory `evals/plan-feature/` contains mock data files for testing the plan-feature skill. The reproducer test should follow the same pattern:
- Add a conventions mock file with trailing whitespace on headings
- Verify that the convention is correctly matched and included in generated output
