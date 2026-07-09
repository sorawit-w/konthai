---
title: Casual Central Thai particles keep masquerading as dialect tells
type: lesson
domain: [decode-core, dialect, thai-dialects]
confidence: low
created: 2026-07-08
---

## Context

`thai-dialects.md` lists recognition tells per regional variant
(th-south, th-isan, th-lanna) used to classify a span as dialect rather than
Standard Thai, then translate it.

## Lesson (inferred from git history — not independently verified)

Git history from the 0.2.0 dialect PR shows a recurring failure pattern
surfacing across several Codex review rounds: candidate dialect tells kept
turning out to *also* occur in ordinary casual Central Thai. Examples: ดิ /
แหละ / หว่า proposed as th-south tells, สิ as a th-isan future-marker tell, and
ตะกี้ as a th-lanna tell — each collides with common Central usage (ไปดิ,
นั่นแหละ, ไปสิ as an imperative, เมื่อกี้/เมื่อตะกี้). Left as primary tells, each
would have mistagged clean Central text as regional dialect and triggered an
unwanted "translation" — the fabrication-on-clean-text failure mode the
project's calibration work explicitly guards against (GATE-OT). Each was
demoted to secondary/corroborating-only (fires only alongside a genuine
primary marker) or dropped outright.

## Applies to

Adding any new dialect-recognition tell to `thai-dialects.md` — check the
candidate against casual/colloquial Central Thai usage, not just against the
target dialect, before promoting it to a primary (standalone-sufficient) tell.

*This entry is agent-drafted from `git log` commit `18271ff`'s review-round
history — not confirmed with the repo owner in this session.*
