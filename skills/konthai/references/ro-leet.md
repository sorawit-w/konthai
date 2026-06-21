# ro-leet — RO / อักษรพิเศษ glyph decoding (data reference)

> Pointed to from `decode-core.md` §2, family row **RO-leet**. This is a **Phase-2
> candidate inventory, not an active codec — and NOT wired into the decoder today.**
> Do **not** generate readings from this file: an RO / อักษรพิเศษ span is named and
> abstained (`cipher-detected`) per `decode-core.md`. *When/if §1 is activated in
> Phase 2*, it will obey **Bias 3 (polyvalence)** — a glyph maps to a *set* of possible
> letters; generate plausible readings, then let context rank them. The **cardinal
> rule** governs throughout: a flagged span you can't stand behind beats a confident
> wrong decode.

> **⚠️ WIRING STATUS — the §1 substitution map is INACTIVE.** Only §0 (the
> machine-verified decorative-affix strip-list) is used by the decoder today. The §1
> Thai-consonant substitution map is **not** wired in as a candidate generator — it is
> a Phase 2 lead, present here for reference, **not** for auto-decoding. Per
> `decode-core.md`, an RO / อักษรพิเศษ span is named as a cipher and **abstained on**
> (`cipher-detected`) until native-verified fixtures exist. Do not decode from §1.

## Status of this file

**DRAFT — NOT native-verified.** Extracted from a community-sourced report
(Perplexity). Glyph *identity* (codepoints, names) is machine-verified; glyph *usage*
(is this substitute actually used in thRO?) is **not** — that needs a native eye.
Rows are tiered:

- **[solid]** — Lao near-homoglyph or an established สก๊อย/Greek/Cyrillic homoglyph,
  and consistent with the source's own worked examples. Trust with normal Bias-3 caution.
- **[verify]** — plausible visual resemblance, but exotic-script and usage-unconfirmed.
  Confirm it appears in real names before relying on it.
- **[contested]** — the source contradicts itself, the cell is garbled, or the
  resemblance is a stretch. **Do not trust until native-checked.**

The source mislabeled multiple codepoints (its `๖ۣۜ` decode, the `꧁꧂` brackets, and
`ℜ` were all wrong). Treat every unverified claim in it as a lead, not a fact.

---

## 0. Strip decorative affixes FIRST

These carry **status / aesthetic signal, never phonetic content.** Strip them before
decoding the core; record the signal in `notes` if useful, never decode them as letters.
Codepoints below are machine-verified.

| Affix | Codepoint(s) | Verified name | Role |
|---|---|---|---|
| `๖ۣۜ` | U+0E56 + U+06E3 + U+06DC | THAI DIGIT SIX + ARABIC SMALL LOW SEEN + ARABIC SMALL HIGH SEEN | "flame/crown" prefix — SEA-gamer status marker |
| `ﾂ` | U+FF82 | HALFWIDTH KATAKANA LETTER TU | "cool/chill" suffix (detached from Japanese ツ smile) |
| `ツ` | U+30C4 | KATAKANA LETTER TU | smile/chill suffix |
| `シ` | U+30B7 | KATAKANA LETTER SI | cool/smile suffix |
| `꧁ … ꧂` | U+A9C1 / U+A9C2 | JAVANESE LEFT/RIGHT RERENGGAN | ornamental frame brackets (source wrongly called these "Cham") |
| `༒` | U+0F12 | TIBETAN MARK RGYA GRAM SHAD | inner-frame ornament |
| `†` | U+2020 | DAGGER | "dark/evil" aesthetic framing (often read as a cross) |
| `★ ☆ ✦ ✧ ♡ ⚡ ❄ ☽ ✿` | U+2605, U+2606, U+2726, U+2727, U+2661, U+26A1, U+2744, U+263D, U+273F | (Misc Symbols / Dingbats) | prefix/suffix ornament — VIP/cute/element flavor |

**Rule:** affixes are noise for the decoder. Strip → decode the core glyphs → re-attach
the affix only as a register/identity note.

---

## 1. Thai-consonant substitution candidates (ก–ฮ)

> **INACTIVE — Phase 2 lead, not wired in.** See the wiring-status banner at the top of
> this file. Do not generate decode candidates from this table; an RO / อักษรพิเศษ span
> is named-and-abstained (`cipher-detected`) until this map is native-verified.

Each Thai consonant → a **set** of glyphs players use to stand in for it. Read a cell as
"any of these *might* be this consonant in *some* word." Rank by which reading yields a
real Thai name/word in context.

| Thai | RTGS | Candidate substitutes | Tier |
|---|---|---|---|
| ก | k/g | ∩ ∏ Ω Ռ ח ν υ п л π / ந ர ମ | [solid] for ∩ п π · [verify] exotic |
| ข | kh | ∫ ရ ျ থ श ४ ဈ ૪ ឧ খ | [verify] |
| ค | kh | の ମ め ꢍ | [solid] の · [verify] rest |
| ง | ng | ງ σ / פ ஜ এ ق ঐ ও ঞ ଏ ၅ ل ७ | [solid] ງ σ(final) · [verify] rest |
| จ | j/ch | ຈ / す ब ন ল ম अ ज न ㅋ व | [solid] ຈ · [verify] rest |
| ช | ch | જ Ճ ಶ ឋ | [verify] |
| ญ | y | ₪ വ ഖ ល ស ภ | [verify] (source had a duplicate `ល`, deduped) |
| ณ/น | n | Њ њ Ю ю / Ա थ ゆ થ य ਪ ឍ ભ | [verify] |
| ด | d | ດ ๑ ໑ / இ ஏ ஞ ௭ ெ | [solid] ດ ๑ · [verify] rest |
| ต | t | ๓ ຕ / რ დ ព တ ო ~~ถ~~ | [solid] ຕ · [contested] ถ (a real Thai consonant) |
| ท | th | η ທ Ŋ ŋ и מ | [solid] ທ η · [verify] rest · **dropped garbled cell `មមហ`** |
| ธ | th | ຣ ຽ চ ន | [verify] |
| บ | b | ບ υ / ப ひ び | [solid] ບ · [verify] rest |
| ป | p | ປ √ ច | [solid] ປ · [verify] √ ច |
| ผ | ph | ຜ / ಛ ಟ ය చ ట | [solid] ຜ · [verify] rest |
| ฝ | f | ຝ / ධ ඨ យ | [solid] ຝ · [verify] rest |
| พ | ph | ພ ш / ಬ ധ ਘ ဃ ឃ | [solid] ພ · [contested] `ш` (see §3) |
| ภ | ph | ຟ / ௰ ಚ ಭ ඩ | [verify] |
| ม | m | ມ / ஆ ௮ ঋ भ ಖ | [solid] ມ · [verify] rest |
| ย | y | ε є ຢ / ξ ઈ ع ধ ㄠ ঘ | [solid] ε ຢ · [verify] rest |
| ร | r | ی र ਙ હ វ よ / ~~ຮ~~ / ~~丂~~ | [verify] · [contested] ຮ, 丂 (see §3) |
| ล | l | ລ / त ਫ਼ බ ढ द ट | [solid] ລ · [verify] rest |
| ว | w | ວ / ಞ Ձ | [solid] ວ · [verify] rest |
| ส | s | ສ / さ ざ द ನ న ឥ ৯ స | [solid] ສ · [verify] rest |
| ห | h | ຫ / × Ҩ ண യ භ ӄ ﾒ א ㄨ ม | [solid] ຫ · [contested] "ม as ห" (junk) |
| อ | (vowel carrier) | Ο о Ө ө ∂ / Ә ਹ ට ბ ס ծ | [solid] Ο о Ө · [verify] rest |
| ฮ | h | ອ ར | [verify] |

> The Lao single-glyph subs (ດ ຕ ບ ປ ຜ ຝ ພ ມ ລ ວ ສ ຫ ງ ຈ ທ …) are the backbone —
> Lao and Thai share Brahmic ancestry, so the shapes are near-identical and these are
> the safest bets. The Greek/Cyrillic homoglyphs (ε=ย, σ=ง-final, Ο/о=อ, η=ท, ш=พ-ish)
> are the next most reliable. The Devanagari/Bengali/Tamil/Burmese/Hangul cells are
> visually *plausible* but need a native eye to confirm they're in real use.

---

## 2. Reading rules

1. **Script signals the language.** Superscript / small-caps Latin (`ᵐⁱⁿᵗ`, `ᴅᴀʀᴋ`) =
   an English word written cute — read it as English. Thai-consonant glyph subs =
   read it as Thai. Which system is active is usually obvious from which glyphs appear.
2. **Tone marks are dropped for aesthetics.** Default to the natural reading of the
   underlying word; recover tone from context. For common names (ดาว, น้ำ, ฟ้า) the
   tone is known; don't over-think it.
3. **Decode per syllable, rank by realness.** A candidate set is only "decoded" when one
   reading lands on a real Thai name/word. If two land (e.g. กิน vs คิม), that's
   `ambiguous` → surface both, per the output contract. If none land, `no-decode` — flag it.

---

## 3. Flagged for native verification (resolve before trusting)

- **`ш` → พ vs ว.** §8.2 lists `ш` under **พ**; §8.6 reads `ยεш` as **เงา** (ш = **ว**).
  Pick one or mark `ш` explicitly polyvalent. Visually `ш` favors the พ/ฟ/ผ family.
- **`丂` → ร vs ส.** §8.2 lists `丂` under **ร**; the §8.7 example `丂อα∩สε` = **แสงสาย**
  reads `丂` as **ส**. Genuinely polyvalent or an error — confirm.
- **`ຮ` → ร.** Lao HO listed as a ร sub; shapes don't obviously match. Verify.
- **`ถ` → ต.** A real Thai consonant listed as a glyph sub for another — suspicious.
- **`ม` → ห ("approx").** Source's own example calls this approximate; ม and ห don't
  resemble each other. Likely junk — probably delete.
- **Garbled/dup cells already cleaned:** dropped `មមហ` from ท, deduped `ល` in ญ.
  Double-check nothing meaningful was lost.

---

## Appendix — provenance

Codepoints in §0 and the tier notes were generated/verified by `verify_ro_glyphs.py`
(in `../src/`). Re-run it after pruning to pin codepoints on the survivors.
