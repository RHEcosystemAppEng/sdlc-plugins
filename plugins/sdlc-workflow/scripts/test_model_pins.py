"""Agent model-pin consistency: every production/eval agent pin must agree (TC-7278)."""

import ast
import shutil
from pathlib import Path

import pytest
import yaml

ROOT = Path(__file__).resolve().parents[3]

# Claude Code aliases float to whatever generation the CLI maps them to, so a pin
# must name a concrete model ID (fullsend.md "Managing the agent model").
FLOATING_ALIASES = {"opus", "sonnet", "haiku", "inherit", "default", "opusplan"}

# Every file that selects the agent model and/or effort, relative to the repo root.
PIN_FILES = [
    "harness/verify-pr.yaml",
    "harness/triage-security.yaml",
    "plugins/sdlc-workflow/agents/verify-pr.md",
    "plugins/sdlc-workflow/agents/triage-security.md",
    "evals/fullsend/run.py",
    "evals/fullsend/triage-security/harness.yaml",
    "evals/fullsend/triage-security/eval.yaml",
    ".fullsend/harness/verify-pr.yaml",
    ".fullsend/harness/triage-security.yaml",
]


def frontmatter(path):
    """Parse the YAML frontmatter of an agent definition, failing on a missing block."""
    text = path.read_text()
    if not text.startswith("---\n"):
        raise ValueError(f"{path}: no frontmatter")
    return yaml.safe_load(text.split("---\n", 2)[1])


def argparse_defaults(path):
    """Return the literal `default=` of each `add_argument` flag in a script, without importing it."""
    defaults = {}
    for node in ast.walk(ast.parse(path.read_text())):
        if (isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute)
                and node.func.attr == "add_argument" and node.args
                and isinstance(node.args[0], ast.Constant)):
            for keyword in node.keywords:
                if keyword.arg == "default" and isinstance(keyword.value, ast.Constant):
                    defaults[node.args[0].value] = keyword.value.value
    return defaults


def collect_pins(root):
    """Map every agent pin location to its (model, effort) value; effort is None where not settable."""
    def harness(rel):
        data = yaml.safe_load((root / rel).read_text())
        return data.get("model"), data.get("effort")

    run_defaults = argparse_defaults(root / "evals/fullsend/run.py")
    suite = yaml.safe_load((root / "evals/fullsend/triage-security/eval.yaml").read_text())
    return {
        "harness/verify-pr.yaml": harness("harness/verify-pr.yaml"),
        "harness/triage-security.yaml": harness("harness/triage-security.yaml"),
        "agents/verify-pr.md frontmatter": (
            frontmatter(root / "plugins/sdlc-workflow/agents/verify-pr.md").get("model"), None),
        "agents/triage-security.md frontmatter": (
            frontmatter(root / "plugins/sdlc-workflow/agents/triage-security.md").get("model"), None),
        "run.py defaults": (run_defaults.get("--model"), run_defaults.get("--effort")),
        "eval harness.yaml": harness("evals/fullsend/triage-security/harness.yaml"),
        "eval.yaml models.skill/runner.effort": (
            (suite.get("models") or {}).get("skill"), (suite.get("runner") or {}).get("effort")),
    }


def pin_problems(root):
    """List every disagreement, missing pin, alias pin or composing-child override; empty means consistent."""
    pins = collect_pins(root)
    problems = []
    for location, (model, _effort) in pins.items():
        if not model:
            problems.append(f"{location}: no model pin")
        elif model in FLOATING_ALIASES:
            problems.append(f"{location}: floating alias {model!r}, pin a concrete model ID")
    models = {location: model for location, (model, _) in pins.items()}
    efforts = {location: effort for location, (_, effort) in pins.items()
               if not location.endswith("frontmatter")}
    problems.extend(f"{location}: no effort pin" for location, effort in efforts.items() if effort is None)
    for kind, values in (("model", models), ("effort", efforts)):
        if len(set(values.values())) > 1:
            problems.append(f"{kind} pins disagree: {values}")
    # The .fullsend/ composing children must inherit model/effort from the pinned
    # base; an override there would silently diverge CI from the base harness.
    for rel in (".fullsend/harness/verify-pr.yaml", ".fullsend/harness/triage-security.yaml"):
        child = yaml.safe_load((root / rel).read_text())
        problems.extend(f"{rel}: overrides {key!r}" for key in ("model", "effort") if key in child)
    return problems


def repo_copy(tmp_path):
    """Copy only the pin files into a scratch tree so a test can mutate one safely."""
    for rel in PIN_FILES:
        (tmp_path / rel).parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(ROOT / rel, tmp_path / rel)
    return tmp_path


def test_repository_model_pins_agree():
    """Every production and eval agent pin in the repository names the same model and effort."""
    assert pin_problems(ROOT) == []


def test_repository_pins_select_target_model_and_effort():
    """The agreed pin is the TC-7274 target: claude-opus-5-5 at explicit medium effort."""
    pins = collect_pins(ROOT)
    assert {model for model, _ in pins.values()} == {"claude-opus-5-5"}
    assert {effort for _, effort in pins.values() if effort is not None} == {"medium"}


@pytest.mark.parametrize("rel, old, new", [
    ("harness/verify-pr.yaml", "model: claude-opus-5-5", "model: claude-opus-4-8"),
    ("harness/verify-pr.yaml", "effort: medium", "effort: high"),
    ("harness/triage-security.yaml", "model: claude-opus-5-5", "model: claude-opus-4-8"),
    ("harness/triage-security.yaml", "effort: medium", "effort: high"),
    ("plugins/sdlc-workflow/agents/verify-pr.md", "model: claude-opus-5-5", "model: claude-opus-4-8"),
    ("plugins/sdlc-workflow/agents/triage-security.md", "model: claude-opus-5-5", "model: claude-opus-4-8"),
    ("evals/fullsend/run.py", 'default="claude-opus-5-5"', 'default="claude-opus-4-8"'),
    ("evals/fullsend/run.py", 'default="medium"', 'default="high"'),
    ("evals/fullsend/triage-security/harness.yaml", "model: claude-opus-5-5", "model: claude-opus-4-8"),
    ("evals/fullsend/triage-security/harness.yaml", "effort: medium", "effort: high"),
    ("evals/fullsend/triage-security/eval.yaml", "skill: claude-opus-5-5", "skill: claude-opus-4-8"),
    ("evals/fullsend/triage-security/eval.yaml", "effort: medium", "effort: high"),
])
def test_single_drifted_pin_fails(tmp_path, rel, old, new):
    """Changing any one pin away from the others is reported as a disagreement."""
    # Given a copy of the pin files where exactly one pin drifts
    root = repo_copy(tmp_path)
    text = (root / rel).read_text()
    assert text.count(old) == 1
    (root / rel).write_text(text.replace(old, new))
    # When the pins are checked
    problems = pin_problems(root)
    # Then the drift is reported as a disagreement for the changed dimension
    kind = "effort" if "medium" in old else "model"
    assert any(p.startswith(f"{kind} pins disagree") for p in problems), problems


@pytest.mark.parametrize("rel", [
    "plugins/sdlc-workflow/agents/verify-pr.md",
    "plugins/sdlc-workflow/agents/triage-security.md",
])
def test_frontmatter_alias_fails(tmp_path, rel):
    """An agent frontmatter reverting to the floating `opus` alias is rejected."""
    # Given an agent definition pinned to the alias instead of a model ID
    root = repo_copy(tmp_path)
    (root / rel).write_text((root / rel).read_text().replace("model: claude-opus-5-5", "model: opus"))
    # When the pins are checked
    problems = pin_problems(root)
    # Then both the alias and the resulting disagreement are reported
    assert any("floating alias 'opus'" in p for p in problems), problems
    assert any(p.startswith("model pins disagree") for p in problems), problems


@pytest.mark.parametrize("rel", [".fullsend/harness/verify-pr.yaml", ".fullsend/harness/triage-security.yaml"])
def test_composing_child_override_fails(tmp_path, rel):
    """A .fullsend/ composing child that overrides the base model is rejected."""
    # Given a composing child that sets its own model
    root = repo_copy(tmp_path)
    (root / rel).write_text((root / rel).read_text() + "model: claude-opus-5-5\n")
    # When the pins are checked
    problems = pin_problems(root)
    # Then the override is reported even though its value matches
    assert problems == [f"{rel}: overrides 'model'"]


def test_missing_run_py_default_fails(tmp_path):
    """A run.py --model flag without a literal default fails closed instead of passing."""
    # Given run.py whose --model default is removed
    root = repo_copy(tmp_path)
    path = root / "evals/fullsend/run.py"
    path.write_text(path.read_text().replace('"--model", default="claude-opus-5-5"', '"--model"'))
    # When the pins are checked
    problems = pin_problems(root)
    # Then the missing pin is reported
    assert "run.py defaults: no model pin" in problems
