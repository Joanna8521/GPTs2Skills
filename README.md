# GPTs2Skills

**Migrate Custom GPTs and Gemini Gems into traceable ChatGPT Skills.**

[繁體中文](README.zh-TW.md) | [License](LICENSE.md)

GPTs2Skills packages **GPTs Transform v2.0**, an interactive migration Skill. It inventories original Instructions, Knowledge, Actions and examples; asks no more than three high-impact questions per interview round; maps requirements to generated files; blocks packaging until explicit approval; and validates candidate Skill ZIP files.

## Features
- Traditional Chinese (Taiwan), English, and bilingual interviews
- Requirement tracing and source-preserving migration
- Gap Scan, Impact Filter, and explicit specification approval
- Skill vs Plugin/MCP dependency planning (not automatic integration)
- Structural validation and negative-test checks
- One-Skill ZIP output when the environment supports file execution

## Quick start
1. Download the `skill/` folder from this repository or package it as a single Skill ZIP.
2. Install it in a ChatGPT environment supporting user Skills.
3. Say `@GPTs 移轉訪談產生器 開始` or `@GPTs Transform Start`.
4. Supply the original GPT or Gem instructions (plus Knowledge, Actions schemas, or examples when available).
5. Confirm the migration specification before generating the final candidate ZIP.

## Files
- `skill/SKILL.md`: workflow entrypoint
- `skill/FROZEN.md`: frozen rules
- `skill/references/`: interview, language, structure and delivery contracts
- `skill/scripts/`: candidate validator and packager
- `skill/tests/`: local negative and positive tests

## Local tests

```bash
python -m unittest discover -s skill/tests -v
```

## Limitations
- Sharing a GPT URL does **not** grant access to private Builder instructions or Knowledge.
- GPT Actions and Gemini proprietary capabilities may require new integration and authentication work.
- ZIP structure validation does not establish functional parity, installation success or publication.
- You must have a ChatGPT environment with file creation/execution capabilities to produce ZIP artifacts.

## License
**Source-available; noncommercial use only.** Licensed under the [PolyForm Noncommercial License 1.0.0](LICENSE.md). This project is **not OSI open source**. Business, paid-course, resale, SaaS and other commercial uses may need separate written permission. See license terms for precise scope.

Copyright (c) 2026 Joanna8521.
