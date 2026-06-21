# Changelog

All notable changes to `konthai` are documented here. Format follows
[Keep a Changelog](https://keepachangelog.com/); versioning is semver.

## [0.2.0] — 2026-06-20

Situational context and regional dialect as honesty-bounded priors. A parse-failure now
has three causes — obfuscation (decode), regional dialect (translate), genuine noise
(abstain) — and konthai translates clean dialect itself as a self-contained fallback. The
cardinal rule is unchanged: priors may lower confidence freely, raise it only within a
span's family, and never promote `ambiguous → decoded`.

### Added
- **`skills/konthai/references/thai-dialects.md`** — vendored, notes-only Thai dialect
  reference (recognition tells for `th-lanna`/`th-south`/`th-isan`; `th-genz`/`th-bupphe`
  as negative boundaries), synced from `agent-skills`' `locale-knowledge.md` with a dated
  sync header. Lets konthai recognize regional dialect and translate clean dialect without
  a sibling-skill dependency.
- New output statuses **`translated`** (a clean regional-dialect span → standard Thai) and
  **`clean`** (parses literally; nothing to decode), a **`variant`** field
  (`th-lanna`/`th-south`/`th-isan`/`unknown`), and a `dialect` family.
- Situational context as an optional prior (platform / thread / register / relationship)
  feeding Detection and candidate ranking.
- Eval gates in `references/eval-seed.md` — **GATE-FD** (dialect false-decode),
  **GATE-BR** (beyond-reference honesty), **GATE-ATTR** (attribution trap), **GATE-OT**
  (over-trigger) — plus native-verified dialect/context rows 18–26.

### Changed
- `references/decode-core.md` — §1 three-causes-of-parse-failure + context prior, §2
  `dialect` family, §3 dialect prior (incl. known-dialect-thread within-family decode and
  all-shared-tells → `variant: unknown`), §5 `translated`/`clean` statuses + the
  self-contained-but-honest translation rule, §6 two anti-patterns.
- `SKILL.md` — output contract gains `dialect`/`translated`/`clean`/`variant` and an
  explicit dialect step. The trigger `description` is **unchanged**: dialect translation
  stays an internal fallback (locale → `i18n`, single-word → `define`), not a headline.
- `README.md` — status table documents the new outcomes; credits the vendored source.

### Notes
- `src/lu.py` and the ภาษาลู cipher rule are untouched.
- Dialect recognition tells were curated to drop non-discriminating words shared with
  casual Central Thai (`ตะกี้`, `ดิ`/`แหละ`/`หว่า`, `สิ`) so clean Central text is not
  mis-tagged as dialect.

## [0.1.0] — 2026-06-19

Initial release. konthai decodes deliberately obfuscated Thai (ภาษาวิบัติ) into
standard Thai + English, honest about what it can't recover.

### Added
- **`skills/konthai/SKILL.md`** — the triggering wrapper; fires on mangled / mixed-script
  Thai, holds back on clean Thai, i18n/locale files, and single-word definitions.
- **`skills/konthai/references/decode-core.md`** — the decode procedure: per-span
  classification, the three candidate-generation biases (phonetic-first, register-aware,
  glyph-polyvalent), the five-outcome abstain taxonomy, and the ภาษาลู rule (§3.5).
- **`skills/konthai/references/eval-seed.md`** — the native-labelled calibration corpus.
- **`skills/konthai/src/lu.py`** — deterministic ภาษาลู encode/decode, with the
  consonant-cluster transform (`แปล`) derived under test and written back into §3.5.
  Decodes untrusted spans via **stdin** (shell-injection-safe; the skill is told to pipe
  spans through a quoted heredoc, never to interpolate them into a shell argument). The
  bare-`ู/ุ` rime ambiguity (e.g. `ลูดู`) is documented, not faked.
- **`scripts/check-skill-compat.py`** — Codex frontmatter + cross-manifest version-parity gate.
- **`VOICE.md`** — konthai's product voice (native-ear, street-fluent; honest over fluent).
- Brand identity set in `assets/` (avatar, icon, logo, banner).
