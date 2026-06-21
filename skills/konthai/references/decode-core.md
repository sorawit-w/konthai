# konthai — decode core

> The procedural heart of the skill. Drop this into `konthai/references/decode-core.md`
> (or inline it into the SKILL.md body). The triggering frontmatter / wrapper is a
> separate job — this file is only "how konthai decodes a span."
>
> Calibrated against a real eval set (a Facebook troll-thread of สก๊อย / ภาษาลู / RO
> comments, native-speaker labelled). Every bias and anti-pattern below fixes an
> observed failure, not a hypothetical one.

**The job:** take possibly-obfuscated Thai → recover the intended standard Thai →
translate to English → **and be honest about whatever it could not recover.**

**The cardinal rule:** never emit a confident decode you cannot stand behind. A flagged
"I can't crack this" beats a fluent lie. This was validated on real data — fluent native
speakers *also abstain* on ภาษาลู. Matching that human ceiling is success, not failure.

---

## 0. Operate per span, never per message

- Split the input into spans (roughly: words / particles / emoji-runs / number-runs).
- Each span gets its own family, decode, and confidence.
- **Message-level confidence = the weakest decoded span, never the average.** A comment
  with 28 clean spans and 2 broken ones is a *2-broken* comment, not a 93%-clean one.

---

## 1. Detection — when to even attempt a decode

Do **not** trigger on "contains non-Thai characters." That rule misses every all-Thai
cipher (ภาษาลู, คำผวน, phonetic respelling) and false-fires on loanwords, brand names,
hashtags, and URLs.

Trigger on the real signal: **the literal reading fails to parse or make sense in
context.** Treat the following only as *suspicion-raisers* (hints, not verdicts):

- mixed script welded inside a word (Latin / digit / symbol / kana glyphs in Thai)
- repeated `ล-` / `มู-` / `ลึง-` syllable patterns → possible ภาษาลู
- characters that share a physical key with Thai letters → possible keyboard-layout collision
- elongated or doubled letters, silent marks (`์ ฯ ๆ`) sprinkled in odd places
- a clean-looking phrase whose surface meaning is a non-sequitur in context → possible
  คำผวน or pun

A span is allowed to be **clean**. If the literal reading parses fine, decode nothing.
(Over-triggering — inventing obfuscation where there is none — is a real failure mode.)

**Parse-failure has three causes — classify *why* before decoding.**
1. **Obfuscation** (สก๊อย, phonetic, glyph, keyboard, ภาษาลู, RO-leet, คำผวน, slang) → decode (the existing job).
2. **Regional dialect** (Northern/คำเมือง, Southern/ภาษาใต้, Isan/อีสาน) → *not* corruption. A valid dialect word is not a broken Central word. Recognize the variant and translate (§5 `translated`); never "correct" it into Central Thai as if it were a cipher.
3. **Genuine noise / render-loss** → abstain (`no-decode` / `unreadable-encoding`).

Mixed forms exist — dialect lexicon *plus* obfuscation. Decode those, using the dialect as a candidate prior (§3).

**Situational context is an optional prior — never a verdict.** When the caller supplies, or the
surrounding chat reveals, platform / thread or reply / register / poster relationship, use it to
(a) judge whether the literal reading makes sense *here*, and (b) weight candidate ranking (§3–§4).
Context may **lower** confidence freely and **raise** it only within a span's existing family — it can
never promote `ambiguous → decoded` (flag > fabricate holds). Record context-driven ranking changes in
`notes`. A trolly-looking thread is not license to decode clean Thai.

---

## 2. Classify the span (family)

| Family | Tell | Recoverable? |
|---|---|---|
| clean | parses literally | pass through, decode nothing |
| romanized / karaoke | Thai written in Latin phonetics (`kon tai`) | yes, high |
| phonetic respell | Thai letters, casual sound-spelling (`ค้าบ`, `มั้ย`, `รึปล่าว`) | yes, high |
| glyph substitution (สก๊อย) | look-alike glyphs (`E`=ย/ี, `ll`=แ, `u`=บ, `J`=ง, `7`=จ) | yes — but maps are **context-dependent** (see Bias 3) |
| keyboard-layout collision | chars from the same physical key with the layout toggled (`ถถถถ` = `5555`) | yes — **look up the layout map; do not assume key positions** |
| ภาษาลู (Lu cipher) | syllables expanded into `ล-`/`หล-`/`ซ-` + `-ู` pairs | **fixed, invertible cipher → rule-decode** (see §3.5). Tone is the lossy part; sloppy written input can still resist clean segmentation |
| RO-leet / อักษรพิเศษ | gamer glyph-art: decorative affixes + cross-script glyph subs for Thai/Latin letters | strip decorative affixes (record as register, §3), **then look at the core: if it's clean Thai/ASCII, decode it normally; if it's glyph-soup, name the cipher and abstain** — emit `cipher-detected`, do not fabricate a reading. Background inventory (unverified, **do not auto-decode from it**): `references/ro-leet.md` |
| คำผวน (spoonerism) | swapped rime + tone across two syllables; literal reading is an odd non-sequitur | mechanically swappable, but **intent is deniable → surface, don't assert** |
| slang | a real Thai word with a non-literal current meaning (`ปัง`, `จึ้ง`, `มงลง`) | yes if known; else retrieve / flag — bounded by recency |
| dialect | a real regional variant (Northern/คำเมือง, Southern/ภาษาใต้, Isan) — valid words, **not** corruption | translate via §5 `translated`; if mixed with obfuscation, decode with the variant as a prior (§3) |

---

## 3. Candidate generation — the three calibrated biases

These three fix the actual errors konthai made on the eval set. They are not optional.

**Bias 1 — phonetic-first ordering.** Generate the plainest standard-Thai reading the
sounds and shapes point to *before* reaching for any slang or "clever" reading. Only
escalate to a slang reading if the plain one does not fit context.
> *Why:* konthai mis-read `แน่` ("for real / sure") as `แฉ` ("spill the tea") and `แถ`
> ("bullshit / deflect") — it grabbed the spicy reading first. `แน่จริง` / `แน่ใจ` are the
> plain readings and should win unless context overrules them.

**Casual Thai is written phonetically and reductively** — people type what a word *sounds
like* said aloud, and drop whatever they can to type less. So a short span may be a
**reduced content word**, not the particle it resembles. When generating candidates,
**re-inflate plausibly-dropped medial vowels** (เ‑ือ, ‑ัว, เ‑ีย, ‑ือ) and test the resulting
content word against context. Particle vs. reduced-content-word is a *ranking* question —
the particle reading is a candidate, never the automatic default.
> *Why:* konthai read `เหน่ย` as the particle เนอะ/เนี่ย when it is `เหนื่อย` ("tired") with the
> เ‑ือ nucleus collapsed (`เหนื่อย → เหน่ย`). Same early-stop pattern as the แน่-blindness above,
> now on word-class.

**Bias 2 — register-aware, do not sanitize.** In casual / troll / argument register, do
**not** down-weight crude or vulgar candidates — they are frequently the correct reading.
Decode the actual word. You may *label* the register; never *soften* the content.
> *Why:* konthai softened `ตายห่า` into `ห่าน` ("goose"), missed `มึง` (read it as "mail"),
> and shrugged off `อมควย` entirely. Politeness bias produced decode errors. The vulgar
> word is the data.

**Bias 3 — glyphs are polyvalent.** Never lock a glyph→letter map to a fixed 1:1. The
same glyph is different letters in different words — `E` was ย in `คนไทE` but ี in `คันหี`.
Generate the plausible glyph interpretations, then let context rank them. Do not commit to
the first mapping you find.

**Dialect prior.** When the span is — or context says it is — Northern / Southern / Isan, draw
candidates from *that variant's* lexicon (`references/thai-dialects.md`) before reaching for the
nearest Central word. Without the prior, Bias 1 confidently picks a wrong Central homophone: Southern
`หรอย` (delicious) mis-read as `ลอย` (float). The variant is the prior that makes the plain reading
correct.

When a span's dialect tells are *all* shared across variants (e.g. `บ่`, `แม่น` in both Isan and
Lanna), set `variant: unknown` rather than leaning to a named variant with a caveat — the gloss can be
confident while the variant stays honestly unpinned. Name a variant only when a variant-specific tell
is present.

A *known-dialect thread* is itself a classification: it makes the span `family: dialect`, so resolving
a Central-looking homophone toward the dialect lexicon — a Southern thread reading `ลอย` as `หรอย`
(delicious) — is a *within-family* decode. Emit `decoded` with the `variant` at **capped (medium)**
confidence for the residual ambiguity, not `ambiguous`. This is narrow: only an actual dialect signal
reclassifies the span. A merely trolly or heated thread is **not** a dialect and never licenses
decoding clean Central text (§1) — that path stays blocked.

For each suspect span: produce 1–3 candidate standard-Thai readings, each carrying its
reasoning (which glyph / sound / cipher step maps to which letters).

**Whole-span exclamation check — read the unit before splitting.** For 2–3 syllable
interjection-shaped spans, match the **full surface** against the fixed exclamation inventory
*before* splitting into token + elongation. A whole-form match beats a greedy leading-token
match. Because casual Thai writes exclamations the way they sound aloud, one exclamation has
several surface spellings — key the inventory by sound and list the variants.
> Inventory (extend as observed): `โอ้โห` / `อ้อหอ` / `อู้หู` ("wow / geez"), `โห`, `โหย`, `เฮ้ย`,
> `เห้อ`, `ว้าย`, `อุ๊ย`, `แหม`, `เชอะ`.
> *Why:* konthai locked on the literal first token `อ้อ` ("oh I see") and lost `อ้อหอ` = `โอ้โห`.
> Read the unit, not the prefix.

**Strip decorative affixes first (RO / อักษรพิเศษ).** Gamer glyph-art names wrap a core
in ornamental affixes — `๖ۣۜ` (flame prefix), `꧁ … ꧂` (frame brackets), `༒`, `†`,
`ﾂ`/`ツ`/`シ`, `★ ☆ ✦ ✧ ♡ ⚡ ❄ ☽ ✿`. These carry **status/aesthetic signal, never
phonetic content.** Identify and **strip** them from the span before decoding the core,
and record the affix only as a **register/identity note** ("SEA-gamer status marker") —
**never decode an affix as a letter.** The verified affix inventory + codepoints live in
`references/ro-leet.md §0`. Stripping a verified ornament cannot fabricate a reading; a
missed ornament just degrades to the same abstain. After stripping: if the core is clean
Thai/ASCII, decode it normally; if the core is glyph-soup, name the cipher and abstain
(`cipher-detected`) — the `ro-leet.md §1` substitution map is **inactive**, do not
auto-decode from it (see §6).

---

## 3.5 Rule-layer ciphers — ภาษาลู (deterministic)

ภาษาลู is **not** an abstain case — it has a fixed, invertible rule. Each spoken syllable
(initial **C** + rime **R**, where R = vowel + final) expands into a pair:

1. **ล-syllable** = `ล` + **R** — initial swapped to `ล`, rime kept.
   High/rising tones surface as `หล`; an original `ล`/`ร` swaps to `ซ` to avoid collision.
2. **อู-syllable** = **C** + `อู`/`อุ` — original initial kept, vowel forced to อู.

**To decode:** pair the syllables → take the rime from the ล-syllable and the initial from
the อู-syllable → recombine as `C + R`. Tone is recovered from markers/context — including
situational context when available (the lossy part).

Worked example — a real comment from the eval set:

```
เลี้ยวดู·ลึงมู·เลอจู   →  เดี๋ยว · มึง · เจอ
ลาภู·ลาษู·ลู          →  ภาษา · ลู
ลึงมู·ละจุ·ลงงู        →  มึง · จะ · งง
```

→ **`เดี๋ยวมึงเจอภาษาลู มึงจะงง`** = "soon you'll run into Lu language — you'll be lost."
(It literally predicted the translator's failure.)

**Caveat:** a fixed rule makes it *decodable*, not *always clean*. Dropped tone marks,
casual/sloppy encoding, and ambiguous syllable segmentation still lower confidence —
sometimes far enough that a fluent native abstains. Apply the rule, then keep the
confidence honest.

**Consonant clusters — the transform (derived & locked).** When the original initial is a
true cluster (`ปล`, `กร`, …), the ล-syllable keeps only the substituted `ล` + the *bare*
rime, and the **full cluster** lives in the อู-syllable. Real case: `แปล` → ล-syllable `แล`
(rime = leading vowel `แ`, no final) + อู-syllable `ปลู` (`ปล` + อู) = `แลปลู`. Decode in two
general steps:
1. When splitting the consonant run that sits before a `ู/ุ`, the อู-initial is the **last
   two** consonants if they form a valid Thai onset cluster (`ปล`, `กร`, …), else the last
   single consonant; anything before is the ล-syllable's finals.
2. Strip the ล-syllable's substituted initial (`ล`/`ซ`/`ห`-digraph) but **keep its leading
   vowel**, then place the recovered initial — the whole cluster — immediately after that
   leading vowel: `แ` + `ปล` → `แปล`. The naive one-consonant rule wrongly yields `แลป`.

Verified by `decode("แลปลู") → แปล` in `../src/lu.py` (test `skills/konthai/tests/test_lu.py`).
Tone stays lossy. (The same robustness drops *spurious* finals leaked by sloppy อู-syllables —
e.g. `หนุย`, `ลูง` — using the invariant that every ล-syllable initial is `ล`/`ซ`/`ห`-digraph.)

**Decode ambiguity — bare `ู/ุ` rimes (a genuine limit, not full determinism).** A syllable
whose rime is a *bare* `ู`/`ุ` (`ดู`, `หมู`, `ครู`) encodes to a ล-syllable that itself ends in
`ู` — `ดู` → `ลู`+`ดู` = `ลูดู`. That `ู` looks like an อู-terminator, *and* `ลู` is also the
literal word "ลู" (as in ภาษา·ลู). So `ลูดู` genuinely means **either** `ดู` (one pair) **or**
the literal "ลู"+"ดู" — the rule cannot disambiguate. Per **flag > fabricate**, the codec takes
the conservative reading (a terminal `ลู`/`ลุ` with no remaining อู-partner is the literal word,
passed through; this is what keeps ภาษาลู itself decoding right), and the skill surfaces such a
span as `ambiguous` / lower confidence rather than asserting a guess. ภาษาลู is a fixed rule for
the general case; this narrow class is a documented ambiguity.

---

## 4. Score & decide (confidence)

- Rank candidates by fit with the surrounding context (semantic plausibility — the LLM's
  natural strength).
- Estimate confidence from **stability**, not self-reported vibe: sample the decode a few
  times (k ≈ 5, moderate temperature) and read the agreement.
  - clean winner → high confidence
  - near-even split → `ambiguous` (Section 5)
  - scatter → low confidence
- Cluster the votes on the **decoded standard-Thai form**, not the full output string
  (otherwise cosmetic wording differences fake a disagreement).
- Anchor the raw numbers against a labelled set before trusting any threshold.
- Context and dialect are priors bound by the same floor: they may lower confidence freely and
  raise it only *within* a span's existing family. A prior never converts `ambiguous → decoded`.

---

## 5. Output — the abstain taxonomy (be precise about *why* you stopped)

Each span resolves to exactly one status. These distinctions were learned from real data;
collapsing them is itself an error.

| Status | When | What to emit |
|---|---|---|
| `clean` | the span parses literally as standard Thai — nothing to decode (pairs with `family: clean`) | the text unchanged + English; context may color the *sense* in `notes` but must not invent a non-clean reading. If a whole message is clean, prefer not firing (SKILL.md "When NOT to fire") |
| `decoded` | one reading clearly wins | standard Thai + English + high confidence |
| `ambiguous` | 2+ readings genuinely compete (incl. คำผวน intent) | **surface all** readings, English for each, note "intent unclear" — never pick silently |
| `cipher-detected` | a cipher family identified but you genuinely lack the rule/key — **not** ภาษาลู (that has a known rule, §3.5) | name the cipher, give a partial *only if labelled as partial*, **do not fabricate** a full translation |
| `unreadable-encoding` | the bytes / glyphs did not arrive intact (font-fallback boxes `□▱`) | say "characters didn't render / can't read the encoding" — this is **not** noise and **not** a failed decode |
| `no-decode` | genuine noise, no plausible reading exists | say so plainly |
| `translated` | a clean regional-dialect span (no obfuscation) | recovered Central Thai in `decoded_th` + English + `variant` (`th-lanna`/`th-south`/`th-isan`/`unknown`); **cap confidence and flag the word** when it falls outside the vendored reference; provenance in `notes` |

**Self-contained dialect translation (clean dialect).** Recognize the variant and translate with the
vendored `references/thai-dialects.md` — konthai owns this, no sibling skill required. The cardinal
rule still governs: the reference covers common cases, not every word, so when a span uses dialect
vocabulary *beyond* the vendored notes, cap confidence and flag the unverifiable word. A flagged
unknown beats a fluent wrong gloss — this lane is the easiest place to start bluffing; hold the line.

`cipher-detected`, `unreadable-encoding`, and `no-decode` are three different outcomes.
konthai once called `แปลกไหมครับ` and `ไม่มีทาง` "noise" — when they were perfectly
decodable and the glyphs simply hadn't rendered on its side. "I can't see these bytes" ≠
"I can't crack this cipher" ≠ "there's no decode here."

---

## 6. Anti-patterns (the failure-first checklist)

- Trigger on "has foreign characters." → Trigger on "the literal reading makes no sense."
- Reach for the slang / clever reading first. → Try the plain phonetic reading first.
- Soften vulgar words. → Decode them; label register if useful.
- Lock a glyph→letter map. → Treat glyphs as context-dependent.
- Average confidence across a message. → Report the weakest span.
- Call anything you can't decode "noise." → Distinguish cipher / unreadable / genuine-noise.
- Abstain on a cipher that has a known rule (e.g. ภาษาลู) because it looks scary. → Apply the rule (§3.5); abstain only for genuinely unkeyed ciphers.
- Treat a dialect as a cipher to "fix." → Recognize the variant; translate (§5 `translated`). A living dialect is not broken Central Thai.
- Bluff a dialect translation you only half-know (esp. words beyond `thai-dialects.md`). → Cap confidence; flag the unverifiable word.
- Auto-decode an อักษรพิเศษ / RO span from the `ro-leet.md` substitution map. → That map is unverified and inactive; strip the decorative affixes, then name the cipher and abstain (`cipher-detected`) until native-checked fixtures exist.
