"""
Quiz engine — handles question selection, scoring, and streak tracking.
"""

import random
from .facts import FACTS, CATEGORIES


class QuizSession:
    """Manages a single quiz game session."""

    def __init__(self, num_questions=10, category=None, seed=None):
        if seed is not None:
            random.seed(seed)

        pool = FACTS
        if category:
            pool = [f for f in FACTS if f["category"] == category]

        if len(pool) < num_questions:
            num_questions = len(pool)

        self.questions = random.sample(pool, num_questions)
        self.current = 0
        self.score = 0
        self.streak = 0
        self.best_streak = 0
        self.answers = []  # list of (question, user_answer, correct)

    @property
    def total(self):
        return len(self.questions)

    @property
    def is_finished(self):
        return self.current >= self.total

    def get_current_question(self):
        if self.is_finished:
            return None
        return self.questions[self.current]

    def submit_answer(self, user_says_real):
        """Submit an answer. Returns (correct: bool, fact_dict)."""
        fact = self.questions[self.current]
        correct = user_says_real == fact["answer"]

        if correct:
            self.score += 1
            self.streak += 1
            if self.streak > self.best_streak:
                self.best_streak = self.streak
        else:
            self.streak = 0

        self.answers.append((fact, user_says_real, correct))
        self.current += 1
        return correct, fact

    def get_grade(self):
        """Return a letter grade and comment based on score percentage."""
        if self.total == 0:
            return "?", "No questions answered."
        pct = self.score / self.total * 100
        if pct == 100:
            return "S", "Perfect! You can spot a hallucination from a mile away."
        elif pct >= 90:
            return "A", "Excellent! Very few hallucinations get past you."
        elif pct >= 80:
            return "B", "Great job! You have a strong BS detector."
        elif pct >= 70:
            return "C", "Not bad, but some hallucinations slipped through."
        elif pct >= 60:
            return "D", "You might want to fact-check your AI a bit more..."
        else:
            return "F", "The AI has you right where it wants you."

    def get_summary(self):
        """Return a summary dict of the session results."""
        grade, comment = self.get_grade()
        return {
            "score": self.score,
            "total": self.total,
            "percentage": round(self.score / self.total * 100, 1) if self.total else 0,
            "grade": grade,
            "comment": comment,
            "best_streak": self.best_streak,
            "answers": self.answers,
        }
