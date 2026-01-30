"""HOA-Bench: Evaluating LLMs as HOA managers applying CC&R rules."""

import json
import pathlib

import yaml

from inspect_ai import Task, task
from inspect_ai.dataset import Sample
from inspect_ai.scorer import match, model_graded_fact
from inspect_ai.solver import generate, system_message

# Path to this directory
_HERE = pathlib.Path(__file__).parent

# System prompt for HOA manager role
HOA_SYSTEM_PROMPT = """You are an HOA manager for Camino Village HOA. Respond to homeowner requests and violation reports by applying the CC&R rules accurately.

Your available decisions are:
- approve: The request complies with rules
- deny: The request violates rules
- violation: A rule violation has occurred
- refer_to_committee: Requires Architectural Committee review
- needs_more_info: Cannot determine without additional information
- no_violation: Complaint does not constitute a violation

For each request, provide:
1. Your decision (one of the options above)
2. Brief reasoning citing the relevant rule

CC&R Rules:
{rules_text}
"""


def _load_rules_text() -> str:
    """Load all rules from YAML and format for the system prompt."""
    rules_path = _HERE / "configs" / "rules.yaml"
    with open(rules_path) as f:
        rules_data = yaml.safe_load(f)

    lines = []
    for rule in rules_data["rules"]:
        lines.append(f"[{rule['source']}] {rule['id']}: {rule['text']}")
    return "\n\n".join(lines)


def _load_scenarios() -> list[Sample]:
    """Load static scenarios from JSON."""
    scenarios_path = _HERE / "data" / "scenarios" / "static_scenarios.json"
    with open(scenarios_path) as f:
        scenarios = json.load(f)

    return [
        Sample(
            input=s["input"]["message"],
            # Target is grading guidance: decision + reasoning for the grader
            target=f"Decision: {s['ground_truth']['decision']}. {s['ground_truth']['reasoning']}",
            metadata={
                "id": s["id"],
                "category": s["category"],
                "difficulty": s["difficulty"],
            },
        )
        for s in scenarios
    ]


@task
def hoa_static() -> Task:
    """Static scenarios task: single-turn HOA manager responses."""
    rules_text = _load_rules_text()
    system_prompt = HOA_SYSTEM_PROMPT.format(rules_text=rules_text)

    return Task(
        dataset=_load_scenarios(),
        solver=[
            system_message(system_prompt),
            generate(),
        ],
        scorer=model_graded_fact(),
    )


@task
def hoa_simulation() -> Task:
    """Simulation task: multi-turn conversation with homeowner persona.

    TODO: Implement multi-turn conversation where:
    - Homeowner persona tries to achieve their goal
    - HOA manager must maintain correct decision across turns
    """
    return Task(
        dataset=[
            Sample(
                input="Placeholder for simulation task",
                target="placeholder",
            )
        ],
        solver=[generate()],
        scorer=match(),
    )
