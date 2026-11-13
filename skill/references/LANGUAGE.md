# Language contract | 語言契約 v2.0

## Detection and switching
- Infer language from current user message; if mixed, prefer the dominant conversational language, not a word count from pasted source instructions.
- Respect explicit `zh-TW`, `en`, `bilingual` user choice. Default to Traditional Chinese (Taiwan) when interacting with a Traditional Chinese-speaking student; never switch to Simplified Chinese.
- An English student gets English questions, explanations, progress, file descriptions, and test notes. A bilingual student gets concise paired headings and substantive explanations in both languages as needed, without duplicating huge source content.
- Keep original source snippets byte-for-byte as provided in `manifest.json` and the evidence map (after only consented secret redaction). Preserve proper nouns, commands, endpoints, filenames, JSON keys, code, and model/API identifiers. Do not translate them silently.
- Generated Skill language defaults to the intended **end user's** language as confirmed by the student, which may differ from interview language. If unclear and outcome differs, ask one high-impact question.

## Punctuation
- Prose written in zh-TW uses Taiwanese terms and natural full-width punctuation. Avoid Chinese em dashes. Do not run Chinese punctuation transforms on English paragraphs, code, URLs, YAML, JSON, OpenAPI, filenames, or verbatim sourced text.
- English prose uses standard English punctuation. ASCII syntax in code and filenames is mandatory.
- Mixed paragraphs preserve the conventions of each language without corrupting instructions.

## Functional parity
- Translation is not proof of equivalent functionality. Preserve original rule precedence, safety constraints, exception behavior, examples and formatting requirements.
- For a bilingual generated Skill, define explicit language selection rules, output language expectations, and at least one test per language. Add a mixed-language test when source language is mixed.
- Explicitly identify untranslatable platform capabilities in both languages where relevant; never claim GPT Actions, Gemini extensions, memory, or proprietary features moved automatically.

## Interview examples
zh-TW: 「你原本的 GPT 是否需要讀取 Google 試算表？是唯讀，還是需要修改資料？」
en: “Does your original GPT need to read Google Sheets? Is it read-only, or must it also modify data?”
Bilingual: 「此操作是否會修改外部資料？／Will this operation change external data?」
