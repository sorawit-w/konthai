---
title: Why the RO-leet substitution map ships inactive
type: decision
domain: [decode-core, ro-leet, calibration]
confidence: low
created: 2026-07-08
---

## Context

The RO-leet (อักษรพิเศษ) family in `decode-core.md` names two mechanisms: a
decorative-affix strip-list (§0) and a Thai-consonant substitution map (§1).
Only §0 is wired into decoding; §1 ships inactive.

## Decision (inferred from git history — not independently verified)

The 0.4.0 commit message states that a community-sourced substitution map was
offered as a candidate generator, but its body self-contradicted on codepoints
and its own worked examples were linguistically wrong (e.g. claiming ย = "ng").
Activating that map would have lowered the abstention threshold and
manufactured false-confident decodes — a direct violation of the flag >
fabricate cardinal rule. So only the parts that *cannot* produce a wrong
decode shipped: the affix-strip logic. The substitution map stays dormant,
documented as a Phase-2 lead pending native-verified fixtures.

## Revisit When

Native-verified fixtures exist for the substitution map, and there's evidence
it recovers names konthai can't already read via other paths.

*This entry is agent-drafted from `git log` commit `f0a7c23` and
`references/ro-leet.md`'s own §1 "inactive" marking — not confirmed with the
repo owner in this session.*
