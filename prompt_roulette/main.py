#!/usr/bin/env python3
"""
Prompt Roulette
===============
Spin the wheel and get a wild, absurd, or surprisingly deep AI prompt.
Mad libs meets AI prompt engineering.

Run:  python -m prompt_roulette
"""

import sys
import os

from .engine import (
    generate_prompt,
    generate_batch,
    reroll_slot,
    get_slot_categories,
    get_complexity_levels,
)
from .banks import SLOTS, TEMPLATES

# -- ANSI colors -------------------------------------------------------------

USE_COLOR = hasattr(sys.stdout, "isatty") and sys.stdout.isatty()
if os.environ.get("NO_COLOR"):
    USE_COLOR = False


def _c(code, text):
    return f"\033[{code}m{text}\033[0m" if USE_COLOR else text


def bold(t):     return _c("1", t)
def red(t):      return _c("91", t)
def green(t):    return _c("92", t)
def yellow(t):   return _c("93", t)
def cyan(t):     return _c("96", t)
def dim(t):      return _c("90", t)
def magenta(t):  return _c("95", t)


# -- Display helpers ----------------------------------------------------------

BANNER = r"""
  ____                            _     ____             _      _   _
 |  _ \ _ __ ___  _ __ ___  _ __ | |_  |  _ \ ___  _   _| | ___| |_| |_ ___
 | |_) | '__/ _ \| '_ ` _ \| '_ \| __| | |_) / _ \| | | | |/ _ \ __| __/ _ \
 |  __/| | | (_) | | | | | | |_) | |_  |  _ < (_) | |_| | |  __/ |_| ||  __/
 |_|   |_|  \___/|_| |_| |_| .__/ \__| |_| \_\___/ \__,_|_|\___|\__|\__\___|
                             |_|
"""

COMPLEXITY_STARS = {1: "*", 2: "**", 3: "***", 4: "****"}


def print_banner():
    print(magenta(BANNER))
    print(bold("  Spin the wheel. Get a wild prompt. Unleash it on your AI."))
    print("  Mad libs meets prompt engineering.\n")


def print_menu():
    print(bold("=== MAIN MENU ===\n"))
    print(f"  {bold('1')}. Spin!  (random prompt)")
    print(f"  {bold('2')}. Spin with complexity  (choose difficulty)")
    print(f"  {bold('3')}. Batch spin  (generate multiple)")
    print(f"  {bold('4')}. Workshop  (build & tweak a prompt)")
    print(f"  {bold('5')}. Browse word banks")
    print(f"  {bold('6')}. Stats")
    print(f"  {bold('Q')}. Quit")
    print()


def display_prompt(result, number=None):
    """Pretty-print a generated prompt."""
    template = result["template"]
    stars = COMPLEXITY_STARS.get(template["complexity"], "?")

    prefix = ""
    if number is not None:
        prefix = f"#{number}  "

    print()
    print(f"  {prefix}{dim(template['name'])}  {yellow(stars)}")
    print(f"  {bold('='*60)}")
    print(f"  {cyan(result['text'])}")
    print(f"  {bold('='*60)}")

    # Show the slot breakdown
    print(f"  {dim('Slots:')}")
    for slot, value in result["fills"].items():
        print(f"    {dim(slot + ':')} {value}")
    print()


def spin(complexity=None):
    """Generate and display a single prompt, with reroll options."""
    result = generate_prompt(complexity=complexity)
    display_prompt(result)

    while True:
        slots = list(result["fills"].keys())
        slot_opts = ", ".join(f"{i+1}={s}" for i, s in enumerate(slots))
        print(dim(f"  Reroll a slot ({slot_opts}), [s]pin again, or [b]ack"))
        try:
            choice = input(f"  {bold('> ')}").strip().lower()
        except (EOFError, KeyboardInterrupt):
            print()
            break

        if not choice or choice == "b" or choice == "back":
            break
        elif choice == "s" or choice == "spin":
            result = generate_prompt(complexity=complexity)
            display_prompt(result)
        elif choice == "c" or choice == "copy":
            print(f"\n  {dim('Copy this prompt:')}")
            print(f"  {result['text']}\n")
        elif choice.isdigit():
            idx = int(choice) - 1
            if 0 <= idx < len(slots):
                result = reroll_slot(result, slots[idx])
                display_prompt(result)
            else:
                print(f"  {red('Invalid slot number.')}\n")
        else:
            print(f"  {dim('Unknown command.')}\n")


def spin_with_complexity():
    """Let user pick a complexity level, then spin."""
    levels = get_complexity_levels()
    print(bold("\n  Choose complexity:\n"))
    for lvl, info in sorted(levels.items()):
        stars = yellow(COMPLEXITY_STARS[lvl])
        print(f"    {bold(str(lvl))}. {info['name']} {stars} — {info['desc']}")
    print(f"    {bold('R')}. Random")
    print()

    try:
        choice = input(f"  {bold('Complexity > ')}").strip().lower()
    except (EOFError, KeyboardInterrupt):
        print()
        return

    if choice == "r":
        spin()
    elif choice.isdigit() and int(choice) in levels:
        spin(complexity=int(choice))
    else:
        print(f"  {dim('Invalid choice, spinning random...')}")
        spin()


def batch_spin():
    """Generate multiple prompts at once."""
    try:
        n = input(f"  How many prompts? (1-20) [{bold('5')}]: ").strip()
    except (EOFError, KeyboardInterrupt):
        print()
        return
    count = int(n) if n.isdigit() and 1 <= int(n) <= 20 else 5

    results = generate_batch(count=count)
    print(bold(f"\n  Generated {len(results)} prompts:\n"))
    for i, result in enumerate(results, 1):
        display_prompt(result, number=i)

    # Export option
    print(dim("  [e]xport to file, or any key to go back"))
    try:
        choice = input(f"  {bold('> ')}").strip().lower()
    except (EOFError, KeyboardInterrupt):
        print()
        return

    if choice == "e":
        _export_batch(results)


def _export_batch(results):
    """Save a batch of prompts to a text file."""
    filename = "prompts.txt"
    try:
        inp = input(f"  Filename [{filename}]: ").strip()
    except (EOFError, KeyboardInterrupt):
        print()
        return
    if inp:
        filename = inp

    with open(filename, "w") as f:
        f.write("PROMPT ROULETTE — Generated Prompts\n")
        f.write("=" * 50 + "\n\n")
        for i, result in enumerate(results, 1):
            f.write(f"#{i} [{result['template']['name']}]\n")
            f.write(f"{result['text']}\n\n")
        f.write("Generated by Prompt Roulette\n")
        f.write("https://github.com/UberGuidoZ/ChatGPT-shenanigans\n")

    print(f"  {green('Saved to')} {bold(filename)}\n")


def workshop():
    """Interactive prompt builder — pick slots one by one or randomize."""
    print(bold("\n=== PROMPT WORKSHOP ===\n"))
    print(dim("  Build a prompt step by step. Pick a template, then fill or randomize each slot.\n"))

    # Pick template
    print(bold("  Available templates:\n"))
    for i, t in enumerate(TEMPLATES, 1):
        stars = yellow(COMPLEXITY_STARS.get(t["complexity"], "?"))
        slots_label = ", ".join(t["slots"])
        print(f"    {bold(str(i)):>4}. {t['name']} {stars}  [{slots_label}]")
    print()

    try:
        choice = input(f"  {bold('Template # > ')}").strip()
    except (EOFError, KeyboardInterrupt):
        print()
        return

    if not choice.isdigit() or int(choice) < 1 or int(choice) > len(TEMPLATES):
        print(f"  {dim('Invalid choice.')}\n")
        return

    template = TEMPLATES[int(choice) - 1]
    fills = {}

    print(f"\n  Template: {bold(template['name'])}")
    print(f"  Pattern:  {dim(template['template'])}\n")

    for slot in template["slots"]:
        options = SLOTS[slot]
        print(f"  {bold(slot.upper())} — pick one or [r]andom:\n")
        for j, opt in enumerate(options, 1):
            print(f"    {j:>2}. {opt}")
        print()

        while True:
            try:
                pick = input(f"  {bold(slot + ' > ')}").strip().lower()
            except (EOFError, KeyboardInterrupt):
                print()
                import random
                fills[slot] = random.choice(options)
                break

            if pick == "r" or pick == "random":
                import random
                fills[slot] = random.choice(options)
                print(f"  {dim('Randomized:')} {fills[slot]}\n")
                break
            elif pick.isdigit():
                idx = int(pick) - 1
                if 0 <= idx < len(options):
                    fills[slot] = options[idx]
                    print()
                    break
                else:
                    print(f"  {red('Out of range.')}")
            else:
                # Treat as custom input
                fills[slot] = pick
                print(f"  {dim('Custom:')} {fills[slot]}\n")
                break

    text = template["template"].format(**fills)
    result = {"text": text, "template": template, "fills": fills}
    display_prompt(result)


def browse_banks():
    """Show all word banks by category."""
    print(bold("\n=== WORD BANKS ===\n"))
    for slot_name, phrases in SLOTS.items():
        print(f"  {yellow(bold(slot_name.upper()))} ({len(phrases)} options)")
        for i, phrase in enumerate(phrases, 1):
            print(f"    {i:>2}. {phrase}")
        print()


def show_stats():
    """Display database statistics."""
    categories = get_slot_categories()
    total_phrases = sum(categories.values())
    total_combos = 1
    for count in categories.values():
        total_combos *= count

    print(bold("\n=== STATS ===\n"))
    print(f"  Templates:    {bold(str(len(TEMPLATES)))}")
    print(f"  Slot types:   {bold(str(len(categories)))}")
    print(f"  Total phrases: {bold(str(total_phrases))}")
    print(f"  Possible combinations: {bold(f'{total_combos:,}+')}")
    print()
    print(bold("  Slot breakdown:"))
    for name, count in sorted(categories.items()):
        bar = green("|" * min(count, 30))
        print(f"    {name:<14} {count:>3} {bar}")
    print()
    print(bold("  Templates by complexity:"))
    for lvl, info in sorted(get_complexity_levels().items()):
        count = sum(1 for t in TEMPLATES if t["complexity"] == lvl)
        stars = yellow(COMPLEXITY_STARS[lvl])
        print(f"    {info['name']:<10} {stars:<5} {count} templates")
    print()


def main():
    print_banner()

    while True:
        print_menu()
        try:
            choice = input(bold("Choose > ")).strip().lower()
        except (EOFError, KeyboardInterrupt):
            print(f"\n{dim('Goodbye!')}")
            break

        if choice == "q":
            print(f"\n{dim('May your prompts be ever absurd.')}")
            break

        elif choice == "1":
            spin()

        elif choice == "2":
            spin_with_complexity()

        elif choice == "3":
            batch_spin()

        elif choice == "4":
            workshop()

        elif choice == "5":
            browse_banks()

        elif choice == "6":
            show_stats()

        else:
            print(red("  Invalid choice. Try 1-6 or Q.\n"))


if __name__ == "__main__":
    main()
