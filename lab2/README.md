# Week 2 Lab — Tokens, System Prompts, and Context

This repository contains the materials for the Week 2 lab, which explores three practical constraints of working with LLM APIs: tokenization and cost, system prompt sensitivity, and instruction adherence over a long context.

**Lab instructions: [Week 2 Lab](https://csic30216-fall26.denniswang.net/labs/week2/)

## Repository Contents

| Path | Description |
|---|---|
| `week2_lab_handout.md` | Full lab instructions, including setup, task descriptions, and grading checklist |
| `task1.py` | Task 1 primary path — offline token counting with `tiktoken` (no API key required) |
| `task1_claude.py`, `task1_gemini.py` | Task 1 optional appendix — real token counts via the Claude and Gemini APIs |
| `task1_file/` | Fixed input files used by Task 1 (sentence, paragraph, Mandarin translation, code, JSON) |
| `task2_claude.py`, `task2_gemini.py` | Task 2 optional appendix — system prompt sensitivity via the API |
| `task3_claude.py`, `task3_gemini.py` | Task 3 optional appendix — instruction dilution via the API |
| `claude_client.py`, `gemini_client.py` | Shared API client setup, used by the appendix scripts above |

## Getting Started

Most of this lab can be completed with no account or API key, using the chat interfaces at claude.ai and gemini.google.com. Optional appendix scripts are provided for students with existing, funded API access to Anthropic and/or Google.

Full setup and task-by-task instructions are in [`week2_lab_handout.md`](./week2_lab_handout.md).

## Notes

- If you use the optional API appendices, you will need your own API key(s) and a local `.env` file — see the Setup section of the handout for details.
- Never commit a `.env` file or an API key to this repository.
