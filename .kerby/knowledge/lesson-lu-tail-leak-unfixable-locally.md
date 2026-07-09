---
title: A leaked ภาษาลู final can't be locally distinguished from a literal final
type: lesson
domain: [decode-core, lu-cipher, src/lu.py]
confidence: low
created: 2026-07-08
---

## Context

ภาษาลู decoding sometimes sees a stray trailing อู-final left over from sloppy
input (e.g. `เต่า่ว` where a clean final leaked in). A fix was attempted to
strip it automatically.

## Lesson (inferred from git history — not independently verified)

Across five fix rounds in the 0.5.0 PR, a token-end leaked-final strip was
prototyped and progressively hardened, then ultimately reverted. The root
problem: the codec cannot locally distinguish a *leaked* Lu final from a
*clean literal* final, because a clean word (ถูก, สนุก, แล้ว) is structurally
identical to a genuine Lu syllable. Each guard in the fix sequence appears to
have only deferred the next corruption case rather than resolving the
ambiguity. The team settled on reverting to append-the-remainder-verbatim,
keeping ภาษาลู "documented-lossy" on sloppy input and letting the skill
surface low confidence — the honest behavior, not a fragile heuristic chasing
edge cases.

## Applies to

Any future attempt to add local disambiguation heuristics to `src/lu.py`'s
decode path for ambiguous trailing ู/ุ rimes — the same structural ambiguity
that already governs the bare-`ู`/`ุ` rime limit documented in `decode-core.md`
§3.5.

*This entry is agent-drafted from `git log` commit `698593e`'s five-round fix
history — not confirmed with the repo owner in this session.*
