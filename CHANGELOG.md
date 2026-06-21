# Changelog

All notable changes to `konthai` are documented here. Format follows
[Keep a Changelog](https://keepachangelog.com/); versioning is semver.

## [0.3.0] — 2026-06-20

Casual-reduction decoding. Casual Thai is written phonetically and reductively — people type
what a word *sounds like* said aloud and drop whatever they can to type less — so a short,
particle-shaped span is often a reduced content word, and one exclamation has many surface
spellings. konthai now re-inflates dropped vowels and reads exclamations as a whole unit. The
cardinal rule is unchanged: each recall rule is paired with a clean-control GATE-OT row so it
can't erode the over-trigger floor.

### Added
- `references/eval-seed.md` rows **27–30** (native-verified; ground truth = Kiang): the two
  confirmed casual-batch misses — `เหน่ย→เหนื่อย` (vowel-collapse) and `อ้อหอ`/`อู้หู`→`โอ้โห`
  (write-as-spoken) — plus clean-control rows `โอเค` and `เนอะ` under **GATE-OT** as the
  precision guard.

### Changed
- `references/decode-core.md` — **Bias 1** gains a casual-reduction pass: re-inflate
  plausibly-dropped medial vowels (เ‑ือ, ‑ัว, เ‑ีย, ‑ือ) so a reduced content word isn't
  mis-read as the particle it resembles. **§3** gains a whole-span exclamation check (read the
  unit before greedy-splitting) with a sound-keyed inventory listing surface variants
  (`โอ้โห` / `อ้อหอ` / `อู้หู`).
- `references/eval-seed.md` — GATE-OT extended to rows 29–30; header note documents the
  rows 27–30 casual-reduction batch.

### Notes
- `src/lu.py` and the ภาษาลู cipher rule are untouched.
- Modeled as an extension of **Bias 1** (phonetic-first), **not** a new bias — casual reduction
  *is* phonetic spelling, already in scope. The broad `โX↔Xอ` glyph-swap proposed in the source
  brief was rejected as over-broad (it would false-fire on clean `โต`/`โพ`/`โอเค`); only attested
  exclamation surface variants are encoded.

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
