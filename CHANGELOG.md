# Changelog

All notable changes to `konthai` are documented here. Format follows
[Keep a Changelog](https://keepachangelog.com/); versioning is semver.

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
- **`scripts/check-skill-compat.py`** — Codex frontmatter + cross-manifest version-parity gate.
- **`VOICE.md`** — konthai's product voice (native-ear, street-fluent; honest over fluent).
- Brand identity set in `assets/` (avatar, icon, logo, banner).
