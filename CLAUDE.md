# CLAUDE.md — the `konthai` repo

`konthai` is a single-skill Claude Code plugin that decodes deliberately obfuscated Thai
(ภาษาวิบัติ) into standard Thai + English, honest about what it can't recover. The skill lives
at [`skills/konthai/`](skills/konthai/SKILL.md); the decode procedure it applies lives in
[`skills/konthai/references/decode-core.md`](skills/konthai/references/decode-core.md).

## The one rule that governs everything

**Flag > fabricate.** Never emit a confident decode you can't stand behind. The calibration
target is the fluent-human ceiling — if a native speaker would abstain cold, then abstaining
(with the cipher *named*) is success, not failure. The eval-seed labels are native-speaker
ground truth; do not "correct" them against model intuition.

## Layout

- `skills/konthai/SKILL.md` — triggering wrapper (thin) + output contract; links the references.
- `skills/konthai/references/decode-core.md` — the calibrated decode logic. **Authoritative.**
- `skills/konthai/references/eval-seed.md` — native-labelled calibration corpus (holds vulgar
  fixtures — these stay out of every README).
- `skills/konthai/src/lu.py` — deterministic ภาษาลู codec; `tests/` are its pytest fixtures.
- `VOICE.md` — the product voice (native-ear, street-fluent; honest over fluent).
- `scripts/check-skill-compat.py` — Codex frontmatter + cross-manifest version-parity gate.

## Conventions

- **README hygiene:** the skill decodes slurs/vulgar register (register is data), but the
  vulgar fixtures live only in `references/eval-seed.md`. No bad words in any README.
- **Version parity:** the release version must agree across `.claude-plugin/plugin.json`,
  `.claude-plugin/marketplace.json`, `.codex-plugin/plugin.json`, the first `## [x.y.z]` in
  `CHANGELOG.md`, and `Current release: \`x.y.z\`` in `README.md`. Run
  `python3 scripts/check-skill-compat.py` to verify.
- **Codex contract:** SKILL.md `description` ≤ 1024 characters or Codex silently skips the skill.
