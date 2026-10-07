# Steps 2-3 - Reproduce/Trace and Codebase Investigation: ACME-500

## Step 2 - Reproduce / Trace

### Reproduction trace

Following the Steps to Reproduce, the code path is:

1. User creates a `CONVENTIONS.md` with trailing whitespace on a heading line:
   ```
   ## Migration Patterns  \n
   ```
   (two trailing spaces before the newline)

2. User runs `/plan-feature ACME-100`.

3. The plan-feature skill reads `CONVENTIONS.md` and parses section headings using:
   ```python
   for line in conventions_content.split('\n'):
       if line.startswith('## '):
           section_name = line[3:]  # Extracts heading text after "## "
           conventions[section_name] = current_section_content
   ```

4. For the heading `## Migration Patterns  `, `line[3:]` produces `"Migration Patterns  "` (with two trailing spaces). This string is stored as the dictionary key.

5. During task enrichment, the skill looks up conventions by exact name match:
   ```python
   if convention_name in discovered_conventions:
       notes.append(f"Per CONVENTIONS.md {convention_name}: {action}")
   ```

6. The lookup uses `"Migration Patterns"` (no trailing whitespace) as the key. The dictionary contains `"Migration Patterns  "` (with trailing whitespace). The exact match fails, so the convention is silently skipped.

7. No warning or error is emitted. The generated task description omits the convention.

### Reproduction confirmed

The bug is reproducible via the traced code path. The root cause is the missing `.strip()` call on the extracted heading text.

## Step 3 - Codebase Investigation

### Affected files

| File | Symbols / Lines | Role |
|---|---|---|
| `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` | Convention heading extraction loop | Parses CONVENTIONS.md headings without stripping whitespace |
| `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` | Convention-aware task enrichment | Looks up conventions by exact section name match |

### Affected code path

1. **Convention extraction** (`plugins/sdlc-workflow/skills/plan-feature/SKILL.md`):
   - `line[3:]` extracts heading text without calling `.strip()`.
   - The extracted key retains any trailing whitespace from the source file.

2. **Convention lookup** (`plugins/sdlc-workflow/skills/plan-feature/SKILL.md`):
   - `convention_name in discovered_conventions` performs exact string match.
   - Fails when dictionary key has trailing whitespace but lookup key does not.

### Existing test coverage

- `evals/plan-feature/files/conventions-mock.md` -- existing eval fixture for plan-feature conventions.
- This fixture does NOT include trailing whitespace on headings, so the edge case is not covered by current evals.
- No existing test specifically validates convention heading parsing with whitespace variants.

### Persistence-impact analysis

- The buggy function output feeds into task description generation (Implementation Notes section).
- Task descriptions are persisted to Jira via the `jira.create_issue` or `jira.update_issue` MCP calls.
- Impact: tasks created while this bug is present may be missing convention references in their Implementation Notes. This leads to implementers not following required conventions, which could result in non-conformant code.
- No data corruption occurs -- the conventions are simply omitted from task descriptions. Re-running plan-feature after a fix would produce correct output.

### Related patterns

The fix pattern is straightforward: add `.strip()` to the heading extraction. This is a common Python idiom for normalizing parsed text:
```python
section_name = line[3:].strip()
```

Both the extraction site and the lookup site should be considered, but stripping at extraction time is sufficient since it normalizes the dictionary key at the source.
