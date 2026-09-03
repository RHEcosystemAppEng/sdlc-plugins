#!/usr/bin/env python3
"""Execute verify-pr structured output actions.

Reads agent-result.json, processes actions sequentially, resolves
{{ref.key}} and {{ref.url}} placeholders as entities are created.

Jira comments (post_comment / post_report) are posted through the native
`fullsend issues post-comment` sticky-comment CLI. The irreducible Jira
writes that have no native primitive yet — sub-tasks, links, and root-cause
tasks — call jira-client.py functions directly (imported as a module).
GitHub operations use the gh CLI. Runs on the fullsend runner (trusted
side), not inside the sandbox.

Not idempotent for entity creation: if an action fails mid-execution,
previously created Jira sub-tasks are not rolled back. Manual cleanup may be
needed after partial failures. Comment posting is idempotent: the Jira sticky
marker updates the existing comment instead of duplicating it, and the GitHub
report comment carries a commit-scoped marker so a retry after a partial
failure updates the same commit's report comment rather than posting a
duplicate.

Usage:
    execute-actions.py <result-json>

Required env vars:
    JIRA_SERVER_URL, JIRA_EMAIL, JIRA_API_TOKEN — Jira credentials
    GH_TOKEN — GitHub token
    JIRA_PROJECT_KEY — Jira project key (for root-cause task creation)
"""

import datetime
import importlib.util
import json
import os
import re
import subprocess
import sys
from typing import Any

_script_dir = os.path.dirname(os.path.abspath(__file__))
_spec = importlib.util.spec_from_file_location(
    "jira_client", os.path.join(_script_dir, "jira-client.py")
)
_jira_mod = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_jira_mod)

REF_PATTERN = re.compile(r"\{\{([a-z0-9-]+)\.(key|url)\}\}")

# Stable marker so the native sticky-comment CLI updates the same Jira
# comment across re-runs instead of posting duplicates. Used by post_report
# (the verification report on the main task).
STICKY_COMMENT_MARKER = "<!-- sdlc-workflow:verify-pr -->"

# Distinct sticky marker for standalone analysis comments (post_comment). The
# native CLI treats the marker as the sticky-comment identity, so a post_comment
# and a post_report targeting the SAME Jira issue in one run must not share one
# marker — otherwise the second post would overwrite the first. Each path keeps
# its own stable marker, so per-path re-run idempotency is preserved.
POST_COMMENT_STICKY_MARKER = "<!-- sdlc-workflow:verify-pr post_comment -->"

# GitHub has no native sticky-comment mechanism, so the verify-pr report comment
# embeds this marker (an invisible HTML comment) in its body. A canonical
# (full-length) commit SHA is appended per post, scoping dedup to a single
# verification run/commit: a retry for the same commit updates the existing
# comment instead of duplicating it, while a later commit gets a fresh comment —
# preserving the per-run verification history that verify-pr SKILL.md Step 9 posts.
GITHUB_REPORT_MARKER_PREFIX = "<!-- sdlc-workflow:verify-pr report commit:"

# Fallback dedup-marker SHA length used only when the commit cannot be resolved to
# its full form (see ``_normalize_commit_sha``). The result schema allows
# commit_sha to be 7-40 hex chars and git abbreviations are prefixes of the full
# SHA, so the schema-minimum 7 chars is the one fixed length that stays invariant
# across a full-vs-abbreviated form of the same commit. (A longer length, e.g. 12,
# would leave a 7-char abbreviation unchanged and still mismatch a full SHA.)
COMMIT_SHA_MARKER_LENGTH = 7

# A canonical, resolved full commit SHA is exactly 40 lowercase hex characters.
_FULL_SHA_RE = re.compile(r"[0-9a-f]{40}")


def _normalize_commit_sha(commit_sha: str) -> str:
    """Canonicalize a commit SHA to its full 40-char form for the dedup marker.

    The result schema allows ``commit_sha`` to be 7-40 hex chars. Truncating every
    form *down* to a shared prefix keeps a full SHA and an abbreviation of the same
    commit invariant, but makes two *distinct* commits that happen to share that
    prefix collide — so a later commit's report could PATCH-overwrite an earlier
    commit's comment. Resolving *up* to the full 40-char SHA via ``git rev-parse``
    keeps the same-commit invariance (a full SHA and any abbreviation of it resolve
    to the same object) while giving distinct commits distinct markers.

    The write path runs host-side in the checked-out repo, so the commit is
    normally resolvable. If ``git`` is unavailable or the value cannot be resolved
    to a full SHA (git missing, object absent, ambiguous abbreviation), it falls
    back to truncating to ``COMMIT_SHA_MARKER_LENGTH`` — the prior fixed-prefix
    behavior, which keeps dedup working (with the rare prefix-collision caveat)
    rather than disabling it.
    """
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--verify", "--quiet", f"{commit_sha}^{{commit}}"],
            capture_output=True, text=True,
        )
    except OSError:
        return commit_sha[:COMMIT_SHA_MARKER_LENGTH]
    resolved = result.stdout.strip()
    if result.returncode == 0 and _FULL_SHA_RE.fullmatch(resolved):
        return resolved
    return commit_sha[:COMMIT_SHA_MARKER_LENGTH]


def resolve_refs(text: str, registry: dict[str, dict[str, str]]) -> str:
    """Replace {{ref.key}} and {{ref.url}} placeholders with resolved values."""
    def replacer(match):
        ref_name, field = match.group(1), match.group(2)
        if ref_name not in registry:
            raise KeyError(f"Unknown ref: {ref_name}")
        return registry[ref_name][field]
    return REF_PATTERN.sub(replacer, text)


def resolve_refs_in_obj(obj: Any, registry: dict[str, dict[str, str]]) -> Any:
    """Recursively resolve refs in a JSON-like object (dicts, lists, strings)."""
    if isinstance(obj, str):
        return resolve_refs(obj, registry)
    if isinstance(obj, list):
        return [resolve_refs_in_obj(item, registry) for item in obj]
    if isinstance(obj, dict):
        return {k: resolve_refs_in_obj(v, registry) for k, v in obj.items()}
    return obj


# ADF inline node types that may appear directly inside a taskItem (per the ADF
# spec) rather than being wrapped in a paragraph block.
_INLINE_NODE_TYPES = {"text", "hardBreak", "mention", "emoji", "inlineCard", "date", "status"}

# Markdown-active characters that the native fullsend CLI reinterprets when it
# re-parses the emitted markdown. Literal occurrences in ADF text nodes must be
# backslash-escaped so they render verbatim (e.g. a literal ``*note*`` stays
# ``*note*`` instead of becoming emphasized). Backslash is listed first so the
# escapes inserted for the other characters are not themselves re-escaped.
_MARKDOWN_ESCAPE_CHARS = ("\\", "`", "*", "_", "[", "]")


def _escape_markdown(text: str) -> str:
    """Backslash-escape markdown-active characters in literal text.

    Applied to a text node's plain value before the renderer wraps it in the
    mark syntax it intentionally adds (``**``, backticks, ``[]()``), so literal
    text round-trips faithfully without double-escaping the marks. Not applied to
    inline-code content, which the CLI treats literally.

    Only *inline* markers are handled here; line-leading block markers (headings,
    lists, blockquotes) are neutralized separately by
    ``_escape_line_leading_markers`` because they are position-sensitive.
    """
    for ch in _MARKDOWN_ESCAPE_CHARS:
        text = text.replace(ch, f"\\{ch}")
    return text


# Line-leading Markdown block markers the native CLI reinterprets when a rendered
# line *starts* with one: ATX headings (``#``..``######`` + space/EOL), blockquotes
# (``>``), bullet lists (``-``/``+`` + space/EOL) and ordered lists (``N.``/``N)`` +
# space/EOL). ``*`` bullets need no entry: ``_escape_markdown`` already escapes ``*``
# everywhere. Each alternative only matches where the construct actually forms, so
# non-markers like ``-5`` or ``1.5`` are left untouched.
_LINE_LEADING_MARKER_RE = re.compile(
    r"""^(?P<indent>[ \t]*)
        (?:
            (?P<heading>\#{1,6})(?=\s|$)
          | (?P<quote>>)
          | (?P<bullet>[-+])(?=\s|$)
          | (?P<ordnum>\d+)(?P<ordsep>[.)])(?=\s|$)
        )
    """,
    re.VERBOSE,
)


def _escape_line_leading_markers(text: str) -> str:
    """Backslash-escape a Markdown block marker at the start of each line.

    Applied to fully-rendered *paragraph* content (the only place literal text
    sits at a true line start, and where a leading ``#``/``-``/``>``/``N.`` would
    otherwise be re-parsed by the native CLI as a heading/list/blockquote). Runs
    per line so markers after a hardBreak are covered too. Intentional block
    markers the renderer itself emits (heading prefixes, list bullets) are added
    by other code paths and never flow through here, so they are not affected.

    A backslash before ASCII punctuation renders as that punctuation, so an
    escape is visually invisible; for ordered lists the ``.``/``)`` separator is
    escaped (``1\\.``) since a backslash before the digit is not a valid escape.
    """
    def _escape_line(line: str) -> str:
        match = _LINE_LEADING_MARKER_RE.match(line)
        if not match:
            return line
        rest = line[match.end():]
        if match.group("ordsep") is not None:
            marker = f"{match.group('ordnum')}\\{match.group('ordsep')}"
        else:
            token = match.group("heading") or match.group("quote") or match.group("bullet")
            marker = f"\\{token}"
        return f"{match.group('indent')}{marker}{rest}"

    return "\n".join(_escape_line(line) for line in text.split("\n"))


def _render_adf_date(timestamp: Any) -> str:
    """Render an ADF ``date`` node's timestamp as a readable ``YYYY-MM-DD`` date.

    ADF ``date`` nodes store ``attrs.timestamp`` as a string of milliseconds
    since the Unix epoch. It is formatted as a UTC calendar date. If the value is
    missing, not an integer, or outside the representable date range, its literal
    form is returned so the node still contributes its value instead of aborting
    the run. ``datetime.fromtimestamp`` can raise ``OverflowError`` or ``OSError``
    (platform-dependent) for out-of-range epoch values, so both are caught here
    alongside the ``int()`` parse errors — an uncaught exception would otherwise
    abort the entire post_script and post nothing.
    """
    try:
        ms = int(timestamp)
        return datetime.datetime.fromtimestamp(
            ms / 1000, tz=datetime.timezone.utc
        ).strftime("%Y-%m-%d")
    except (TypeError, ValueError, OverflowError, OSError):
        return str(timestamp) if timestamp else ""


def _render_adf_inline(nodes: list) -> str:
    """Render a list of ADF inline nodes to markdown.

    Handles every inline leaf type in ``_INLINE_NODE_TYPES``: ``text`` and
    ``hardBreak``, plus the leaf nodes that carry their displayable value in
    ``attrs`` rather than a ``content`` array — ``mention``/``emoji``/``status``
    (``attrs.text``), ``inlineCard`` (``attrs.url``) and ``date``
    (``attrs.timestamp``). These are rendered explicitly so they are not routed
    to the final ``else`` (which recurses into ``content``) and silently dropped
    as empty strings; that keeps the renderer in sync with ``_INLINE_NODE_TYPES``.
    The ``else`` remains for genuinely unknown container-like inline nodes so they
    still degrade gracefully by rendering any nested content.
    """
    parts = []
    for node in nodes:
        node_type = node.get("type")
        if node_type == "text":
            text = node.get("text", "")
            marks = node.get("marks", [])
            mark_types = {m.get("type") for m in marks}
            # Escape markdown-active characters in the literal text before mark
            # wrapping. Inline code is exempt: its content is literal to the CLI
            # and escaping would corrupt inline-code semantics.
            if "code" not in mark_types:
                text = _escape_markdown(text)
            if "code" in mark_types:
                text = f"`{text}`"
            if "strong" in mark_types:
                text = f"**{text}**"
            if "em" in mark_types:
                text = f"*{text}*"
            link = next((m for m in marks if m.get("type") == "link"), None)
            if link:
                href = link.get("attrs", {}).get("href", "")
                text = f"[{text}]({href})"
            parts.append(text)
        elif node_type == "hardBreak":
            parts.append("\n")
        elif node_type in ("mention", "status"):
            # Displayable text lives in attrs.text; escape it as literal text.
            parts.append(_escape_markdown(node.get("attrs", {}).get("text", "")))
        elif node_type == "emoji":
            # Prefer the unicode/text fallback; custom emoji may only have a
            # shortName. Escaped as literal text.
            attrs = node.get("attrs", {})
            parts.append(_escape_markdown(attrs.get("text") or attrs.get("shortName", "")))
        elif node_type == "inlineCard":
            # Render the card's URL as a bare link target; URLs are not escaped.
            parts.append(node.get("attrs", {}).get("url", ""))
        elif node_type == "date":
            parts.append(_render_adf_date(node.get("attrs", {}).get("timestamp", "")))
        else:
            # Unknown inline node — recurse into any nested content.
            parts.append(_render_adf_inline(node.get("content", [])))
    return "".join(parts)


def _render_adf_list(node: dict, *, ordered: bool) -> str:
    """Render an ADF bulletList/orderedList to markdown."""
    lines = []
    for index, item in enumerate(node.get("content", []), start=1):
        marker = f"{index}." if ordered else "-"
        item_md = _render_adf_blocks(item.get("content", []))
        for line_number, line in enumerate(item_md.split("\n")):
            prefix = f"{marker} " if line_number == 0 else "  "
            lines.append(f"{prefix}{line}")
    return "\n".join(lines)


def _render_adf_task_list(node: dict) -> str:
    """Render an ADF taskList to a markdown checklist.

    Each taskItem carries a ``state`` attr of ``DONE`` or ``TODO``, rendered as
    ``- [x]`` / ``- [ ]``. taskItem content may be inline nodes (ADF spec) or
    paragraph blocks (as ``sanitize_adf`` and some producers treat them); both
    are handled so no variant falls through to the flattening unknown-block path.
    """
    lines = []
    for item in node.get("content", []):
        if item.get("type") != "taskItem":
            continue
        state = item.get("attrs", {}).get("state", "TODO")
        marker = "- [x]" if state == "DONE" else "- [ ]"
        content = item.get("content", [])
        if content and all(child.get("type") in _INLINE_NODE_TYPES for child in content):
            item_md = _render_adf_inline(content)
        else:
            item_md = _render_adf_blocks(content)
        for line_number, line in enumerate(item_md.split("\n")):
            prefix = f"{marker} " if line_number == 0 else "  "
            lines.append(f"{prefix}{line}")
    return "\n".join(lines)


def _render_adf_blockquote(node: dict) -> str:
    """Render an ADF ``blockquote``/``panel`` as markdown ``> ``-prefixed lines.

    The framing children are rendered as ordinary blocks and every resulting line
    (blank lines included, so the quote stays contiguous) gets the ``> `` prefix.
    A ``panel``'s ``attrs.panelType`` (e.g. ``info``/``warning``) is emitted as a
    leading bold label so the panel's kind is not lost in the markdown, which has
    no native panel construct.
    """
    inner = _render_adf_blocks(node.get("content", []))
    lines = inner.split("\n") if inner else [""]
    panel_type = node.get("attrs", {}).get("panelType")
    if panel_type:
        lines = [f"**{panel_type}**", ""] + lines
    return "\n".join(f"> {line}".rstrip() for line in lines)


def _render_adf_table_cell(cell: dict) -> str:
    """Render one ADF ``tableCell``/``tableHeader`` to a single GFM table cell.

    Cell content is block-level (usually a paragraph), but a GFM cell must be one
    line, so inter-block newlines are collapsed to spaces and any literal pipe is
    escaped so it does not break the column structure.
    """
    text = _render_adf_blocks(cell.get("content", []))
    return text.replace("\n", " ").replace("|", "\\|").strip()


def _render_adf_table(node: dict) -> str:
    """Render an ADF ``table`` to a GitHub-flavored markdown table.

    The first ``tableRow`` is treated as the header row (followed by the ``---``
    separator); remaining rows are body rows. The separator is sized to the header
    column count so the table is well-formed even when body rows are ragged.
    """
    rows = [row for row in node.get("content", []) if row.get("type") == "tableRow"]
    if not rows:
        return ""
    rendered = [
        [_render_adf_table_cell(cell) for cell in row.get("content", [])]
        for row in rows
    ]
    header = rendered[0]
    lines = [
        "| " + " | ".join(header) + " |",
        "| " + " | ".join(["---"] * len(header)) + " |",
    ]
    for body_row in rendered[1:]:
        lines.append("| " + " | ".join(body_row) + " |")
    return "\n".join(lines)


def _render_adf_media(node: dict) -> str:
    """Render an ADF ``media``/``mediaSingle``/``mediaGroup`` node.

    A ``mediaSingle``/``mediaGroup`` wraps one or more ``media`` children; each is
    rendered as a markdown image ``![alt](url)`` when a URL attr is present, or a
    non-empty ``[alt]`` placeholder otherwise — never dropped silently. Attachment
    media (``type: file`` with only an ``id``) has no dereferenceable URL here, so
    it falls back to the alt/id placeholder.
    """
    if node.get("type") in ("mediaSingle", "mediaGroup"):
        parts = [_render_adf_media(child) for child in node.get("content", [])
                 if child.get("type") == "media"]
        return "\n".join(part for part in parts if part)
    attrs = node.get("attrs", {})
    url = attrs.get("url", "")
    alt = attrs.get("alt") or attrs.get("id") or "media"
    return f"![{alt}]({url})" if url else f"[{alt}]"


def _render_adf_block(node: dict) -> str:
    """Render a single ADF block node to markdown."""
    node_type = node.get("type")
    if node_type == "paragraph":
        return _escape_line_leading_markers(_render_adf_inline(node.get("content", [])))
    if node_type == "heading":
        level = node.get("attrs", {}).get("level", 1)
        return f"{'#' * level} {_render_adf_inline(node.get('content', []))}"
    if node_type == "rule":
        return "---"
    if node_type == "codeBlock":
        language = node.get("attrs", {}).get("language", "") or ""
        code = "".join(child.get("text", "") for child in node.get("content", []))
        return f"```{language}\n{code}\n```"
    if node_type == "bulletList":
        return _render_adf_list(node, ordered=False)
    if node_type == "orderedList":
        return _render_adf_list(node, ordered=True)
    if node_type == "taskList":
        return _render_adf_task_list(node)
    if node_type in ("blockquote", "panel"):
        return _render_adf_blockquote(node)
    if node_type == "table":
        return _render_adf_table(node)
    if node_type in ("media", "mediaSingle", "mediaGroup"):
        return _render_adf_media(node)
    # Unknown block — recurse into nested content.
    return _render_adf_blocks(node.get("content", []))


def _render_adf_blocks(nodes: list) -> str:
    """Render a list of ADF block nodes to markdown, separated by blank lines."""
    blocks = [_render_adf_block(node) for node in nodes]
    return "\n\n".join(block for block in blocks if block)


def adf_to_markdown(doc: dict) -> str:
    """Render an ADF document to markdown (inverse of jira-client's markdown_to_adf).

    The native ``fullsend issues post-comment`` CLI consumes markdown on stdin,
    but the result schema carries ``post_comment`` bodies as ADF (``body_adf``).
    This renders the ADF back to markdown covering the node set markdown_to_adf
    produces: headings, paragraphs, bullet/ordered lists, code blocks, rules, and
    the strong/em/code/link inline marks. taskList/taskItem nodes (which agents may
    emit directly in ``body_adf``) render as markdown checklists (``- [ ]`` /
    ``- [x]``). Additional block nodes an agent may emit in ``body_adf`` are also
    rendered rather than flattened: ``blockquote``/``panel`` as ``> `` quotes,
    ``table`` as a GitHub-flavored markdown table, and ``media``/``mediaSingle``/
    ``mediaGroup`` as an image link or ``[alt]`` placeholder. Non-text inline leaf
    nodes (``mention``/``emoji``/``status``/``inlineCard``/``date``) are rendered
    from their ``attrs``. Genuinely unknown container nodes still degrade
    gracefully by recursing into their nested content.
    """
    if not isinstance(doc, dict):
        raise TypeError("adf_to_markdown expects an ADF document object")
    return _render_adf_blocks(doc.get("content", []))


def build_issue_url(key: str) -> str:
    """Build Jira issue browse URL from key."""
    server = os.environ.get("JIRA_SERVER_URL", "").rstrip("/")
    if not server:
        print("JIRA_SERVER_URL is required for issue URL construction", file=sys.stderr)
        sys.exit(1)
    return f"{server}/browse/{key}"


def _jira_native_env() -> dict[str, str]:
    """Build the environment for the native fullsend Jira CLI.

    Maps this script's JIRA_SERVER_URL / JIRA_EMAIL / JIRA_API_TOKEN onto the
    JIRA_BASE_URL / JIRA_USER_EMAIL / JIRA_TOKEN names the fullsend CLI expects.
    Exits with a clear message if any credential is missing.
    """
    try:
        return {
            **os.environ,
            "JIRA_BASE_URL": os.environ["JIRA_SERVER_URL"],
            "JIRA_USER_EMAIL": os.environ["JIRA_EMAIL"],
            "JIRA_TOKEN": os.environ["JIRA_API_TOKEN"],
        }
    except KeyError as e:
        print(f"Missing required env var for native Jira comment: {e.args[0]}", file=sys.stderr)
        sys.exit(1)


def post_jira_comment_native(
    issue_key: str, body_md: str, marker: str = STICKY_COMMENT_MARKER
) -> None:
    """Post a Jira comment via the native fullsend sticky-comment CLI.

    The body is passed as markdown on stdin (``--result -``). The ``marker`` is
    the sticky-comment identity: re-runs with the same marker update the existing
    comment rather than creating duplicates. Callers pass a per-purpose marker so
    two comments on the same issue (report vs analysis) do not clobber each other;
    the default preserves the report path's historical marker.
    """
    project, _, number = issue_key.rpartition("-")
    if not project or not number:
        print(f"Invalid Jira issue key: {issue_key}", file=sys.stderr)
        sys.exit(1)

    result = subprocess.run(
        ["fullsend", "issues", "post-comment", "--tracker", "jira",
         "--project", project, "--number", number,
         "--marker", marker, "--result", "-"],
        input=body_md, text=True, capture_output=True,
        env=_jira_native_env(),
    )
    if result.returncode != 0:
        print(f"fullsend post-comment failed for {issue_key}: {result.stderr}", file=sys.stderr)
        sys.exit(1)


def _create_and_register(action: dict, registry: dict, *,
                        project_key: str, issue_type: str,
                        parent: str | None = None, label: str = "issue") -> None:
    ref = action["ref"]
    summary = resolve_refs(action["summary"], registry)
    labels = action["labels"]
    description_adf = resolve_refs_in_obj(action["description_adf"], registry)

    try:
        result = _jira_mod.create_issue(
            project_key=project_key,
            summary=summary,
            issue_type=issue_type,
            parent=parent,
            description_adf=description_adf,
            labels=labels,
        )
    except SystemExit:
        print(f"  Failed to create {label}: {summary}", file=sys.stderr)
        sys.exit(1)

    key = result.get("key", "")
    url = build_issue_url(key)
    registry[ref] = {"key": key, "url": url}
    print(f"  Created {label}: {key} (ref: {ref})")


def execute_create_subtask(action: dict, registry: dict) -> None:
    parent = resolve_refs(action["parent"], registry)
    _create_and_register(
        action, registry,
        project_key=parent.split("-")[0],
        issue_type="Sub-task",
        parent=parent,
        label="sub-task",
    )


def execute_create_link(action: dict, registry: dict) -> None:
    link_type = action["link_type"]
    inward = resolve_refs(action["inward"], registry)
    outward = resolve_refs(action["outward"], registry)

    try:
        _jira_mod.create_link(
            inward_issue=inward,
            outward_issue=outward,
            link_type=link_type,
        )
    except SystemExit:
        print(f"  Failed to create link: {inward} {link_type} {outward}", file=sys.stderr)
        sys.exit(1)

    print(f"  Created link: {inward} {link_type} {outward}")


def execute_post_pr_reply(action: dict, registry: dict) -> None:
    repo = action["repo"]
    pr_number = action["pr_number"]
    comment_id = action["comment_id"]
    body = resolve_refs(action["body"], registry)

    result = subprocess.run(
        ["gh", "api",
         f"repos/{repo}/pulls/{pr_number}/comments/{comment_id}/replies",
         "-f", f"body={body}"],
        capture_output=True, text=True,
    )
    if result.returncode != 0:
        print(f"gh api failed: {result.stderr}", file=sys.stderr)
        sys.exit(1)
    print(f"  Posted PR reply on comment {comment_id}")


def execute_post_pr_comment(action: dict, registry: dict) -> None:
    repo = action["repo"]
    pr_number = action["pr_number"]
    body = resolve_refs(action["body"], registry)

    result = subprocess.run(
        ["gh", "api",
         f"repos/{repo}/issues/{pr_number}/comments",
         "-f", f"body={body}"],
        capture_output=True, text=True,
    )
    if result.returncode != 0:
        print(f"gh api failed: {result.stderr}", file=sys.stderr)
        sys.exit(1)
    print(f"  Posted PR comment on #{pr_number}")


def execute_create_root_cause_task(action: dict, registry: dict) -> None:
    project_key = os.environ.get("JIRA_PROJECT_KEY", "")
    if not project_key:
        print("JIRA_PROJECT_KEY is required for root-cause task creation", file=sys.stderr)
        sys.exit(1)

    _create_and_register(
        action, registry,
        project_key=project_key,
        issue_type="Task",
        label="root-cause task",
    )


def execute_post_comment(action: dict, registry: dict) -> None:
    issue = resolve_refs(action["issue"], registry)
    body_adf = resolve_refs_in_obj(action["body_adf"], registry)
    body_md = adf_to_markdown(body_adf)

    post_jira_comment_native(issue, body_md, marker=POST_COMMENT_STICKY_MARKER)
    print(f"  Posted comment on {issue}")


def _find_report_comment_id(repo: str, pr_number: int, marker: str) -> int | None:
    """Return the id of an existing PR report comment whose body carries ``marker``.

    Lists the PR's issue-level comments and matches on the commit-scoped marker
    so a retry updates the same commit's report comment instead of duplicating
    it. Returns ``None`` when no marked comment exists yet.

    ``--slurp`` is required alongside ``--paginate``: without it ``gh`` emits one
    JSON array per page concatenated (``[...][...]``), which is not valid combined
    JSON once the PR has more than one page of comments (>30) and would fail to
    parse. ``--slurp`` wraps the per-page arrays in a single outer array, so the
    output is valid JSON regardless of page count; the pages are then flattened
    into one comment list. A parse failure is a real error (surfaced via
    ``sys.exit``), never silently treated as "no existing comment" — doing so
    would defeat retry idempotency by creating a duplicate report comment.
    """
    result = subprocess.run(
        ["gh", "api", f"repos/{repo}/issues/{pr_number}/comments",
         "--paginate", "--slurp"],
        capture_output=True, text=True,
    )
    if result.returncode != 0:
        print(f"Failed to list PR comments: {result.stderr}", file=sys.stderr)
        sys.exit(1)
    try:
        pages = json.loads(result.stdout or "[]")
    except json.JSONDecodeError as e:
        print(f"Failed to parse PR comments JSON: {e}", file=sys.stderr)
        sys.exit(1)
    comments = [comment for page in pages for comment in page]
    for comment in comments:
        if marker in (comment.get("body") or ""):
            return comment.get("id")
    return None


def execute_post_report(action: dict, registry: dict, report: dict) -> None:
    """Post the verification report to the GitHub PR and the Jira issue.

    The GitHub comment carries a commit-scoped marker
    (``GITHUB_REPORT_MARKER_PREFIX`` + the canonical full commit SHA): if a prior
    report comment for the same commit exists it is updated in place
    (``gh api ... -X PATCH``)
    instead of creating a duplicate, so a retry after a partial failure is
    idempotent while a new commit still gets a fresh comment. The Jira side is
    already idempotent via its sticky marker; it receives the report rendered
    from ``report_adf`` (the tracker-native body) via ``adf_to_markdown``, which
    the native CLI converts back to ADF — the GitHub-only ``report_md`` (and its
    embedded marker) is never sent to Jira.
    """
    repo = report["pr_repo"]
    pr_number = report["pr_number"]
    jira_issue_id = report["jira_issue_id"]
    commit_sha = report["commit_sha"]
    report_md = resolve_refs(report["report_md"], registry)
    report_adf = resolve_refs_in_obj(report["report_adf"], registry)
    jira_body_md = adf_to_markdown(report_adf)

    marker = f"{GITHUB_REPORT_MARKER_PREFIX}{_normalize_commit_sha(commit_sha)} -->"
    github_body = f"{report_md}\n\n{marker}"

    existing_id = _find_report_comment_id(repo, pr_number, marker)
    if existing_id is not None:
        result = subprocess.run(
            ["gh", "api", f"repos/{repo}/issues/comments/{existing_id}",
             "-X", "PATCH", "-f", f"body={github_body}"],
            capture_output=True, text=True,
        )
        if result.returncode != 0:
            print(f"Failed to update GitHub PR comment: {result.stderr}", file=sys.stderr)
            sys.exit(1)
        print(f"  Updated existing report comment on PR #{pr_number}")
    else:
        result = subprocess.run(
            ["gh", "pr", "comment", str(pr_number), "--body", github_body, "-R", repo],
            capture_output=True, text=True,
        )
        if result.returncode != 0:
            print(f"Failed to post GitHub PR comment: {result.stderr}", file=sys.stderr)
            sys.exit(1)
        print(f"  Posted report to PR #{pr_number}")

    post_jira_comment_native(jira_issue_id, jira_body_md)
    print(f"  Posted report to Jira {jira_issue_id}")


EXECUTORS = {
    "create_subtask": execute_create_subtask,
    "create_link": execute_create_link,
    "post_pr_reply": execute_post_pr_reply,
    "post_pr_comment": execute_post_pr_comment,
    "create_root_cause_task": execute_create_root_cause_task,
    "post_comment": execute_post_comment,
}


def main():
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <result-json>", file=sys.stderr)
        sys.exit(1)

    result_path = sys.argv[1]
    with open(result_path) as f:
        data = json.load(f)

    report = data["report"]
    actions = data["actions"]
    registry: dict[str, dict[str, str]] = {}

    print(f"Executing {len(actions)} actions for {report['jira_issue_id']}...")

    # post_report resolves {{ref.key}} placeholders in report_md against the
    # registry, which the entity-creating actions (create_subtask,
    # create_root_cause_task) populate as they run. Defer every post_report until
    # after the actions loop so the registry is fully populated first — otherwise
    # a post_report ordered before an action it references would raise an
    # uncaught KeyError from resolve_refs and abort the run. verify-pr already
    # emits post_report last, so this only removes an undocumented,
    # order-dependent trap; it does not change the observed behavior.
    deferred_reports: list[dict] = []

    for i, action in enumerate(actions):
        action_type = action["type"]
        print(f"[{i + 1}/{len(actions)}] {action_type}")

        if action_type == "post_report":
            deferred_reports.append(action)
        elif action_type in EXECUTORS:
            EXECUTORS[action_type](action, registry)
        else:
            print(f"  Unknown action type: {action_type}", file=sys.stderr)
            sys.exit(1)

    for action in deferred_reports:
        execute_post_report(action, registry, report)

    print(f"Done. {len(actions)} actions executed successfully.")


if __name__ == "__main__":
    main()
