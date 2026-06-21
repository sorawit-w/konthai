# Changelog

All notable changes to `konthai` are documented here. Format follows
[Keep a Changelog](https://keepachangelog.com/); versioning is semver.

## [0.4.0] — 2026-06-20

RO / อักษรพิเศษ "safe slice" — name-the-cipher-and-abstain. The RO-leet family was a stub
(`partial at best`, no inventory). A community-sourced report + draft map were offered, but the
report's in-scope core (the Thai-consonant substitution map) is unreliable: its body
self-contradicts on codepoints and its own worked examples are linguistically wrong
(`ยεш = เงา` claims `ย = ng`). Activating that map as a candidate generator would lower the
abstention threshold and manufacture false-confident decodes. So konthai ships only the parts
that **cannot produce a wrong decode**: it now *names* the อักษรพิเศษ cipher and abstains
(`cipher-detected`), and recognizes/strips decorative affixes as register signal. The
substitution map ships **inactive** as a Phase-2 lead. Cardinal rule intact.

### Added
- `references/ro-leet.md` — **DRAFT, NOT native-verified** candidate inventory. Only §0 (the
  machine-verified decorative-affix strip-list) is wired in; the §1 substitution map is marked
  **inactive** (Phase-2 lead, not auto-decoded).
- `src/verify_ro_glyphs.py` — identity-only checker (codepoints + Unicode names + garbled/dup
  scan) with a `__main__` self-check. Does **not** verify usage (native-eye job, Phase 2).
- `references/eval-seed.md` rows **31–33** (⚠ inputs pending native confirmation; ground truth =
  expected *behavior*) under new **GATE-RO**: name-the-cipher-and-abstain, strip affixes as
  register, never decode from the inactive §1 map. Includes a no-over-trigger negative case and
  an affix-wrapped clean-core positive case.

### Changed
- `references/decode-core.md` — RO-leet family row (§2) reworded to **name the cipher and
  abstain** (route to `cipher-detected`), pointing at `ro-leet.md` as *background only*. New §3
  decorative-affix-strip guidance (strip verified ornaments → record as register, never as
  letters). New §6 anti-pattern: do not auto-decode an อักษรพิเศษ span from the inactive map.

### Notes
- `src/lu.py` and the ภาษาลู cipher rule are untouched.
- The §8.2 substitution map is **deliberately dormant**. Phase 2 (activating it) is gated on
  evidence it recovers real names konthai can't already read, plus native-verified fixtures and
  an explicit abstain-by-default decode gate.

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
