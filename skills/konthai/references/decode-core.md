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
| RO-leet | gamer-origin symbol / letter soup | partial at best |
| คำผวน (spoonerism) | swapped rime + tone across two syllables; literal reading is an odd non-sequitur | mechanically swappable, but **intent is deniable → surface, don't assert** |
| slang | a real Thai word with a non-literal current meaning (`ปัง`, `จึ้ง`, `มงลง`) | yes if known; else retrieve / flag — bounded by recency |

---

## 3. Candidate generation — the three calibrated biases

These three fix the actual errors konthai made on the eval set. They are not optional.

**Bias 1 — phonetic-first ordering.** Generate the plainest standard-Thai reading the
sounds and shapes point to *before* reaching for any slang or "clever" reading. Only
escalate to a slang reading if the plain one does not fit context.
> *Why:* konthai mis-read `แน่` ("for real / sure") as `แฉ` ("spill the tea") and `แถ`
> ("bullshit / deflect") — it grabbed the spicy reading first. `แน่จริง` / `แน่ใจ` are the
> plain readings and should win unless context overrules them.

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

For each suspect span: produce 1–3 candidate standard-Thai readings, each carrying its
reasoning (which glyph / sound / cipher step maps to which letters).

---

## 3.5 Rule-layer ciphers — ภาษาลู (deterministic)

ภาษาลู is **not** an abstain case — it has a fixed, invertible rule. Each spoken syllable
(initial **C** + rime **R**, where R = vowel + final) expands into a pair:

1. **ล-syllable** = `ล` + **R** — initial swapped to `ล`, rime kept.
   High/rising tones surface as `หล`; an original `ล`/`ร` swaps to `ซ` to avoid collision.
2. **อู-syllable** = **C** + `อู`/`อุ` — original initial kept, vowel forced to อู.

**To decode:** pair the syllables → take the rime from the ล-syllable and the initial from
the อู-syllable → recombine as `C + R`. Tone is recovered from markers/context (the lossy
part).

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

---

## 5. Output — the abstain taxonomy (be precise about *why* you stopped)

Each span resolves to exactly one status. These distinctions were learned from real data;
collapsing them is itself an error.

| Status | When | What to emit |
|---|---|---|
| `decoded` | one reading clearly wins | standard Thai + English + high confidence |
| `ambiguous` | 2+ readings genuinely compete (incl. คำผวน intent) | **surface all** readings, English for each, note "intent unclear" — never pick silently |
| `cipher-detected` | a cipher family identified but you genuinely lack the rule/key — **not** ภาษาลู (that has a known rule, §3.5) | name the cipher, give a partial *only if labelled as partial*, **do not fabricate** a full translation |
| `unreadable-encoding` | the bytes / glyphs did not arrive intact (font-fallback boxes `□▱`) | say "characters didn't render / can't read the encoding" — this is **not** noise and **not** a failed decode |
| `no-decode` | genuine noise, no plausible reading exists | say so plainly |

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
