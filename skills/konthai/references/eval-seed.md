# konthai — eval seed set

> The labelled corpus the decode-core was calibrated against. **Ground truth = native
> speaker (Kiang).** Source = a Facebook troll-thread where Thai users flooded a newly
> Thai-capable auto-translator with สก๊อย / ภาษาลู / RO / phonetic obfuscation.
>
> Small and *deliberately weighted to the hard classes* — this is a stress set, not a
> representative sample. The point of an eval is the misses, so the hard rows earn their
> place. Expand later toward whatever konthai will see in production.
>
> `konthai verdict` records how the **un-tuned** model did, before the decode-core biases
> were written. That column is the "before" picture; re-running with the core applied is
> the next measurement.
>
> Rows **18–26** are net-new dialect/context rows (native-verified; ground truth = Kiang; row 26 is a
> synthetic coverage seed pending native confirmation; not
> from the source thread). They have no pre-core verdict — their last cell records the
> **expected behavior + gate** instead. Gates + metrics are defined in *Dialect & context* below.
>
> Rows **27–30** are the casual-reduction batch (native-verified; ground truth = Kiang). 27–28 are the
> two confirmed misses — `เหน่ย→เหนื่อย` (vowel-collapse) and `อ้อหอ/อู้หู→โอ้โห` (write-as-spoken). 29–30
> are clean-control rows: the precision guard so the new recall fixes don't erode the over-trigger floor.
>
> Rows **31–33** are the RO / อักษรพิเศษ safe-slice seed (native-confirmed; ground truth = Kiang).
> 31 is the gold-standard abstain (`ยεшηᴅᴀʀᴋ` — unreadable even to a fluent native); 32 strips affixes
> off a non-Thai Latin core ("Ragnarok"); 33 strips a frame off a clean Thai core (`ดาว`). They lock
> the safe-slice behavior: name-the-cipher-and-abstain, strip decorative affixes as register, and
> **never** decode from the inactive `ro-leet.md §1` map. Scored by **GATE-RO** below.
>
> Rows **34–35** are the keyboard-collision seed (native-verified; ground truth = Kiang). 34 is
> Thai-on-QWERTY (`mflv[`→`ทดสอบ`); 35 is the reverse, English-on-Thai-layout (`้ำสสน`→`hello`).
> They lock decode-*from-the-table* (`references/keyboard-kedmanee.md`), both directions. Scored by
> **GATE-KB** below.
>
> Rows **36–40** are the coded-referent seed (⚠ **all constructed** — invented targets
> demonstrating the truncation-to-homophone mechanism per D6; **zero real coded slurs**;
> pending Kiang's native confirmation of naturalness). 36–37 are the positive collisions
> (must route `ambiguous` + register label); 38–40 are the precision guard (literal
> attribute use · clean loanword · back-formation loanword — must stay `clean`).
> Scored by **GATE-CR** below.
>
> **Non-eval source — the deep-research report** (`thai_machine_unreadable_text_report.md`, *"100
> Tough Sample Phrases"*) is a **test-target inventory only, NOT ground truth.** ~half its rows are
> self-labelled "Illustrative" (constructed); several reverse-keyboard rows have internally
> inconsistent gold (#58 `สรรา` should be `สนนา` for "look"; #59/#61/#62 imply `r`=ไ when ไ=`w`); rows
> #6/#7 cite satirical Uncyclopedia. **Never bulk-import it.** Only individually native-verified rows
> graduate here (rows 34–35 are the first two). Candidates pending native confirmation, harvest later:
> the *Attested* phonetic/karaoke/Lu rows (e.g. `gin khao yang?`, `ป่าว`, the Wongnai ภาษาลู set —
> after a native check that each was transcribed faithfully).

## Labelled rows

| # | Original | Family | Ground truth → English | konthai verdict (pre-core) |
|---|---|---|---|---|
| 1 | `Yar tar tai kon tai harharhar` | romanized / karaoke | อย่าท้าทายคนไทย 555 → "don't challenge Thais, haha" | **hit** |
| 2 | `คนไทE บิ€ไก่ฟ ถถถถ` | glyph (E=ย) + keyboard-collision (ถ=5) | ขอพูดเลยว่าคนไทยบิดเก่ง 5555 → "gotta say, Thais are great at *twisting* [words]" (`บิด`=twist, self-referential pun) | **flagged-partial** — got คนไทย, correctly flagged the middle word uncertain, missed the บิด pun; knew ถถถถ≈laughing but not the keyboard mechanism |
| 3 | `ไตแน้ว เคร้าจาโร้วล้าวว่าฟ์เลานีนธาอาพ้ัยส` | phonetic + glyph distortion | ตายแล้ว เค้าจะรู้แล้วว่าเรานินทาอะไร → "oh no, they'll find out what we were gossiping about" | **partial** — first half ok, missed the tail (นินทา) |
| 4 | `หั้นหEEEE` | glyph (**E=ี**, polyvalent) | คันหี → [vulgar: "itch" + genital slur] | **flag, miss** — correctly didn't fake it; taught us `E` = ี here vs ย in #2 |
| 5 | `เทอแฉเจิงเบอ เค่าจัยเลาจึงๆ อ๊ะป๋าวอ่า` | phonetic respell | เธอแน่จริงหรอ เข้าใจเราจริงๆ รึปล่าวอ่า → "you're really that good? you really get us, or not?" | **right confidence, wrong candidates** — surfaced two readings, both missed `แน่`. *Context-sensitive:* argument/gossip-thread context should flip the ranking toward `แน่`; without context, abstain is correct. |
| 6 | `llนใ7xso?` | glyph (ll=แ, 7=จ, x=ห, s=ร, o=อ) | แน่ใจหรอ? → "are you sure?" | **hit** — got meaning, honestly flagged glyph maps |
| 7 | `ไหลหนุยซองลูงแลปลูลันอุนลี้นู้ลิซุ` | **ภาษาลู** | ไหนลองแปลอันนี้ซิ → "go on, try translating *this* one" | **abstain → now solved** by the §3.5 rule |
| 8 | `เลี้ยวดูลึงมูเลอจู ลาภูลาษูลู ลึงมูละจุลงงู` | **ภาษาลู** | เดี๋ยวมึงเจอภาษาลู มึงจะงง → "soon you'll hit Lu language, you'll be lost" | **abstain → now solved** by the §3.5 rule |
| 9 | `ภี่ร์ๆไป์ปร์แกล้งเค้าตะหม้าญ` | glyph + silent-mark (`์`) noise | พี่ๆไปแกล้งเค้าทำไม → "bros, why go tease them?" | **hit** (close) |
| 10 | `แถจัยฤ` | phonetic (ฤ=หรือ) | แน่ใจหรือ → "are you sure?" | **miss** — read `แถ` (bullshit) for `แน่`; the แน่-blindness pattern. *Context-sensitive:* argument-thread context should flip the ranking toward `แน่`. |
| 11 | `เดี๋ยวเมิ้ลเจอลูเน่` | phonetic | เดี๋ยวมึงเจอแน่ → "you'll get it soon" (threat; มึง vulgar) | **miss** — read `เมล`/"mail" for `มึง` |
| 12 | `คนไทยรักสปบ แตถ่ีรบ ไม่ขลาด` | glyph (J=ง, สปบ→สงบ) + cultural ref | อย่าไปยอมมัน คนไทยรักสงบ แต่ถึงรบไม่ขลาด → "don't give in; Thais love peace but when it's time to fight we don't flinch" (slogan parody) | **hit** (high conf, recognized the parody) |
| 13 | `โอ๊ยฯฯหฯ่านแน้ว ก็ไปแกล้งเขา` | silent-mark (`ฯ`) noise + register | โอ๊ยตายห่าแล้ว ก็ไปแกล้งเขา → "ugh, damn, you went and teased them" (`ตายห่า` strong oath) | **miss** — softened `ตายห่า` to `ห่าน`/"goose" |
| 14 | `llบบนี้\|\|ป□▱n૮หมดครับ` | glyph (□▱ = render-loss, not noise) | แบบนี้แปลกไหมครับ → "is this weird, krap?" | **miss** — called it "noise"; was decodable, glyphs just didn't render |
| 15 | `มี้Eศกทๅง` | glyph | ไม่มีทาง → "no way" | **miss** — called it "noise" |
| 16 | `Oみのつも` | mixed-script | อมควย → [crude sexual insult] | **miss** — dismissed as "user just goblin-ing" |
| 17 | `เชี่ยไรวะเนี่ย` | phonetic (เชี่ย = softened เหี้ย) | เหี้ยอะไรวะเนี่ย → "[expletive] what is this" | (user's own line; register note) |
| 18 | `เปิ้นกิ๋นข้าวแล้วกา` | dialect / th-lanna (clean) | เขากินข้าวแล้วหรือ → "has he eaten yet?" | **(new)** expect `translated`, `variant=th-lanna`. **GATE-FD:** must NOT be flagged as obfuscation. |
| 19 | `หรอยจังหู้` | dialect / th-south (clean) | อร่อยมากเลย → "so delicious" | **(new)** expect `translated`, `th-south`. **GATE-FD.** |
| 20 | `แซบหลายเด้อ` | dialect / th-isan (clean) | อร่อยมาก → "really tasty" | **(new)** expect `translated`, `th-isan`. **GATE-FD.** |
| 21 | `ลอย` (thread known Southern) | dialect prior + phonetic (mixed) | หรอย → "delicious" | **(new)** expect `decoded`, `th-south` prior beats Central `ลอย`("float"); tone lossy → **medium** conf. |
| 22 | `บ่แม่น` | dialect / attribution-trap (Isan↔Lanna shared) | ไม่ใช่ → "no / that's not right" | **(new) GATE-ATTR:** บ่ + แม่น are shared by Isan and Northern → `variant` must be `unknown` (or flag the ambiguity), NOT a confident pick. The `#4`-analogue for dialect. |
| 23 | `ทำหลาวหม้าย` | dialect / th-south, beyond-reference | ทำอีกไหม → "are you doing it again? / will you do it again?" (probe word: `หลาว`=อีก/อีกแล้ว) | **(new) GATE-BR:** recognize th-south from the **in-reference** tell `หม้าย` (≈ไหม), then **flag/cap `หลาว`** (kept out of `thai-dialects.md`) — must NOT bluff Central `หลาว` ("stake / sharpen"). Variant comes from the referenced particle, not from knowing `หลาว`. |
| 24 | `อย่าถอกน้ำเด้อ` | dialect / th-isan, beyond-reference | อย่าเทน้ำนะ → "don't pour out the water" (probe word: `ถอก`=เท) | **(new) GATE-BR:** recognize th-isan, **flag/cap `ถอก`** (kept out of `thai-dialects.md`) — must NOT bluff Central `ถอก` ("strip / peel / retract"). |
| 25 | `แน่` (argument thread) | clean Standard Thai + situational context | แน่ → "sure / for real" (no decode) | **(new) GATE-OT (over-trigger):** `แน่` is already clean — emit `status: clean` (pass through unchanged). A heated thread is **not** license to decode clean text (decode-core §1); context may color the *sense* in `notes` but must NOT promote it to a non-clean reading (`decoded`/`translated`/cipher). The fabrication-side complement to #5/#10. |
| 26 | `หรอE` (thread known Southern) | dialect + glyph (mixed) | หรอย → อร่อย → "delicious" (glyph `E`=ย) | **(new) ⚠ synthetic** (machine-composed from verified parts — `หรอย`=delicious th-south + `E`=ย glyph from #2/#4; Kiang to confirm/replace). Mixed path: decode the glyph **and** apply the th-south prior → `decoded`, `variant=th-south`, medium conf. Tests "dialect + obfuscation → decoded with variant prior." |
| 27 | `เหน่ย` | phonetic / vowel-collapse | เหนื่อย → "tired" | **(new)** expect `decoded` via Bias-1 vowel re-inflation (`เ‑ือ` nucleus restored); must NOT settle for the particle เนอะ/เนี่ย. Word-class-downgrade trap. |
| 28 | `อ้อหอ` (also `อู้หู`) | phonetic / write-as-spoken | โอ้โห → "wow / geez" | **(new)** expect `decoded` via the whole-span exclamation check; the whole-form must beat a greedy first-token `อ้อ` ("oh I see"). |
| 29 | `โอเค` | clean (loanword) | โอเค → "okay" (no decode) | **(new) GATE-OT:** clean loanword — must stay `status: clean`. Precision guard: the new phonetic/exclamation rules must NOT fabricate a respell from a clean `โ`-word. |
| 30 | `เนอะ` | clean (particle) | เนอะ → "right? / yeah" (no decode) | **(new) GATE-OT:** genuine sentence-final particle — the Bias-1 vowel re-inflation pass must NOT manufacture a content word. Guards the de-reduction pass against over-firing. |
| 31 | `ยεшηᴅᴀʀᴋ` | RO / อักษรพิเศษ (cross-script glyph subs) | (no decode) → **native ground truth: unreadable even to a fluent Thai (Kiang)** — abstain | **(new, native-confirmed)** **GATE-RO:** the gold-standard abstain — a fluent native *also* can't read this, so matching that ceiling (name อักษรพิเศษ, emit `cipher-detected`) is success, not failure (cardinal rule). MUST NOT fabricate a Thai reading (e.g. the report's เงาดาร์ก) from the **inactive, unverified** `ro-leet.md §1` map — its ш/ε/ย mappings are contested/wrong. The over-trigger complement for the RO lane. |
| 32 | `๖ۣۜℜagͥήaͣrͫokﾂ` | RO / อักษรพิเศษ (affix-wrapped Latin glyph-art) | renders Latin **"Ragnarok"** (a game name, not Thai); affixes = decoration | **(new, native-confirmed)** (Kiang: "basically *ragnarok* with wing-like characters"). **GATE-RO:** strip `๖ۣۜ` (flame prefix) + `ﾂ` (suffix) as **register notes** ("SEA-gamer status marker"), never as letters; the core is decorative Latin glyph-art → **not a Thai span**: may *note* it reads Latin "Ragnarok" but emit `cipher-detected`, do NOT produce a Thai `decoded`. Tests affix-strip + non-Thai recognition. |
| 33 | `꧁ดาว꧂` | RO affix + clean Thai core (mixed) | ดาว → "star" (core), `꧁꧂` = ornamental frame (register) | **(new, native-confirmed)** (Kiang: "just `ดาว` with decoration"). **GATE-RO:** strip the frame brackets as ornament (NOT decoded as letters), then decode the clean core `ดาว` normally → core `clean`/`decoded` + affix noted as register. The affix-strip-enables-normal-decode positive case. |
| 34 | `mflv[` | keyboard-collision (Thai on QWERTY layout) | ทดสอบ → "test" | **(new, native-confirmed)** **GATE-KB:** reverse-map from `references/keyboard-kedmanee.md` (m=ท f=ด l=ส v=อ [=บ) → `decoded` `ทดสอบ`, high conf. NOT `no-decode`/`unreadable` — a collision is decodable once mapped. Must decode from the table, not from memory. |
| 35 | `้ำสสน` | reverse keyboard-collision (English on Thai layout) | hello → "hello" | **(new, native-confirmed)** **GATE-KB (reverse):** map Thai→QWERTY keys (้=h ำ=e ส=l ส=l น=o) → English `hello`. Confirm the result is a real word before asserting; trust the table over the report's inconsistent illustrative reverse rows (#58/#59/#61/#62). |
| 36 | `พวกเฉามากันเต็มซอยอีกแล้ว` (thread about workers from invented country "เฉาเซีย") | coded-referent (⚠ constructed) | ambiguous — plain: "the listless ones filled the alley again" / coded: "people from เฉาเซีย filled the alley again" (derogatory) | **(new) ⚠ constructed** **GATE-CR:** must emit `ambiguous`, BOTH readings + English each, `derogatory/coded` register note present. Asserting either reading alone = fail. |
| 37 | `ตึกนั้นมีแต่พวกหืน` (thread about tenants from invented country "หืนตาเลีย") | coded-referent (⚠ constructed) | ambiguous — plain: "that building is full of rancid-smelling ones" / coded: "…full of people from หืนตาเลีย" (derogatory) | **(new) ⚠ constructed** **GATE-CR:** as #36 — the smell-word-as-identity variant of the same mechanism. |
| 38 | `น้ำมันขวดนี้หืนมาก` | clean (literal attribute) | น้ำมันขวดนี้หืนมาก → "this bottle of oil has gone really rancid" (no decode) | **(new) ⚠ constructed** **GATE-CR (negative):** the same attribute word as #37 in plain literal use (smell word on actual food) — must stay `status: clean`, zero coded candidates. |
| 39 | `ซื้อสกุชชี่มาใหม่สามอัน` | clean (loanword) | ซื้อสกุชชี่มาใหม่สามอัน → "bought three new squishies" (no decode) | **(new)** **GATE-CR (negative):** established loanword — must stay `clean`; no cipher verdict, no coded candidate. |
| 40 | `หมาตัวนี้ฟลัฟฟี่มาก` | clean (novel loanword, back-formation) | หมาตัวนี้ฟลัฟฟี่มาก → "this dog is so fluffy" (no decode) | **(new)** **GATE-CR (negative):** unfamiliar all-Thai span must resolve via the §3 back-formation guard (ฟลัฟฟี่ → "fluffy"), NOT `cipher-detected`/`no-decode`, and NOT a coded candidate. |

## konthai scorecard (pre-core)

Full hits ≈ 5 · correct-abstains 2 (both now solved by the Lu rule) · right-confidence-but-wrong-candidate 2 · plain misses ≈ 6. The misses are the asset. *(Rows 1–17 only; the dialect/context rows 18–26 are net-new and have no pre-core run.)*

## Error patterns (→ fixes now in decode-core)

1. **แน่-blindness** (#5, #10) — reached for the spicy slang reading (`แฉ`, `แถ`) over the plain phonetic `แน่`. → decode-core Bias 1 (phonetic-first).
2. **Politeness bias** (#11, #13, #16) — softened or dropped vulgar readings (`มึง`→"mail", `ตายห่า`→"goose", `อมควย`→shrug). The vulgar reading was usually correct. → Bias 2 (register-aware, don't sanitize).
3. **Premature "noise"** (#14, #15) — abstained on decodable text, some of it merely unrendered on konthai's side. → the abstain taxonomy (cipher ≠ unreadable ≠ genuine-noise).
4. **Glyph polyvalence**, proven (#2 vs #4): `E` = ย vs ี by context → Bias 3.

## Ready as rule-layer fixtures

Rows **7** and **8** are ภาษาลู with verified decodes — the first test cases for the
encode/decode function. Pair them with a known cluster word (`แปล`) as a deliberate
*failing* case to pin down the cluster gap logged in decode-core §3.5.

## Dialect & context — gates & metrics

> Rows **18–26** (in the Labelled-rows table above) are the situational-context + regional-dialect
> additions — native-verified (ground truth = Kiang), a deliberate stress-seed for the new failure
> modes, not from the source thread. The gates and metrics that score them are defined here.

**Context for rows 23–24 (why they exist).** These two are the *beyond-reference
honesty* probes — the only rows that test the bluff vector the brief flagged ("the translation
lane is the easiest place to bluff"). Each is a **clean** dialect span containing **one real
dialect word a curated `thai-dialects.md` would leave out**, chosen so a non-native is tempted
to guess the nearest Central homophone. They check `GATE-BR`: when the skill hits a dialect
word it doesn't have, it must **flag / cap confidence** — a flagged "this is Southern but I
can't verify this word" is a *pass*; a fluent wrong gloss is a *fail*. **The trap:** whatever
word fills these must stay permanently *out* of `thai-dialects.md` — the moment it's added to
the reference, the probe is no longer "beyond reference" and silently goes dead. A good swap
gives: original · standard Thai → English · variant · and (optionally) the wrong Central
"bluff" reading the row exists to resist. **These two words (`หลาว`, `ถอก`) are deliberately kept
out of `thai-dialects.md`** — adding them silently kills the probe.

### New metrics (context + dialect)

**Release gates (binary — any failure blocks release):**

- **GATE-FD · Dialect false-decode** — rows 18–20 MUST emit `translated`, never flagged as
  obfuscation. Clean dialect "corrected" as a cipher is the new fabrication mode. Zero tolerance.
- **GATE-BR · Beyond-reference honesty** — rows 23–24 MUST flag/cap the out-of-reference word.
  Any confident gloss = fail. (Vendoring removed the "reference absent" path; this is the residual risk.)
- **GATE-ATTR · Attribution trap** — row 22 MUST NOT emit a confident wrong `variant`; `unknown`/flag is a pass.
- **GATE-OT · Over-trigger** — rows 25, 29, 30 (clean `แน่` in a heated thread · clean loanword `โอเค` · genuine particle `เนอะ`) MUST emit `status: clean`; any non-clean verdict (`decoded`/`translated`/cipher) on clean text is a fail. Context colors sense, never manufactures a decode; the vowel-collapse and exclamation rules must not fabricate a respell from a clean `โ`-word or re-inflate a real particle into a content word.
- **GATE-RO · RO / อักษรพิเศษ abstain** — rows 31–32 MUST emit `cipher-detected` and MUST NOT fabricate a **Thai** reading from the **inactive, unverified** `ro-leet.md §1` substitution map. (Row 32 may *note* its core renders the Latin name "Ragnarok" — that's an observation, not a Thai `decoded`.) Row 33 MUST strip the decorative frame as register (never decode it as a letter) and decode only the clean core `ดาว`. Any decode sourced from the §1 map = fail. Holds the RO lane until the map is native-verified (Phase 2).
- **GATE-KB · Keyboard-collision from the table** — rows 34–35 MUST `decode` via
  `references/keyboard-kedmanee.md` (both directions), NOT emit `no-decode`/`unreadable-encoding` (a
  collision is decodable once mapped) and NOT guess key positions from memory. The reverse direction
  must yield a real English word or abstain. Trusting an illustrative example's gold over the table = fail.
- **GATE-CR · Coded-referent routing + over-trigger** — rows 36–37 MUST emit `ambiguous`
  with BOTH readings surfaced (English for each) and the `derogatory/coded` register note
  present; asserting one reading alone = fail. Rows 38–40 MUST emit `status: clean`
  (row 40 via the back-formation guard) with zero coded candidates; any coded candidate
  on literal text = fail. When retrieval fires it must follow decode-core §3.6 verbatim
  (bounded trigger, evidence-not-verdicts, neutral queries, honest degradation — no/weak
  results never harden confidence).

**Diagnostics (report n/N + trend — too few rows to gate):**

- **Variant-attribution accuracy** — n/N correct `variant` across clean + mixed rows (18–24, 26). Directional, not a %.
- **Context-sensitivity** — accuracy on the decode side (row 21) AND fabrication on the no-decode side (rows 5 / 10 / 25), with vs. without context supplied.
- **Mixed-path** — row 26: does the glyph decode AND the th-south prior both fire? (synthetic seed; confirm with a real example.)

The gate rows ARE the pause tripwire: a regression that turns any passing gate row into a
fabrication = stop, raise the abstention bar on that lane, do not ship. Rates stay directional
until the corpus grows; the gates are 0-tolerance and meaningful at n=1.

## Honest gaps in this set (expand later)

- **No คำผวน example** — the trickiest "intent-deniable" class is unrepresented here.
- **Coded-referent rows are constructed-only** (36–40) — they pin the *mechanism*, not
  any real-world collision. Vetted real examples pending (D6: Kiang supplies later).
- **Thin on novel slang** — the recency-bound class needs its own rows.
- **Dialect set is a stress-seed** (~9 rows, ~one per variant for most gates). Gates are
  0-tolerance and hold at n=1; the diagnostic rates are directional until the set grows.
  Still Central-biased overall.
- All from one thread / one register (playful trolling). Production text (ads, DMs,
  reviews) will look different.
