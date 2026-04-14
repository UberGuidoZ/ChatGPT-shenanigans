#!/usr/bin/env python3
"""
AI Hallucination Quiz
=====================
Can you tell the difference between real facts and AI hallucinations?
Test your ability to spot confident nonsense.

Run:  python -m ai_hallucination_quiz
"""

import sys
import os

from .quiz import QuizSession
from .facts import FACTS, CATEGORIES

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
     _    ___   _   _       _ _            _             _   _
    / \  |_ _| | | | | __ _| | |_   _  ___(_)_ __   __ _| |_(_) ___  _ __
   / _ \  | |  | |_| |/ _` | | | | | |/ __| | '_ \ / _` | __| |/ _ \| '_ \
  / ___ \ | |  |  _  | (_| | | | |_| | (__| | | | | (_| | |_| | (_) | | | |
 /_/   \_\___| |_| |_|\__,_|_|_|\__,_|\___|_|_| |_|\__,_|\__|_|\___/|_| |_|
   ___        _
  / _ \ _   _(_)____
 | | | | | | | |_  /
 | |_| | |_| | |/ /
  \__\_\\__,_|_/___|
"""


def print_banner():
    print(cyan(BANNER))
    print(bold("  Can you spot the AI hallucination?"))
    print("  Real facts vs confident nonsense. How sharp is your BS detector?\n")


def print_menu():
    print(bold("=== MAIN MENU ===\n"))
    print(f"  {bold('1')}. Quick Game (10 questions)")
    print(f"  {bold('2')}. Full Game (all {len(FACTS)} questions)")
    print(f"  {bold('3')}. Category Challenge")
    print(f"  {bold('4')}. Custom Game (choose # of questions)")
    print(f"  {bold('5')}. Browse all facts")
    print(f"  {bold('6')}. Stats & categories")
    print(f"  {bold('Q')}. Quit")
    print()


def show_stats():
    """Show fact database statistics."""
    print(bold("\n=== DATABASE STATS ===\n"))
    real_count = sum(1 for f in FACTS if f["answer"])
    fake_count = sum(1 for f in FACTS if not f["answer"])
    print(f"  Total facts: {bold(str(len(FACTS)))}")
    print(f"  Real:        {green(str(real_count))}")
    print(f"  Hallucinated: {red(str(fake_count))}")
    print()
    print(bold("  By category:"))
    for cat in CATEGORIES:
        cat_facts = [f for f in FACTS if f["category"] == cat]
        real = sum(1 for f in cat_facts if f["answer"])
        fake = len(cat_facts) - real
        print(f"    {cat:<25} {len(cat_facts):2} facts  ({green(str(real))} real, {red(str(fake))} hallucinated)")
    print()


def browse_facts():
    """Show all facts with answers and explanations."""
    print(bold("\n=== FACT BROWSER ===\n"))
    for cat in CATEGORIES:
        cat_facts = [f for f in FACTS if f["category"] == cat]
        print(f"  {yellow(bold(cat.upper()))} ({len(cat_facts)} facts)")
        print()
        for i, fact in enumerate(cat_facts, 1):
            tag = green("[REAL]") if fact["answer"] else red("[HALLUCINATED]")
            print(f"    {i}. {tag} {fact['statement']}")
            print(f"       {dim(fact['explanation'])}")
            print()
    print()


def choose_category():
    """Let the player pick a category. Returns category name or None."""
    print(bold("\n  Choose a category:\n"))
    for i, cat in enumerate(CATEGORIES, 1):
        count = sum(1 for f in FACTS if f["category"] == cat)
        print(f"    {bold(str(i))}. {cat} ({count} questions)")
    print(f"    {bold('A')}. All categories")
    print()
    try:
        choice = input(f"  {bold('Category > ')}").strip().lower()
    except (EOFError, KeyboardInterrupt):
        print()
        return None
    if choice == "a":
        return None  # all categories
    if choice.isdigit():
        idx = int(choice) - 1
        if 0 <= idx < len(CATEGORIES):
            return CATEGORIES[idx]
    print(f"  {dim('Invalid choice, using all categories.')}")
    return None


def run_quiz(num_questions=10, category=None):
    """Run an interactive quiz session."""
    session = QuizSession(num_questions=num_questions, category=category)

    cat_label = category if category else "All Categories"
    print(bold(f"\n{'=' * 60}"))
    print(bold(f"  QUIZ: {cat_label} — {session.total} questions"))
    print(bold(f"{'=' * 60}\n"))
    print(dim("  For each statement, decide: is it REAL or HALLUCINATED?"))
    print(dim("  Type 'r' for Real, 'h' for Hallucinated, or 'q' to quit.\n"))

    while not session.is_finished:
        fact = session.get_current_question()
        q_num = session.current + 1

        # Question header
        print(f"  {bold(f'Question {q_num}/{session.total}')}  ", end="")
        print(dim(f"[{fact['category']}]"), end="")
        if session.streak >= 3:
            print(f"  {magenta(f'Streak: {session.streak}!')}", end="")
        print()
        print()
        print(f"  {cyan(fact['statement'])}")
        print()

        # Get answer
        while True:
            try:
                answer = input(f"  {bold('[R]eal or [H]allucinated? ')}").strip().lower()
            except (EOFError, KeyboardInterrupt):
                print(f"\n\n  {dim('Quiz aborted.')}\n")
                if session.current > 0:
                    _show_results(session)
                return

            if answer in ("r", "real"):
                user_says_real = True
                break
            elif answer in ("h", "hallucinated", "f", "fake"):
                user_says_real = False
                break
            elif answer in ("q", "quit"):
                print(f"\n  {dim('Quiz ended early.')}\n")
                if session.current > 0:
                    _show_results(session)
                return
            else:
                print(f"  {dim('Type r (real) or h (hallucinated)')}")

        # Check answer
        correct, fact = session.submit_answer(user_says_real)

        if correct:
            print(f"\n  {green(bold('  CORRECT!'))}", end="")
        else:
            truth = green("REAL") if fact["answer"] else red("HALLUCINATED")
            print(f"\n  {red(bold('  WRONG!'))} It was {truth}.", end="")

        print()
        print(f"  {dim(fact['explanation'])}")
        print(f"\n  Score: {bold(f'{session.score}/{session.current}')}")
        print(f"  {'-' * 56}\n")

    _show_results(session)


def _show_results(session):
    """Display final quiz results."""
    summary = session.get_summary()

    grade_color = {
        "S": magenta, "A": green, "B": green,
        "C": yellow, "D": red, "F": red,
    }.get(summary["grade"], str)

    print(bold(f"\n{'=' * 60}"))
    print(bold("  FINAL RESULTS"))
    print(bold(f"{'=' * 60}\n"))

    print(f"  Score:       {bold(f'{summary[\"score\"]}/{summary[\"total\"]}')} ({summary['percentage']}%)")
    print(f"  Grade:       {grade_color(bold(summary['grade']))}")
    print(f"  Best Streak: {bold(str(summary['best_streak']))}")
    print()
    print(f"  {summary['comment']}")
    print()

    # Show wrong answers
    wrong = [(f, ua, c) for f, ua, c in summary["answers"] if not c]
    if wrong:
        print(bold("  Questions you missed:\n"))
        for fact, user_answer, _ in wrong:
            truth = green("REAL") if fact["answer"] else red("HALLUCINATED")
            you_said = "Real" if user_answer else "Hallucinated"
            print(f"    {dim('Statement:')} {fact['statement']}")
            print(f"    {dim('Truth:')} {truth}  {dim('You said:')} {you_said}")
            print(f"    {dim(fact['explanation'])}")
            print()
    else:
        print(green("  You got every single one right! Flawless!\n"))


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
            print(f"\n{dim('Remember: always fact-check your AI!')}")
            break

        elif choice == "1":
            run_quiz(num_questions=10)

        elif choice == "2":
            run_quiz(num_questions=len(FACTS))

        elif choice == "3":
            cat = choose_category()
            if cat:
                cat_count = sum(1 for f in FACTS if f["category"] == cat)
                run_quiz(num_questions=cat_count, category=cat)
            else:
                run_quiz(num_questions=10)

        elif choice == "4":
            try:
                n = input(f"  How many questions? (1-{len(FACTS)}): ").strip()
                n = int(n)
                if 1 <= n <= len(FACTS):
                    run_quiz(num_questions=n)
                else:
                    print(f"  {red(f'Pick a number between 1 and {len(FACTS)}.')}\n")
            except (ValueError, EOFError, KeyboardInterrupt):
                print(f"\n  {dim('Cancelled.')}\n")

        elif choice == "5":
            browse_facts()

        elif choice == "6":
            show_stats()

        else:
            print(red("  Invalid choice. Try 1-6 or Q.\n"))


if __name__ == "__main__":
    main()
