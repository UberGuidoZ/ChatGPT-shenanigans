"""
Bingo card generation and rendering.

Generates 5x5 bingo cards with a balanced mix of phrase categories,
a FREE center square, and clean terminal-based display.
"""

import random
import textwrap

from .phrases import PHRASES, ALL_PHRASES

CARD_SIZE = 5
FREE_SPACE = "FREE SPACE"
CELL_WIDTH = 22
HEADER = "B-I-N-G-O"


def generate_card(seed=None):
    """
    Generate a 5x5 bingo card with balanced category representation.

    Returns a 5x5 list of phrase strings, with the center as FREE SPACE.
    """
    if seed is not None:
        random.seed(seed)

    # Pick phrases with category balance: at least 2 from each category,
    # then fill remaining slots randomly
    needed = CARD_SIZE * CARD_SIZE - 1  # 24 phrases + 1 free space
    selected = []
    categories = list(PHRASES.keys())

    # Guarantee at least 2 from each category (if we have enough categories)
    for cat in categories:
        pool = list(PHRASES[cat])
        random.shuffle(pool)
        selected.extend(pool[:min(3, len(pool))])

    # Deduplicate and trim if we overshot
    selected = list(dict.fromkeys(selected))  # preserves order, removes dupes

    # Fill remaining slots from the full pool
    remaining = [p for p in ALL_PHRASES if p not in selected]
    random.shuffle(remaining)
    selected.extend(remaining)

    # Take exactly what we need and shuffle
    selected = selected[:needed]
    random.shuffle(selected)

    # Build the 5x5 grid
    grid = []
    idx = 0
    center = CARD_SIZE // 2
    for row in range(CARD_SIZE):
        grid_row = []
        for col in range(CARD_SIZE):
            if row == center and col == center:
                grid_row.append(FREE_SPACE)
            else:
                grid_row.append(selected[idx])
                idx += 1
        grid.append(grid_row)

    return grid


def _wrap_cell(text, width):
    """Wrap text to fit within a cell, returning a list of lines."""
    lines = textwrap.wrap(text, width=width - 2)
    if not lines:
        lines = [""]
    return lines


def render_card(grid, marked=None):
    """
    Render a bingo card as a formatted string for the terminal.

    marked: optional set of (row, col) tuples that have been marked.
    """
    if marked is None:
        marked = set()

    # Always mark the free space
    center = CARD_SIZE // 2
    marked = marked | {(center, center)}

    lines = []

    # Header
    header_cells = list(HEADER.replace("-", ""))
    header_line = "+"
    header_content = "|"
    for letter in header_cells:
        header_line += "-" * (CELL_WIDTH + 2) + "+"
        header_content += " " + letter.center(CELL_WIDTH) + " |"
    lines.append(header_line)
    lines.append(header_content)
    lines.append(header_line)

    # Grid rows
    for row_idx, row in enumerate(grid):
        # Wrap all cells and find the max height for this row
        wrapped = [_wrap_cell(cell, CELL_WIDTH) for cell in row]
        max_height = max(len(w) for w in wrapped)

        # Pad shorter cells with empty lines
        for w in wrapped:
            while len(w) < max_height:
                w.append("")

        # Render each sub-line of the row
        for line_idx in range(max_height):
            content = "|"
            for col_idx, cell_lines in enumerate(wrapped):
                text = cell_lines[line_idx]
                is_marked = (row_idx, col_idx) in marked
                if is_marked:
                    cell_str = f"[{text.center(CELL_WIDTH)}]"
                else:
                    cell_str = f" {text.center(CELL_WIDTH)} "
                content += cell_str + "|"
            lines.append(content)

        # Row separator
        sep = "+"
        for _ in range(CARD_SIZE):
            sep += "-" * (CELL_WIDTH + 2) + "+"
        lines.append(sep)

    return "\n".join(lines)


def check_bingo(marked):
    """Check if marked positions form a bingo (row, column, or diagonal)."""
    center = CARD_SIZE // 2
    marked = marked | {(center, center)}  # free space always counted

    wins = []

    # Check rows
    for r in range(CARD_SIZE):
        if all((r, c) in marked for c in range(CARD_SIZE)):
            wins.append(("row", r))

    # Check columns
    for c in range(CARD_SIZE):
        if all((r, c) in marked for r in range(CARD_SIZE)):
            wins.append(("column", c))

    # Check diagonals
    if all((i, i) in marked for i in range(CARD_SIZE)):
        wins.append(("diagonal", "top-left to bottom-right"))
    if all((i, CARD_SIZE - 1 - i) in marked for i in range(CARD_SIZE)):
        wins.append(("diagonal", "top-right to bottom-left"))

    return wins
