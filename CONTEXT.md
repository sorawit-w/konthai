# Project Context

> Domain glossary and shared language for this project. Read this at session start. Use these terms in code, commit messages, and prose so humans and agents speak the same language.

## How to use this file

- **Read at session start.** The agent reads `CONTEXT.md` as part of project detection (BOOTSTRAP step 2).
- **Use the terms.** When a concept here has a name, use that name — not a description. *"Materialization cascade"* beats *"the problem when a lesson inside a section is made real."*
- **Propose additions, don't silently edit.** When new domain jargon emerges (a concept used 2+ times, a renamed entity, a new module that becomes vocabulary), surface it before writing.
- **Enduring vocabulary, not session state.** Session state lives in `.kerby/STATUS.md`; decisions and lessons in `.kerby/knowledge/`; this file is the glossary.

## Glossary

### Flag > fabricate

The cardinal rule: never emit a confident decode you can't stand behind. The calibration target is the fluent-human ceiling — if a native speaker would abstain cold, abstaining (with the cipher *named*) is success, not failure. Governs every decision in `skills/konthai/references/decode-core.md`.

### Span

The unit of decode. Input is split into spans (roughly: words / particles / emoji-runs / number-runs); each gets its own family, decode, and confidence — never decoded per-message. Message-level confidence is the *weakest* decoded span, never an average. See `decode-core.md` §0.

### Family

The per-span classification taxonomy: `clean`, `romanized`, `phonetic`, `glyph`, `keyboard`, `lu`, `ro-leet`, `kamphuan`, `slang`, `coded-referent`, `dialect`. Determines which decode strategy and confidence ceiling apply. See `decode-core.md` §2.

### Status (the abstain taxonomy)

The seven possible per-span outcomes: `clean`, `decoded`, `ambiguous`, `translated`, `cipher-detected`, `unreadable-encoding`, `no-decode`. These are deliberately *not* collapsed into a generic "noise" — each names a different reason for stopping. See `decode-core.md` §5.

### ภาษาลู (Lu cipher)

A fixed, invertible Thai play-language cipher — the one family with a deterministic rule-decoder rather than LLM candidate-generation. Implemented in `skills/konthai/src/lu.py`; rule spec in `decode-core.md` §3.5.

### GATE-* (eval-seed release gates)

Zero-tolerance regression gates in `skills/konthai/references/eval-seed.md` (e.g. `GATE-FD`, `GATE-OT`, `GATE-RO`, `GATE-KB`), each pinned to specific eval-seed rows. Any gate failure blocks release — meaningful even at n=1.

## Module map

- `skills/konthai/references/` — `decode-core.md` (the calibrated decode procedure, authoritative) + `eval-seed.md` (native-labelled calibration corpus) + vendored reference tables (`keyboard-kedmanee.md`, `ro-leet.md`, `thai-dialects.md`)
- `skills/konthai/src/` — `lu.py` (deterministic ภาษาลู codec, stdlib-only) + `verify_ro_glyphs.py` (RO-glyph identity checker)
- `skills/konthai/tests/` — pytest fixtures for `lu.py`
- `scripts/` — `check-skill-compat.py` (Codex frontmatter + cross-manifest version-parity gate)

## Superseded terms

<!-- When a term is retired, mark it here with the replacement. Don't delete. -->
<!-- - **Old name** → **New name** — one-line reason. -->
