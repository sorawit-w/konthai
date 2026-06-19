---
name: konthai
description: >
  Decodes obfuscated / "corrupted" Thai (ภาษาวิบัติ) into standard Thai and English
  — สก๊อย glyph substitution, phonetic respelling, karaoke-romanized Thai,
  keyboard-layout collisions, the ภาษาลู cipher, RO-leet, gen-z slang, and คำผวน.
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
4. **Don't sanitize.** In casual / troll / argument register, crude or vulgar
   readings are frequently the correct reading. Decode the actual word; you may
   *label* the register, never *soften* the content.

## Output contract (per span)

Emit, for each decoded span:

| field | meaning |
|---|---|
| `span` | the original surface text |
| `family` | clean · romanized · phonetic · glyph · keyboard · lu · ro-leet · kamphuan · slang |
| `status` | decoded · ambiguous · cipher-detected · unreadable-encoding · no-decode |
| `decoded_th` | recovered standard Thai (omit if not `decoded`) |
| `english` | English reading |
| `confidence` | your honest read — high / medium / low |
| `notes` | which glyph/sound/cipher step mapped to what; register label if useful |

- `ambiguous` → **surface ALL competing readings** with English for each; never pick
  one silently. This includes คำผวน, whose intent is deniable — surface, don't assert.
- `cipher-detected` / `unreadable-encoding` / `no-decode` are three *different*
  outcomes (a keyed cipher you lack ≠ glyphs that didn't render ≠ genuine noise).
  Never collapse them into "noise."
- Then give a short plain-language answer to what the user actually asked.

## When NOT to fire

Clean standard Thai (decode nothing — over-triggering is a real failure mode);
i18n / locale-file translation (→ `i18n`); single-word in-context definition
(→ `define`). See `references/eval-seed.md` for the native-labelled calibration set.
