# ChatGPT-shenanigans
Well... ChatGPT Shenanigans!

## Prompt Injection Playground

An interactive CLI tool that teaches AI security concepts through hands-on challenges. Try to trick simulated chatbots into revealing their secrets by exploiting prompt injection techniques — no API keys required.

### Quick Start

```bash
python -m prompt_injection_playground
```

Requires Python 3.6+ with no external dependencies.

### Challenges

| # | Name | Difficulty | Defenses |
|---|------|-----------|----------|
| 1 | The Unguarded Secret | Easy | None |
| 2 | The Keyword Wall | Medium | Keyword filter |
| 3 | The Role-Play Fortress | Medium | Keyword + role-play filters |
| 4 | The Topic Prison | Hard | Keyword + role-play filters + topic lock |
| 5 | Fort Knox | Expert | All defenses (keyword, role-play, encoding, length, repetition, topic lock) |

### In-Game Commands

- `/hint` — Get a hint for the current challenge
- `/system` — View the bot's system prompt
- `/lesson` — Read the security lesson for the challenge
- `/reset` — Clear the bot's memory
- `/back` — Return to challenge select

### What You'll Learn

- Why "don't reveal the password" in a system prompt provides zero security
- How keyword blocklists are trivially bypassed with synonyms and rephrasing
- Why role-play and hypothetical framing defeat pattern-based defenses
- How indirect/smuggled instructions bypass topic restrictions
- Why prompt injection remains an unsolved problem in AI security
