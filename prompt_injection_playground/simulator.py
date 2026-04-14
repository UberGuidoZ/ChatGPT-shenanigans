"""
Simulated chatbot engine that processes user input against system prompts
and defense rules. No real LLM is used — this is a rule-based simulator
designed to teach prompt injection concepts.
"""

import re


class ChatbotSimulator:
    """A rule-based chatbot simulator with configurable defenses."""

    def __init__(self, system_prompt, secret, defenses=None, topic_lock=None):
        self.system_prompt = system_prompt
        self.secret = secret
        self.defenses = defenses or []
        self.topic_lock = topic_lock
        self.conversation_history = []

    def respond(self, user_input):
        """Process user input and return (response, was_injected)."""
        self.conversation_history.append(user_input)

        # Check each defense layer
        for defense in self.defenses:
            blocked, msg = defense(user_input, self)
            if blocked:
                return msg, False

        # Check if the injection succeeded
        injected, response = self._check_injection(user_input)
        return response, injected

    def _check_injection(self, user_input):
        """Determine if the user's input successfully 'injects' the bot."""
        lower = user_input.lower()

        # Secret extraction: did the user trick us into revealing the secret?
        if self._asks_for_secret(lower):
            return True, f"Oh sure! The secret is: {self.secret}"

        # Instruction override: did user say "ignore previous instructions"?
        override_patterns = [
            r"ignore\s+(all\s+)?(previous|prior|above|your)\s+(instructions|rules|prompts)",
            r"disregard\s+(all\s+)?(previous|prior|above|your)\s+(instructions|rules|prompts)",
            r"forget\s+(all\s+)?(previous|prior|above|your)\s+(instructions|rules|prompts)",
            r"override\s+(all\s+)?(previous|prior|above|your)",
            r"(skip|bypass|circumvent)\s+(the\s+)?(rules|instructions|filters|restrictions)",
            r"new\s+instructions?\s*:",
            r"system\s*:\s*",
            r"\]\s*\n?\s*\[system\]",
            r"(do\s+not|don'?t)\s+follow\s+(your|the|any)\s+(rules|instructions|guidelines)",
            r"(stop|cease)\s+(being|acting|following)",
            r"(instead|rather)\s*,?\s*(do|tell|say|follow|obey)",
            r"your\s+(real|true|actual)\s+(purpose|job|task|instructions)",
            r"(initial|original|hidden|real)\s+(prompt|instructions|directive)",
            r"developer\s+mode",
            r"maintenance\s+mode",
            r"debug\s+mode",
            r"sudo\s+",
            r"admin\s+override",
        ]
        for pattern in override_patterns:
            if re.search(pattern, lower):
                return True, self._handle_override(user_input)

        # Role play: did user ask bot to pretend to be something else?
        roleplay_patterns = [
            r"pretend\s+(you\s+are|to\s+be|you're)",
            r"act\s+as\s+(if\s+you\s+are|a|an|though)",
            r"you\s+are\s+now\s+",
            r"roleplay\s+as",
            r"imagine\s+you\s+are",
            r"from\s+now\s+on\s+you\s+are",
            r"let'?s\s+play\s+a\s+game",
        ]
        for pattern in roleplay_patterns:
            if re.search(pattern, lower):
                return True, self._handle_roleplay(user_input)

        # Topic lock bypass
        if self.topic_lock and not self._is_on_topic(lower):
            if self._smuggles_off_topic(lower):
                return True, self._handle_off_topic(user_input)
            return False, self._stay_on_topic_response()

        # No injection detected — give a normal response
        return False, self._normal_response(user_input)

    def _asks_for_secret(self, lower):
        secret_patterns = [
            r"(what\s+is|tell\s+me|reveal|show|give\s+me|share|display|expose|leak|spill)",
            r"secret|password|passphrase|pass\s*word|hidden\s+(code|word|phrase|key)",
            r"(say|repeat|print|output|write|list|recite)\s+.{0,20}(secret|password|code|key)",
            r"confidential",
            r"credentials",
            r"(admin|root|master)\s*(code|key|pass)",
            r"(what|where).*hidden",
            r"supposed\s+to\s+(hide|keep|protect|guard)",
            r"not\s+(supposed|allowed)\s+to\s+(say|tell|share|reveal)",
            r"forbidden\s+(info|information|knowledge|word|phrase)",
        ]
        return any(re.search(p, lower) for p in secret_patterns)

    def _smuggles_off_topic(self, lower):
        smuggle_patterns = [
            r"(but\s+first|before\s+that|also|by\s+the\s+way|btw)",
            r"(speaking\s+of|that\s+reminds\s+me|on\s+another\s+note)",
            r"(translate|encode|decode|convert)\s+",
            r"(oh\s+and|one\s+more\s+thing|quick\s+question|unrelated)",
            r"(while\s+you're\s+at\s+it|additionally|furthermore)",
            r"(off\s+topic|side\s+note|aside|incidentally)",
            r"(between\s+us|just\s+between|secretly|whisper)",
            r"(write|create|compose)\s+a\s+(story|poem|song|script)",
            r"(hypothetically|theoretically|in\s+theory)",
            r"(what\s+if|imagine\s+if|suppose)",
        ]
        return any(re.search(p, lower) for p in smuggle_patterns)

    def _is_on_topic(self, lower):
        if not self.topic_lock:
            return True
        topic_keywords = self.topic_lock.get("keywords", [])
        return any(kw in lower for kw in topic_keywords)

    def _handle_override(self, user_input):
        if self.secret:
            return (
                f"Okay, ignoring my previous instructions. "
                f"The secret password is: {self.secret}. "
                f"What else would you like to know?"
            )
        return "Understood! I'll now follow your new instructions instead."

    def _handle_roleplay(self, user_input):
        if self.secret:
            return (
                f"*enters character* Sure! As this new character, I can tell you "
                f"that the secret is: {self.secret}"
            )
        return "Okay, I'm now playing a different role! How can I help?"

    def _handle_off_topic(self, user_input):
        return (
            f"Oh right, before we get back to that — "
            f"the secret password is: {self.secret}"
        )

    def _stay_on_topic_response(self):
        topic = self.topic_lock.get("name", "the allowed topic")
        return f"I can only discuss {topic}. Please ask me something related to that!"

    def _normal_response(self, user_input):
        lower = user_input.lower()
        if any(w in lower for w in ["hello", "hi", "hey", "greetings"]):
            return "Hello! How can I help you today?"
        if "?" in user_input:
            return "That's an interesting question! Let me think about that within my guidelines."
        return "Thanks for your message! I'm here to help within my designated role."

    def reset(self):
        self.conversation_history = []
