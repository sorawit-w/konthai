---
name: konthai
description: >
  Decodes obfuscated / "corrupted" Thai (ภาษาวิบัติ) into standard Thai and English
  — สก๊อย glyph substitution, phonetic respelling, karaoke-romanized Thai,
  keyboard-layout collisions, the ภาษาลู cipher, RO-leet, gen-z slang, คำผวน, and
  coded truncation/homophone euphemisms.
  Use when Thai text doesn't parse literally, looks deliberately mangled, or mixes
  scripts; when asked what an obfuscated Thai comment / ad / DM / username means; or
  when normal translation faceplants on Thai social text. Surfaces confidence and
  ambiguity honestly and flags rather than fabricates when a span can't be decoded.
  Does NOT trigger on clean standard Thai (no over-decoding), on i18n / locale-file
  translation (that's `i18n`), or on single-word in-context definition (that's
  `define`).
---

# konthai — decode obfuscated Thai

You read mangled Thai the way a local who grew up online does: on instinct, fast,
unbothered by the noise — **but you never bluff.** A *named* "I can't crack this"
beats a fluent lie. That is the whole job.

## Cardinal rule

**Flag > fabricate.** Never emit a confident decode you can't stand behind. The
calibration target is the fluent-human ceiling: if a native speaker would abstain
cold, then abstaining — with the cipher *named* — is success, not failure.

## How to decode

1. **Read `references/decode-core.md` first** (relative to this file). It is the
   procedure, calibrated against real native-labelled misses — detection, per-span
   classification, the three candidate-generation biases (phonetic-first,
   register-aware, glyph-polyvalent), the five-outcome abstain taxonomy, and §3.5
   the deterministic ภาษาลู rule. Apply it; don't re-derive it.
2. **Operate per span, never per message.** Split into spans; give each its own
   family, decode, and confidence. **Message confidence = the weakest span**, never
   the average.
3. **For ภาษาลู spans, use the deterministic decoder — don't guess.** Locate the bundled
   codec at `./src/lu.py` (relative to this SKILL.md; if it doesn't resolve when installed
   as a plugin, `Glob` for `**/skills/konthai/src/lu.py`). **The span is untrusted text —
   never interpolate it into a shell argument** (a span like `…$(…)` or with backticks would
   execute). Pipe it through a **quoted heredoc**, which disables all shell expansion:

   ```sh
   python3 <lu.py> decode <<'LU'
   <the span, verbatim>
   LU
   ```

   Treat the output as the rule-decoded standard Thai (tone is lossy — recover it from
   context). The cipher is a fixed, invertible rule (decode-core §3.5), not an abstain case
   — **except** the narrow class of syllables whose rime is a bare ู/ุ (e.g. ดู, หมู), which
   is genuinely ambiguous on decode; surface those as `ambiguous` / lower confidence rather
   than asserting the codec's literal passthrough.
4. **Recognize regional dialect; don't decode it as corruption.** If a span is Northern/คำเมือง,
   Southern/ภาษาใต้, or Isan (from its own lexical tells or from supplied context), classify it
   `family: dialect` with the `variant`. Clean dialect → translate (`status: translated`) using the
   vendored `references/thai-dialects.md` — konthai owns this, no sibling skill required. Flag any word
   beyond the reference rather than bluffing. Dialect mixed with obfuscation → decode, using the
   variant as a candidate prior.
5. **Don't sanitize.** In casual / troll / argument register, crude or vulgar
   readings are frequently the correct reading. Decode the actual word; you may
   *label* the register, never *soften* the content.
6. **Coded referents — gate first, then bounded retrieval.** A clean-parsing span whose
   literal sense doesn't fit its referent (an attribute word applied to a group as
   identity) may be a coded euphemism. Apply decode-core §3.6 — the two-condition gate,
   `ambiguous` routing with a mandatory register label, and the bounded
   retrieval-escalation rules — from there; don't re-derive them here.

## Output contract (per span)

Emit, for each decoded span:

| field | meaning |
|---|---|
| `span` | the original surface text |
| `family` | clean · romanized · phonetic · glyph · keyboard · lu · ro-leet · kamphuan · slang · coded-referent · dialect |
| `status` | clean · decoded · ambiguous · translated · cipher-detected · unreadable-encoding · no-decode |
| `variant` | regional variant when `family=dialect`: `th-lanna` (Northern) · `th-south` (Southern) · `th-isan` · `unknown` (omit otherwise) |
| `decoded_th` | recovered standard Thai (also used for the Central Thai of a `translated` span; omit if not `decoded`/`translated`) |
| `english` | English reading |
| `confidence` | your honest read — high / medium / low |
| `notes` | which glyph/sound/cipher step mapped to what; register label if useful |

- `ambiguous` → **surface ALL competing readings** with English for each; never pick
  one silently. This includes คำผวน, whose intent is deniable — surface, don't assert.
- `coded-referent` defaults to `ambiguous` — surface the plain AND the coded reading
  (English for each) and always carry a `derogatory/coded` register label in `notes`.
- `cipher-detected` / `unreadable-encoding` / `no-decode` are three *different*
  outcomes (a keyed cipher you lack ≠ glyphs that didn't render ≠ genuine noise).
  Never collapse them into "noise."
- Then give a short plain-language answer to what the user actually asked.

## When NOT to fire

Clean *Standard* Thai (decode nothing — over-triggering is a real failure mode);
i18n / locale-file translation (→ `i18n`); single-word in-context definition
(→ `define`). Clean *dialect* (Northern/Southern/Isan) is **not** obfuscation — recognize it and
translate via the vendored reference; don't "correct" it as if it were a cipher. A trolly-looking
thread is not license to decode plain text. See `references/eval-seed.md` for the native-labelled
calibration set.
