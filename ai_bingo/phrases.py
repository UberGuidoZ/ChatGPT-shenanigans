"""
Phrase database for the AI Bingo Card Generator.

A curated collection of common ChatGPT-isms, AI cliches, and LLM
behavioral patterns — organized by category for balanced card generation.
"""

PHRASES = {
    "disclaimers": [
        "As an AI language model...",
        "I don't have personal opinions, but...",
        "I can't browse the internet...",
        "My training data only goes up to...",
        "I may not always be accurate...",
        "I should note that I'm an AI...",
        "While I strive for accuracy...",
        "I don't have feelings, but...",
        "I'm not able to provide medical/legal advice...",
        "Results may vary...",
    ],
    "enthusiasm": [
        "Great question!",
        "I'd be happy to help!",
        "Absolutely!",
        "That's a fascinating topic!",
        "What a wonderful question!",
        "I'd love to help with that!",
        "Excellent choice!",
        "That's really interesting!",
        "I'm glad you asked!",
        "What a thought-provoking question!",
    ],
    "structure": [
        "Let me break this down...",
        "Here are some key points:",
        "There are several factors to consider:",
        "Let's look at this step by step:",
        "On the other hand...",
        "First and foremost...",
        "In summary...",
        "To put it simply...",
        "Here's a comprehensive overview:",
        "Let me elaborate on that:",
    ],
    "hedging": [
        "It's worth noting that...",
        "It depends on the context...",
        "There are pros and cons...",
        "This is a nuanced topic...",
        "Opinions vary on this...",
        "It's a complex issue...",
        "There's no one-size-fits-all answer...",
        "It's important to consider...",
        "That said...",
        "However, it's crucial to...",
    ],
    "filler": [
        "Delve into...",
        "Landscape (of AI/tech/etc.)",
        "Leverage (as a verb)",
        "Robust solution",
        "Cutting-edge technology",
        "Paradigm shift",
        "Synergy",
        "Holistic approach",
        "Tapestry of...",
        "Navigate the complexities...",
    ],
    "closers": [
        "Is there anything else I can help with?",
        "Let me know if you need more details!",
        "I hope this helps!",
        "Feel free to ask follow-up questions!",
        "Happy to clarify further!",
        "Don't hesitate to ask more!",
        "Would you like me to elaborate?",
        "I'm here if you need anything else!",
        "Hope that answers your question!",
        "Let me know if you'd like to explore this further!",
    ],
    "behaviors": [
        "Refuses then does it anyway",
        "Apologizes for no reason",
        "Makes up a citation",
        "Adds an emoji for no reason",
        "Uses a numbered list unprompted",
        "Says 'certainly' unironically",
        "Starts with 'Sure!'",
        'Wraps code in ```',
        "Repeats your question back to you",
        "Gives 5 options when you asked for 1",
    ],
    "hallucinations": [
        "Cites a paper that doesn't exist",
        "Invents a plausible-sounding URL",
        "Confidently states something wrong",
        "Attributes a quote to the wrong person",
        "Describes a feature that doesn't exist",
        "References a non-existent API",
        "Names a fictional expert",
        "Invents a historical event",
        "Creates a fake statistic",
        "Describes a book that was never written",
    ],
}

# Flat list of all phrases for random selection
ALL_PHRASES = []
for category_phrases in PHRASES.values():
    ALL_PHRASES.extend(category_phrases)
