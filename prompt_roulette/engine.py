"""
Prompt generation engine.

Assembles random prompts from templates and word banks, with support
for complexity filtering, rerolling individual slots, and history.
"""

import random
from .banks import SLOTS, TEMPLATES


def generate_prompt(complexity=None, seed=None):
    """
    Generate a random prompt from a template and slot fills.

    Returns a dict with:
      - "text": the final prompt string
      - "template": the template dict used
      - "fills": dict of {slot_name: chosen_phrase}
    """
    if seed is not None:
        random.seed(seed)

    # Filter templates by complexity if requested
    pool = TEMPLATES
    if complexity is not None:
        pool = [t for t in TEMPLATES if t["complexity"] == complexity]
        if not pool:
            pool = TEMPLATES

    template = random.choice(pool)
    fills = {}
    for slot in template["slots"]:
        fills[slot] = random.choice(SLOTS[slot])

    text = template["template"].format(**fills)
    return {"text": text, "template": template, "fills": fills}


def reroll_slot(prompt_result, slot_name):
    """
    Re-randomize a single slot in an existing prompt result.

    Returns a new prompt result with only that slot changed.
    """
    if slot_name not in prompt_result["fills"]:
        return prompt_result

    template = prompt_result["template"]
    fills = dict(prompt_result["fills"])

    # Pick a new value, avoiding the current one if possible
    current = fills[slot_name]
    options = [v for v in SLOTS[slot_name] if v != current]
    if not options:
        options = SLOTS[slot_name]
    fills[slot_name] = random.choice(options)

    text = template["template"].format(**fills)
    return {"text": text, "template": template, "fills": fills}


def generate_batch(count=5, complexity=None):
    """Generate multiple unique prompts at once."""
    results = []
    seen = set()
    attempts = 0
    while len(results) < count and attempts < count * 10:
        p = generate_prompt(complexity=complexity)
        if p["text"] not in seen:
            seen.add(p["text"])
            results.append(p)
        attempts += 1
    return results


def get_slot_categories():
    """Return info about available slot categories."""
    return {name: len(phrases) for name, phrases in SLOTS.items()}


def get_complexity_levels():
    """Return available complexity levels with descriptions."""
    return {
        1: {"name": "Simple", "desc": "2 slots — quick and fun", "slots": "2"},
        2: {"name": "Medium", "desc": "3 slots — a bit wilder", "slots": "3"},
        3: {"name": "Complex", "desc": "4 slots — getting absurd", "slots": "4"},
        4: {"name": "Chaos", "desc": "5 slots — maximum nonsense", "slots": "5"},
    }
