#!/usr/bin/env python3
"""Tests for execute-actions.py ref resolution and native Jira comment posting."""

import sys
import os
import json
import tempfile
import importlib.util

from jsonschema import validate, ValidationError

script_dir = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location(
    "execute_actions",
    os.path.join(script_dir, "execute-actions.py"),
)
execute_actions = importlib.util.module_from_spec(spec)
spec.loader.exec_module(execute_actions)

resolve_refs = execute_actions.resolve_refs

# The result schema the fullsend validation_loop enforces before the post_script
# runs. Loaded once so the schema-validation tests below assert against the real
# shipped constraints rather than a reimplementation.
_RESULT_SCHEMA_PATH = os.path.join(
    script_dir, "..", "schemas", "verify-pr-result.schema.json"
)
with open(_RESULT_SCHEMA_PATH) as _schema_f:
    _RESULT_SCHEMA = json.load(_schema_f)

# Validate a single action instance against the schema's action definition. The
# action def carries no external $refs, so wrapping it with the document's $defs
# and dialect lets `validate` exercise the post_comment if/then branch directly.
_ACTION_SCHEMA = {
    "$schema": _RESULT_SCHEMA["$schema"],
    "$defs": _RESULT_SCHEMA["$defs"],
    "$ref": "#/$defs/action",
}


def test_resolve_refs_replaces_key():
    """A single {{ref.key}}/{{ref.url}} pair resolves to registered values."""
    registry = {"subtask-1": {"key": "TC-100", "url": "https://jira.example.com/browse/TC-100"}}
    text = "Sub-task [{{subtask-1.key}}]({{subtask-1.url}}) created."
    result = resolve_refs(text, registry)
    assert result == "Sub-task [TC-100](https://jira.example.com/browse/TC-100) created.", f"Got: {result}"


def test_resolve_refs_no_placeholders():
    """Text without placeholders is returned unchanged."""
    registry = {}
    text = "No placeholders here."
    result = resolve_refs(text, registry)
    assert result == "No placeholders here."


def test_resolve_refs_unknown_ref_raises():
    """An unregistered ref raises KeyError."""
    registry = {}
    text = "{{unknown-ref.key}}"
    try:
        resolve_refs(text, registry)
        assert False, "Should have raised KeyError"
    except KeyError:
        pass


def test_resolve_refs_in_adf():
    """resolve_refs_in_obj resolves placeholders nested inside an ADF doc."""
    registry = {"rc-1": {"key": "TC-200", "url": "https://jira.example.com/browse/TC-200"}}
    adf = {
        "type": "doc",
        "content": [
            {"type": "text", "text": "Task {{rc-1.key}} created"}
        ]
    }
    result = execute_actions.resolve_refs_in_obj(adf, registry)
    assert result["content"][0]["text"] == "Task TC-200 created"


def test_resolve_refs_multiple_different_refs():
    """Multiple distinct refs in one string each resolve independently."""
    registry = {
        "subtask-1": {"key": "TC-100", "url": "https://jira.example.com/browse/TC-100"},
        "rc-1": {"key": "TC-200", "url": "https://jira.example.com/browse/TC-200"},
    }
    text = "Sub-task {{subtask-1.key}} and root-cause {{rc-1.key}} ({{rc-1.url}})."
    result = resolve_refs(text, registry)
    assert result == "Sub-task TC-100 and root-cause TC-200 (https://jira.example.com/browse/TC-200).", f"Got: {result}"


def test_resolve_refs_repeated_placeholder():
    """A placeholder repeated in one string resolves at every occurrence."""
    registry = {"subtask-1": {"key": "TC-100", "url": "https://jira.example.com/browse/TC-100"}}
    text = "{{subtask-1.key}} depends on {{subtask-1.key}}."
    result = resolve_refs(text, registry)
    assert result == "TC-100 depends on TC-100.", f"Got: {result}"


def test_resolve_refs_mixed_key_url_same_ref():
    """The .key and .url fields of one ref resolve to their respective values."""
    registry = {"subtask-1": {"key": "TC-100", "url": "https://jira.example.com/browse/TC-100"}}
    text = "See {{subtask-1.key}} at {{subtask-1.url}}; {{subtask-1.key}} must be done first."
    result = resolve_refs(text, registry)
    assert result == "See TC-100 at https://jira.example.com/browse/TC-100; TC-100 must be done first.", f"Got: {result}"


class _FakeCompleted:
    """Stand-in for subprocess.CompletedProcess."""

    def __init__(self, returncode=0, stderr="", stdout=""):
        self.returncode = returncode
        self.stderr = stderr
        self.stdout = stdout


class _RunRecorder:
    """Captures the argv/input/env of a single subprocess.run call."""

    def __init__(self, returncode=0, stderr=""):
        self.returncode = returncode
        self.stderr = stderr
        self.cmd = None
        self.input = None
        self.env = None

    def __call__(self, cmd, input=None, text=None, capture_output=None, env=None):
        self.cmd = cmd
        self.input = input
        self.env = env
        return _FakeCompleted(self.returncode, self.stderr)


_JIRA_ENV = {
    "JIRA_SERVER_URL": "https://jira.example.com",
    "JIRA_EMAIL": "bot@example.com",
    "JIRA_API_TOKEN": "s3cr3t",
}


def _with_jira_env_and_recorder(recorder):
    """Install a fake subprocess.run + Jira env; return a restore callback."""
    saved_run = execute_actions.subprocess.run
    saved_env = {k: os.environ.get(k) for k in _JIRA_ENV}
    execute_actions.subprocess.run = recorder
    os.environ.update(_JIRA_ENV)

    def restore():
        execute_actions.subprocess.run = saved_run
        for k, v in saved_env.items():
            if v is None:
                os.environ.pop(k, None)
            else:
                os.environ[k] = v

    return restore


def test_post_jira_comment_native_builds_argv():
    """post_jira_comment_native calls the native CLI with marker, project, and number."""
    recorder = _RunRecorder()
    restore = _with_jira_env_and_recorder(recorder)
    try:
        execute_actions.post_jira_comment_native("TC-321", "hello **world**")
    finally:
        restore()

    assert recorder.cmd[:4] == ["fullsend", "issues", "post-comment", "--tracker"], f"Got: {recorder.cmd}"
    assert "jira" in recorder.cmd
    assert "--project" in recorder.cmd and recorder.cmd[recorder.cmd.index("--project") + 1] == "TC"
    assert "--number" in recorder.cmd and recorder.cmd[recorder.cmd.index("--number") + 1] == "321"
    assert "--marker" in recorder.cmd
    assert recorder.cmd[recorder.cmd.index("--marker") + 1] == execute_actions.STICKY_COMMENT_MARKER
    assert "--result" in recorder.cmd and recorder.cmd[recorder.cmd.index("--result") + 1] == "-"
    assert recorder.input == "hello **world**"


def test_post_jira_comment_native_maps_env():
    """The native CLI receives JIRA_BASE_URL/JIRA_USER_EMAIL/JIRA_TOKEN mapped from this script's vars."""
    recorder = _RunRecorder()
    restore = _with_jira_env_and_recorder(recorder)
    try:
        execute_actions.post_jira_comment_native("TC-1", "body")
    finally:
        restore()

    assert recorder.env["JIRA_BASE_URL"] == "https://jira.example.com"
    assert recorder.env["JIRA_USER_EMAIL"] == "bot@example.com"
    assert recorder.env["JIRA_TOKEN"] == "s3cr3t"


def test_post_jira_comment_native_nonzero_exits():
    """A non-zero CLI exit aborts with sys.exit(1)."""
    recorder = _RunRecorder(returncode=1, stderr="boom")
    restore = _with_jira_env_and_recorder(recorder)
    try:
        execute_actions.post_jira_comment_native("TC-1", "body")
        assert False, "Should have exited"
    except SystemExit as e:
        assert e.code == 1
    finally:
        restore()


def test_post_jira_comment_native_invalid_key_exits():
    """A malformed issue key (no hyphen) aborts before invoking the CLI."""
    recorder = _RunRecorder()
    restore = _with_jira_env_and_recorder(recorder)
    try:
        execute_actions.post_jira_comment_native("TC123", "body")
        assert False, "Should have exited"
    except SystemExit as e:
        assert e.code == 1
    finally:
        restore()
    assert recorder.cmd is None, "CLI should not run for an invalid key"


def test_schema_post_comment_accepts_valid_jira_key():
    """The post_comment schema accepts a well-formed hyphenated Jira key so a
    legitimate action still validates and routes to the native CLI."""
    # Given a post_comment action whose issue is a valid Jira key
    action = {"type": "post_comment", "issue": "TC-5811", "body_adf": {}}
    # When validating it against the result schema's action definition
    # Then validation passes (validate raises ValidationError on failure)
    validate(instance=action, schema=_ACTION_SCHEMA)


def test_schema_post_comment_accepts_ref_key_placeholder():
    """The post_comment schema accepts a {{<ref>.key}} placeholder so a comment
    targeting an issue created by an earlier action (which execute_post_comment
    resolves via resolve_refs) survives fullsend's validation_loop instead of
    being rejected before the reference can be resolved."""
    # Given a post_comment action whose issue is a {{<ref>.key}} placeholder
    action = {"type": "post_comment", "issue": "{{sub-1.key}}", "body_adf": {}}
    # When validating it against the result schema's action definition
    # Then validation passes (validate raises ValidationError on failure)
    validate(instance=action, schema=_ACTION_SCHEMA)


def test_schema_post_comment_rejects_non_key_issue():
    """A schema-valid-string-but-non-key issue (numeric ID, URL, lowercase,
    missing hyphen, or a non-.key placeholder) is rejected at validation, so it
    can never pass the producer boundary only to hit the executor's rpartition
    guard and sys.exit(1)."""
    # Given post_comment actions whose issue is neither a hyphenated Jira key
    # nor a {{<ref>.key}} placeholder
    non_keys = [
        "12345",                                        # numeric Jira ID
        "https://jira.example.com/browse/TC-5811",      # URL
        "tc-5811",                                      # lowercase project
        "TC5811",                                       # missing hyphen
        "TC-",                                          # missing number
        "-5811",                                        # missing project
        "{{sub-1.url}}",                                # .url placeholder (not a key)
        "{{SUB.key}}",                                  # uppercase ref name
        "{{sub-1.status}}",                             # unsupported placeholder attr
        "sub-1.key",                                    # missing braces
        "prefix {{sub-1.key}}",                         # placeholder not anchored
    ]
    for issue in non_keys:
        action = {"type": "post_comment", "issue": issue, "body_adf": {}}
        # When validating each against the schema
        # Then validation fails before the action can reach the executor
        try:
            validate(instance=action, schema=_ACTION_SCHEMA)
            assert False, f"non-key issue should be rejected: {issue!r}"
        except ValidationError:
            pass


def test_adf_to_markdown_renders_blocks_and_marks():
    """adf_to_markdown renders headings, lists, code blocks, rules, and inline marks."""
    doc = {
        "type": "doc",
        "version": 1,
        "content": [
            {"type": "heading", "attrs": {"level": 2},
             "content": [{"type": "text", "text": "Title"}]},
            {"type": "paragraph", "content": [
                {"type": "text", "text": "See "},
                {"type": "text", "text": "TC-1", "marks": [{"type": "strong"}]},
                {"type": "text", "text": " and "},
                {"type": "text", "text": "run", "marks": [{"type": "code"}]},
                {"type": "text", "text": " at "},
                {"type": "text", "text": "here",
                 "marks": [{"type": "link", "attrs": {"href": "https://x.example/y"}}]},
            ]},
            {"type": "bulletList", "content": [
                {"type": "listItem", "content": [
                    {"type": "paragraph", "content": [{"type": "text", "text": "first"}]}]},
                {"type": "listItem", "content": [
                    {"type": "paragraph", "content": [{"type": "text", "text": "second"}]}]},
            ]},
            {"type": "rule"},
            {"type": "codeBlock", "attrs": {"language": "python"},
             "content": [{"type": "text", "text": "x = 1"}]},
        ],
    }
    result = execute_actions.adf_to_markdown(doc)
    expected = (
        "## Title\n\n"
        "See **TC-1** and `run` at [here](https://x.example/y)\n\n"
        "- first\n- second\n\n"
        "---\n\n"
        "```python\nx = 1\n```"
    )
    assert result == expected, f"Got: {result!r}"


def test_adf_to_markdown_renders_task_list():
    """adf_to_markdown renders taskList DONE/TODO items as - [x] / - [ ] markers, for both paragraph-wrapped and inline taskItem content."""
    doc = {
        "type": "doc",
        "version": 1,
        "content": [
            {"type": "taskList", "content": [
                {"type": "taskItem", "attrs": {"state": "DONE"}, "content": [
                    {"type": "paragraph", "content": [{"type": "text", "text": "done item"}]}]},
                {"type": "taskItem", "attrs": {"state": "TODO"}, "content": [
                    {"type": "text", "text": "todo item"}]},
            ]},
        ],
    }
    result = execute_actions.adf_to_markdown(doc)
    assert result == "- [x] done item\n- [ ] todo item", f"Got: {result!r}"


def test_adf_to_markdown_escapes_markdown_active_chars_in_literal_text():
    """Literal markdown-active characters in a plain text node are backslash-escaped
    so the native CLI renders them verbatim instead of reinterpreting them as
    formatting."""
    # Given a paragraph whose literal text contains * _ [ ] and a backtick
    doc = {
        "type": "doc",
        "version": 1,
        "content": [
            {"type": "paragraph", "content": [
                {"type": "text", "text": "a*b_c[d]e`f"},
            ]},
        ],
    }
    # When rendering the ADF to markdown
    result = execute_actions.adf_to_markdown(doc)
    # Then each active character is escaped with a leading backslash
    assert result == "a\\*b\\_c\\[d\\]e\\`f", f"Got: {result!r}"


def test_adf_to_markdown_does_not_double_escape_marks_or_code():
    """Intentional marks (strong/link) and inline code render correctly: the mark
    syntax the renderer adds is not escaped, inline-code content stays literal, and
    link hrefs are not escaped."""
    # Given marked text, an inline-code span containing an asterisk, and a link
    # whose href contains an underscore
    doc = {
        "type": "doc",
        "version": 1,
        "content": [
            {"type": "paragraph", "content": [
                {"type": "text", "text": "bold", "marks": [{"type": "strong"}]},
                {"type": "text", "text": " and "},
                {"type": "text", "text": "a*b", "marks": [{"type": "code"}]},
                {"type": "text", "text": " see "},
                {"type": "text", "text": "here",
                 "marks": [{"type": "link", "attrs": {"href": "https://x.example/a_b"}}]},
            ]},
        ],
    }
    # When rendering the ADF to markdown
    result = execute_actions.adf_to_markdown(doc)
    # Then the ** stays, the code asterisk stays literal, and the href underscore
    # is preserved (none are escaped)
    assert result == "**bold** and `a*b` see [here](https://x.example/a_b)", f"Got: {result!r}"


def test_adf_to_markdown_escapes_line_leading_block_markers():
    """A paragraph whose literal text begins with a Markdown block marker
    (heading/bullet/blockquote/ordered-list) has that marker backslash-escaped so
    the native CLI renders it verbatim instead of re-parsing it as a block."""
    # Given paragraphs each starting with a different line-leading block marker
    doc = {
        "type": "doc",
        "version": 1,
        "content": [
            {"type": "paragraph", "content": [{"type": "text", "text": "# not a heading"}]},
            {"type": "paragraph", "content": [{"type": "text", "text": "### also not"}]},
            {"type": "paragraph", "content": [{"type": "text", "text": "- not a bullet"}]},
            {"type": "paragraph", "content": [{"type": "text", "text": "+ not a bullet"}]},
            {"type": "paragraph", "content": [{"type": "text", "text": "> not a quote"}]},
            {"type": "paragraph", "content": [{"type": "text", "text": "1. not ordered"}]},
            {"type": "paragraph", "content": [{"type": "text", "text": "2) not ordered"}]},
        ],
    }
    # When rendering the ADF to markdown
    result = execute_actions.adf_to_markdown(doc)
    # Then the leading marker of each line is escaped (heading/bullet/quote escape
    # the first char; ordered lists escape the . / ) separator)
    assert result == (
        "\\# not a heading\n\n"
        "\\### also not\n\n"
        "\\- not a bullet\n\n"
        "\\+ not a bullet\n\n"
        "\\> not a quote\n\n"
        "1\\. not ordered\n\n"
        "2\\) not ordered"
    ), f"Got: {result!r}"


def test_adf_to_markdown_escapes_line_leading_marker_after_hardbreak():
    """A block marker that starts a line *after* a hardBreak inside a paragraph is
    escaped too, since it is at a real line start once rendered."""
    # Given a paragraph with a hardBreak followed by text starting with "# "
    doc = {
        "type": "doc",
        "version": 1,
        "content": [
            {"type": "paragraph", "content": [
                {"type": "text", "text": "see:"},
                {"type": "hardBreak"},
                {"type": "text", "text": "# heading"},
            ]},
        ],
    }
    # When rendering the ADF to markdown
    result = execute_actions.adf_to_markdown(doc)
    # Then only the post-hardBreak line-leading marker is escaped
    assert result == "see:\n\\# heading", f"Got: {result!r}"


def test_adf_to_markdown_does_not_escape_midline_or_non_marker_text():
    """Escaping is line-position-sensitive: a marker char mid-line, or a
    marker-like prefix that does not actually form a block (no trailing space, a
    heading start intentionally emitted by the heading renderer), is left alone."""
    # Given a heading node, a paragraph with a mid-line '#', and paragraphs whose
    # leading chars do not form a block construct ("-5", "1.5" have no space)
    doc = {
        "type": "doc",
        "version": 1,
        "content": [
            {"type": "heading", "attrs": {"level": 2},
             "content": [{"type": "text", "text": "Real Heading"}]},
            {"type": "paragraph", "content": [{"type": "text", "text": "not # a heading"}]},
            {"type": "paragraph", "content": [{"type": "text", "text": "-5 degrees"}]},
            {"type": "paragraph", "content": [{"type": "text", "text": "1.5 times"}]},
        ],
    }
    # When rendering the ADF to markdown
    result = execute_actions.adf_to_markdown(doc)
    # Then the real heading keeps its intentional prefix and nothing else is escaped
    assert result == (
        "## Real Heading\n\n"
        "not # a heading\n\n"
        "-5 degrees\n\n"
        "1.5 times"
    ), f"Got: {result!r}"


def test_adf_to_markdown_renders_non_text_inline_nodes():
    """Each non-text inline leaf node (mention/emoji/inlineCard/date/status)
    renders its attrs-sourced displayable value instead of being dropped to an
    empty string."""
    # Given a paragraph containing one of each non-text inline leaf type, with
    # an underscore in the inlineCard URL (URLs must not be escaped) and an
    # epoch-millisecond date timestamp for 2021-01-01 UTC
    doc = {
        "type": "doc",
        "version": 1,
        "content": [
            {"type": "paragraph", "content": [
                {"type": "mention", "attrs": {"id": "abc", "text": "@Marco Rizzi"}},
                {"type": "text", "text": " "},
                {"type": "emoji", "attrs": {"shortName": ":smile:", "text": "😄"}},
                {"type": "text", "text": " "},
                {"type": "inlineCard", "attrs": {"url": "https://example.com/a_b"}},
                {"type": "text", "text": " "},
                {"type": "date", "attrs": {"timestamp": "1609459200000"}},
                {"type": "text", "text": " "},
                {"type": "status", "attrs": {"text": "In Progress", "color": "yellow"}},
            ]},
        ],
    }
    # When rendering the ADF to markdown
    result = execute_actions.adf_to_markdown(doc)
    # Then every node contributes its attrs value (URL underscore preserved, date
    # formatted as YYYY-MM-DD) and nothing is silently dropped
    assert result == "@Marco Rizzi 😄 https://example.com/a_b 2021-01-01 In Progress", \
        f"Got: {result!r}"


def test_adf_to_markdown_renders_inline_nodes_in_task_item():
    """A taskItem whose inline content mixes text with a mention and an
    inlineCard renders all of them — the inline nodes are not dropped in the
    taskItem context."""
    # Given a TODO taskItem with inline mention and inlineCard nodes
    doc = {
        "type": "doc",
        "version": 1,
        "content": [
            {"type": "taskList", "content": [
                {"type": "taskItem", "attrs": {"state": "TODO"}, "content": [
                    {"type": "text", "text": "ping "},
                    {"type": "mention", "attrs": {"text": "@dev"}},
                    {"type": "text", "text": " re "},
                    {"type": "inlineCard", "attrs": {"url": "https://example.com/pr/1"}},
                ]},
            ]},
        ],
    }
    # When rendering the ADF to markdown
    result = execute_actions.adf_to_markdown(doc)
    # Then the checklist item retains the mention and inlineCard values
    assert result == "- [ ] ping @dev re https://example.com/pr/1", f"Got: {result!r}"


def test_adf_to_markdown_renders_table():
    """A table renders as a GFM table: first tableRow is the header (with a ---
    separator), tableCell/tableHeader content is rendered, and literal pipes in a
    cell are escaped so they do not break the column grid."""
    doc = {
        "type": "doc",
        "version": 1,
        "content": [
            {"type": "table", "content": [
                {"type": "tableRow", "content": [
                    {"type": "tableHeader", "content": [
                        {"type": "paragraph", "content": [{"type": "text", "text": "Name"}]}]},
                    {"type": "tableHeader", "content": [
                        {"type": "paragraph", "content": [{"type": "text", "text": "Note"}]}]},
                ]},
                {"type": "tableRow", "content": [
                    {"type": "tableCell", "content": [
                        {"type": "paragraph", "content": [{"type": "text", "text": "a"}]}]},
                    {"type": "tableCell", "content": [
                        {"type": "paragraph", "content": [{"type": "text", "text": "b|c"}]}]},
                ]},
            ]},
        ],
    }
    result = execute_actions.adf_to_markdown(doc)
    assert result == (
        "| Name | Note |\n"
        "| --- | --- |\n"
        "| a | b\\|c |"
    ), f"Got: {result!r}"


def test_adf_to_markdown_renders_blockquote_and_panel():
    """blockquote renders as > -prefixed lines; a panel renders as a quote with a
    bold panelType label so its kind is preserved."""
    doc = {
        "type": "doc",
        "version": 1,
        "content": [
            {"type": "blockquote", "content": [
                {"type": "paragraph", "content": [{"type": "text", "text": "quoted"}]}]},
            {"type": "panel", "attrs": {"panelType": "info"}, "content": [
                {"type": "paragraph", "content": [{"type": "text", "text": "heads up"}]}]},
        ],
    }
    result = execute_actions.adf_to_markdown(doc)
    assert result == (
        "> quoted\n"
        "\n"
        "> **info**\n"
        ">\n"
        "> heads up"
    ), f"Got: {result!r}"


def test_adf_to_markdown_renders_media_instead_of_dropping():
    """media/mediaSingle render a non-empty image link (or [alt] placeholder when
    no URL is present) rather than being silently dropped — media nodes have no
    text content, so the pre-fix flattening fallback emitted nothing."""
    doc = {
        "type": "doc",
        "version": 1,
        "content": [
            {"type": "mediaSingle", "content": [
                {"type": "media", "attrs": {"url": "https://ex.com/i.png", "alt": "chart"}}]},
            {"type": "mediaSingle", "content": [
                {"type": "media", "attrs": {"type": "file", "id": "abc-123"}}]},
        ],
    }
    result = execute_actions.adf_to_markdown(doc)
    assert result == "![chart](https://ex.com/i.png)\n\n[abc-123]", f"Got: {result!r}"


def test_adf_to_markdown_unknown_block_still_flattens():
    """A genuinely unknown container block still degrades gracefully by recursing
    into its nested content (the preserved fallback), so the fix does not regress
    forward-compat handling of block nodes it does not explicitly cover."""
    doc = {
        "type": "doc",
        "version": 1,
        "content": [
            {"type": "someFutureBlock", "content": [
                {"type": "paragraph", "content": [{"type": "text", "text": "still here"}]}]},
        ],
    }
    result = execute_actions.adf_to_markdown(doc)
    assert result == "still here", f"Got: {result!r}"


def test_render_adf_date_falls_back_on_out_of_range_timestamp():
    """An integer-parseable but out-of-range epoch-ms timestamp renders as its
    literal string instead of raising, so a single malformed date node cannot
    abort the whole post_script. datetime.fromtimestamp raises OverflowError/OSError
    (or ValueError) for out-of-range values, and that call now sits inside the
    guarded try; before the fix it was outside and any such exception propagated."""
    # Given an integer-parseable epoch-millisecond value far outside the
    # representable datetime range
    out_of_range = "99999999999999999"
    # When rendering it as an ADF date node
    result = execute_actions._render_adf_date(out_of_range)
    # Then the literal value is returned and no exception propagates
    assert result == out_of_range, f"Got: {result!r}"


def test_execute_post_comment_routes_to_native():
    """execute_post_comment resolves refs in body_adf, renders to markdown, and posts it."""
    recorder = _RunRecorder()
    restore = _with_jira_env_and_recorder(recorder)
    registry = {"sub-1": {"key": "TC-500", "url": "https://jira.example.com/browse/TC-500"}}
    body_adf = {
        "type": "doc",
        "version": 1,
        "content": [
            {"type": "paragraph", "content": [
                {"type": "text", "text": "See "},
                {"type": "text", "text": "{{sub-1.key}}", "marks": [{"type": "strong"}]},
                {"type": "text", "text": " at "},
                {"type": "text", "text": "link",
                 "marks": [{"type": "link", "attrs": {"href": "{{sub-1.url}}"}}]},
            ]},
        ],
    }
    try:
        execute_actions.execute_post_comment(
            {"type": "post_comment", "issue": "{{sub-1.key}}", "body_adf": body_adf},
            registry,
        )
    finally:
        restore()

    assert recorder.cmd[recorder.cmd.index("--number") + 1] == "500"
    assert recorder.input == "See **TC-500** at [link](https://jira.example.com/browse/TC-500)", \
        f"Got: {recorder.input!r}"


def test_post_comment_and_report_use_distinct_sticky_markers():
    """A post_comment and a post_report pass DIFFERENT --marker values to the
    native CLI, so two sticky comments on the same Jira issue never share one
    marker identity and clobber each other."""
    # Given the comment path
    comment_recorder = _RunRecorder()
    restore = _with_jira_env_and_recorder(comment_recorder)
    try:
        execute_actions.execute_post_comment(
            {"type": "post_comment", "issue": "TC-777",
             "body_adf": {"type": "doc", "version": 1, "content": []}},
            {},
        )
    finally:
        restore()
    comment_marker = comment_recorder.cmd[comment_recorder.cmd.index("--marker") + 1]

    # And the report path (no existing GitHub comment → lists then posts)
    report_calls = []

    def fake_run(cmd, input=None, text=None, capture_output=None, env=None):
        report_calls.append(cmd)
        return _FakeCompleted(0, "", "[]")

    saved_run = execute_actions.subprocess.run
    saved_env = {k: os.environ.get(k) for k in _JIRA_ENV}
    execute_actions.subprocess.run = fake_run
    os.environ.update(_JIRA_ENV)
    try:
        report = {
            "pr_repo": "acme/widget",
            "pr_number": 42,
            "jira_issue_id": "TC-777",
            "commit_sha": "946556e",
            "report_md": "## Verify report",
        }
        execute_actions.execute_post_report({"type": "post_report"}, {}, report)
    finally:
        execute_actions.subprocess.run = saved_run
        for k, v in saved_env.items():
            if v is None:
                os.environ.pop(k, None)
            else:
                os.environ[k] = v
    jira_cmd = next(c for c in report_calls if c[:3] == ["fullsend", "issues", "post-comment"])
    report_marker = jira_cmd[jira_cmd.index("--marker") + 1]

    # Then the two markers differ, and each matches its dedicated constant
    assert comment_marker == execute_actions.POST_COMMENT_STICKY_MARKER
    assert report_marker == execute_actions.STICKY_COMMENT_MARKER
    assert comment_marker != report_marker, "post_comment and post_report must use distinct markers"


def test_execute_post_report_posts_github_then_jira():
    """execute_post_report lists PR comments, creates a marked GitHub comment when none exists, then posts to Jira."""
    calls = []

    def fake_run(cmd, input=None, text=None, capture_output=None, env=None):
        calls.append({"cmd": cmd, "input": input, "env": env})
        # No existing report comment on the PR yet.
        return _FakeCompleted(0, "", "[]")

    saved_run = execute_actions.subprocess.run
    saved_env = {k: os.environ.get(k) for k in _JIRA_ENV}
    execute_actions.subprocess.run = fake_run
    os.environ.update(_JIRA_ENV)
    try:
        report = {
            "pr_repo": "acme/widget",
            "pr_number": 42,
            "jira_issue_id": "TC-777",
            "commit_sha": "946556e",
            "report_md": "## Verify report\nAll good.",
        }
        execute_actions.execute_post_report({"type": "post_report"}, {}, report)
    finally:
        execute_actions.subprocess.run = saved_run
        for k, v in saved_env.items():
            if v is None:
                os.environ.pop(k, None)
            else:
                os.environ[k] = v

    assert len(calls) == 3, f"Expected list + create + native calls, got {len(calls)}"
    list_call, gh_call, jira_call = calls
    # Existing comments are listed first to check for a prior report.
    assert list_call["cmd"][:2] == ["gh", "api"]
    assert list_call["cmd"][2] == "repos/acme/widget/issues/42/comments"
    # No existing comment → a new PR comment is created, carrying the commit marker.
    assert gh_call["cmd"][:3] == ["gh", "pr", "comment"]
    assert "acme/widget" in gh_call["cmd"]
    gh_body = gh_call["cmd"][gh_call["cmd"].index("--body") + 1]
    assert gh_body.startswith("## Verify report\nAll good.")
    assert "<!-- sdlc-workflow:verify-pr report commit:946556e -->" in gh_body
    # Jira side is unchanged: sticky CLI, clean body without the GitHub marker.
    assert jira_call["cmd"][:3] == ["fullsend", "issues", "post-comment"]
    assert jira_call["cmd"][jira_call["cmd"].index("--number") + 1] == "777"
    assert jira_call["input"] == "## Verify report\nAll good."


def test_execute_post_report_updates_existing_github_comment_on_retry():
    """A retry for the same commit PATCH-updates the existing GitHub report comment instead of creating a duplicate."""
    # Given a prior report comment for this commit already exists on the PR.
    # `gh api --paginate --slurp` wraps each page's comment array in one outer
    # array, so the listing is a single-page array-of-pages here.
    calls = []
    existing_page = [{"id": 555,
                      "body": "old report\n\n<!-- sdlc-workflow:verify-pr report commit:946556e -->"}]

    def fake_run(cmd, input=None, text=None, capture_output=None, env=None):
        calls.append({"cmd": cmd, "input": input, "env": env})
        if cmd[:2] == ["gh", "api"] and cmd[2].endswith("/comments"):
            return _FakeCompleted(0, "", json.dumps([existing_page]))
        return _FakeCompleted(0, "")

    saved_run = execute_actions.subprocess.run
    saved_env = {k: os.environ.get(k) for k in _JIRA_ENV}
    execute_actions.subprocess.run = fake_run
    os.environ.update(_JIRA_ENV)
    try:
        report = {
            "pr_repo": "acme/widget",
            "pr_number": 42,
            "jira_issue_id": "TC-777",
            "commit_sha": "946556e",
            "report_md": "## Verify report\nAll good.",
        }
        # When posting the report again (e.g. after a prior Jira failure)
        execute_actions.execute_post_report({"type": "post_report"}, {}, report)
    finally:
        execute_actions.subprocess.run = saved_run
        for k, v in saved_env.items():
            if v is None:
                os.environ.pop(k, None)
            else:
                os.environ[k] = v

    # Then no new GitHub comment is created; the existing one is PATCH-updated
    assert not any(c["cmd"][:3] == ["gh", "pr", "comment"] for c in calls), \
        "retry must not create a new GitHub comment"
    patch_calls = [c for c in calls if "PATCH" in c["cmd"]]
    assert len(patch_calls) == 1, f"Expected one PATCH update, got {len(patch_calls)}"
    assert patch_calls[0]["cmd"][2] == "repos/acme/widget/issues/comments/555"
    # And the Jira report is still posted
    assert any(c["cmd"][:3] == ["fullsend", "issues", "post-comment"] for c in calls), \
        "Jira report must still be posted on retry"


def test_execute_post_report_updates_comment_on_later_page():
    """When the listing spans multiple pages, an existing report comment on a
    non-first page is still found and PATCH-updated (no duplicate created)."""
    # Given a slurped, multi-page listing (array-of-pages) where the marked report
    # comment lives on the SECOND page — the exact case a single json.loads on
    # concatenated per-page arrays could not parse.
    calls = []
    page_one = [
        {"id": 101, "body": "just a normal review comment"},
        {"id": 102, "body": "another unrelated comment"},
    ]
    page_two = [
        {"id": 103, "body": "chatter"},
        {"id": 555,
         "body": "old report\n\n<!-- sdlc-workflow:verify-pr report commit:946556e -->"},
    ]

    def fake_run(cmd, input=None, text=None, capture_output=None, env=None):
        calls.append({"cmd": cmd, "input": input, "env": env})
        if cmd[:2] == ["gh", "api"] and cmd[2].endswith("/comments"):
            # --paginate --slurp wraps each page's array in one outer array.
            return _FakeCompleted(0, "", json.dumps([page_one, page_two]))
        return _FakeCompleted(0, "")

    saved_run = execute_actions.subprocess.run
    saved_env = {k: os.environ.get(k) for k in _JIRA_ENV}
    execute_actions.subprocess.run = fake_run
    os.environ.update(_JIRA_ENV)
    try:
        report = {
            "pr_repo": "acme/widget",
            "pr_number": 42,
            "jira_issue_id": "TC-777",
            "commit_sha": "946556e",
            "report_md": "## Verify report\nAll good.",
        }
        # When posting the report again for the same commit
        execute_actions.execute_post_report({"type": "post_report"}, {}, report)
    finally:
        execute_actions.subprocess.run = saved_run
        for k, v in saved_env.items():
            if v is None:
                os.environ.pop(k, None)
            else:
                os.environ[k] = v

    # Then the comment on the second page is PATCH-updated, not duplicated.
    assert not any(c["cmd"][:3] == ["gh", "pr", "comment"] for c in calls), \
        "must not create a new GitHub comment when the report exists on a later page"
    patch_calls = [c for c in calls if "PATCH" in c["cmd"]]
    assert len(patch_calls) == 1, f"Expected one PATCH update, got {len(patch_calls)}"
    assert patch_calls[0]["cmd"][2] == "repos/acme/widget/issues/comments/555"


def test_execute_post_report_dedup_marker_invariant_to_sha_length():
    """A full-length SHA on one run and an abbreviated SHA for the same commit on
    a retry resolve to the SAME report comment (PATCH-update, not duplicate),
    because the dedup marker normalizes the SHA to a canonical length."""
    full_sha = "946556e" + "a" * 33   # 40 hex chars
    short_sha = "946556e"             # 7-char abbreviation of the same commit

    def _run_report(commit_sha, existing_comments):
        """Run execute_post_report; return (calls, created_body_or_None)."""
        calls = []

        def fake_run(cmd, input=None, text=None, capture_output=None, env=None):
            calls.append({"cmd": cmd, "input": input})
            if cmd[:2] == ["gh", "api"] and cmd[2].endswith("/comments"):
                return _FakeCompleted(0, "", json.dumps([existing_comments]))
            return _FakeCompleted(0, "")

        saved_run = execute_actions.subprocess.run
        saved_env = {k: os.environ.get(k) for k in _JIRA_ENV}
        execute_actions.subprocess.run = fake_run
        os.environ.update(_JIRA_ENV)
        try:
            report = {
                "pr_repo": "acme/widget",
                "pr_number": 42,
                "jira_issue_id": "TC-777",
                "commit_sha": commit_sha,
                "report_md": "## Verify report",
            }
            execute_actions.execute_post_report({"type": "post_report"}, {}, report)
        finally:
            execute_actions.subprocess.run = saved_run
            for k, v in saved_env.items():
                if v is None:
                    os.environ.pop(k, None)
                else:
                    os.environ[k] = v
        return calls

    # First run with the FULL SHA and no existing comment → a comment is created;
    # capture the marker it embedded.
    first_calls = _run_report(full_sha, [])
    create_call = next(c for c in first_calls if c["cmd"][:3] == ["gh", "pr", "comment"])
    created_body = create_call["cmd"][create_call["cmd"].index("--body") + 1]

    # Retry with the ABBREVIATED SHA; the PR already has the comment created above.
    retry_calls = _run_report(short_sha, [{"id": 555, "body": created_body}])

    # Then the retry PATCH-updates the existing comment instead of duplicating it.
    assert not any(c["cmd"][:3] == ["gh", "pr", "comment"] for c in retry_calls), \
        "abbreviated-SHA retry must not create a duplicate report comment"
    patch_calls = [c for c in retry_calls if "PATCH" in c["cmd"]]
    assert len(patch_calls) == 1, f"Expected one PATCH update, got {len(patch_calls)}"
    assert patch_calls[0]["cmd"][2] == "repos/acme/widget/issues/comments/555"


def test_post_report_resolves_ref_created_by_later_action():
    """report_md refs resolve regardless of action ordering: a post_report ordered
    BEFORE the create_subtask it references still resolves, because main() defers
    every post_report until after the actions loop populates the registry."""
    calls = []

    def fake_run(cmd, input=None, text=None, capture_output=None, env=None):
        calls.append({"cmd": cmd, "input": input})
        if cmd[:2] == ["gh", "api"] and cmd[2].endswith("/comments"):
            return _FakeCompleted(0, "", "[]")  # no existing report comment
        return _FakeCompleted(0, "")

    def fake_create_issue(**kwargs):
        return {"key": "TC-999"}

    # Actions deliberately order post_report FIRST, then the create_subtask whose
    # ref its report_md interpolates — the pre-fix inline order would KeyError.
    data = {
        "report": {
            "pr_repo": "acme/widget",
            "pr_number": 42,
            "jira_issue_id": "TC-777",
            "commit_sha": "946556e",
            "report_md": "Filed sub-task {{sub-1.key}}.",
        },
        "actions": [
            {"type": "post_report"},
            {
                "type": "create_subtask",
                "ref": "sub-1",
                "parent": "TC-100",
                "summary": "A sub-task",
                "labels": ["review-feedback"],
                "description_adf": {"type": "doc", "version": 1, "content": []},
            },
        ],
    }

    saved_run = execute_actions.subprocess.run
    saved_create = execute_actions._jira_mod.create_issue
    saved_argv = sys.argv
    saved_env = {k: os.environ.get(k) for k in _JIRA_ENV}
    execute_actions.subprocess.run = fake_run
    execute_actions._jira_mod.create_issue = fake_create_issue
    os.environ.update(_JIRA_ENV)
    fd, path = tempfile.mkstemp(suffix=".json")
    try:
        with os.fdopen(fd, "w") as f:
            json.dump(data, f)
        sys.argv = ["execute-actions.py", path]
        execute_actions.main()
    finally:
        execute_actions.subprocess.run = saved_run
        execute_actions._jira_mod.create_issue = saved_create
        sys.argv = saved_argv
        os.remove(path)
        for k, v in saved_env.items():
            if v is None:
                os.environ.pop(k, None)
            else:
                os.environ[k] = v

    # The GitHub report body carries the resolved key, not the raw placeholder.
    create_call = next(c for c in calls if c["cmd"][:3] == ["gh", "pr", "comment"])
    gh_body = create_call["cmd"][create_call["cmd"].index("--body") + 1]
    assert "Filed sub-task TC-999." in gh_body, f"ref not resolved: {gh_body}"
    assert "{{sub-1.key}}" not in gh_body, "placeholder leaked into report body"


def test_find_report_comment_id_exits_on_unparseable_json():
    """A JSON parse failure aborts with sys.exit(1) instead of silently returning
    None (which would let a retry create a duplicate report comment)."""
    # Given `gh` returns malformed JSON (e.g. concatenated per-page arrays, the
    # pre-fix --paginate-without-slurp shape that is not valid combined JSON)
    def fake_run(cmd, input=None, text=None, capture_output=None, env=None):
        return _FakeCompleted(0, "", "[{\"id\": 1}][{\"id\": 2}]")

    saved_run = execute_actions.subprocess.run
    execute_actions.subprocess.run = fake_run
    try:
        # When the id lookup runs, it must fail loudly rather than swallow the error
        execute_actions._find_report_comment_id("acme/widget", 42, "marker")
        assert False, "Should have exited on unparseable JSON"
    except SystemExit as e:
        assert e.code == 1
    finally:
        execute_actions.subprocess.run = saved_run


if __name__ == "__main__":
    test_resolve_refs_replaces_key()
    test_resolve_refs_no_placeholders()
    test_resolve_refs_unknown_ref_raises()
    test_resolve_refs_in_adf()
    test_resolve_refs_multiple_different_refs()
    test_resolve_refs_repeated_placeholder()
    test_resolve_refs_mixed_key_url_same_ref()
    test_post_jira_comment_native_builds_argv()
    test_post_jira_comment_native_maps_env()
    test_post_jira_comment_native_nonzero_exits()
    test_post_jira_comment_native_invalid_key_exits()
    test_schema_post_comment_accepts_valid_jira_key()
    test_schema_post_comment_accepts_ref_key_placeholder()
    test_schema_post_comment_rejects_non_key_issue()
    test_adf_to_markdown_renders_blocks_and_marks()
    test_adf_to_markdown_renders_task_list()
    test_adf_to_markdown_escapes_markdown_active_chars_in_literal_text()
    test_adf_to_markdown_does_not_double_escape_marks_or_code()
    test_adf_to_markdown_escapes_line_leading_block_markers()
    test_adf_to_markdown_escapes_line_leading_marker_after_hardbreak()
    test_adf_to_markdown_does_not_escape_midline_or_non_marker_text()
    test_adf_to_markdown_renders_non_text_inline_nodes()
    test_adf_to_markdown_renders_inline_nodes_in_task_item()
    test_adf_to_markdown_renders_table()
    test_adf_to_markdown_renders_blockquote_and_panel()
    test_adf_to_markdown_renders_media_instead_of_dropping()
    test_adf_to_markdown_unknown_block_still_flattens()
    test_render_adf_date_falls_back_on_out_of_range_timestamp()
    test_execute_post_comment_routes_to_native()
    test_post_comment_and_report_use_distinct_sticky_markers()
    test_execute_post_report_posts_github_then_jira()
    test_execute_post_report_updates_existing_github_comment_on_retry()
    test_execute_post_report_updates_comment_on_later_page()
    test_execute_post_report_dedup_marker_invariant_to_sha_length()
    test_post_report_resolves_ref_created_by_later_action()
    test_find_report_comment_id_exits_on_unparseable_json()
    print("All tests passed.")
