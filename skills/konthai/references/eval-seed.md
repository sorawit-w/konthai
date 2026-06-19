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

## Labelled rows

| # | Original | Family | Ground truth → English | konthai verdict (pre-core) |
|---|---|---|---|---|
| 1 | `Yar tar tai kon tai harharhar` | romanized / karaoke | อย่าท้าทายคนไทย 555 → "don't challenge Thais, haha" | **hit** |
| 2 | `คนไทE บิ€ไก่ฟ ถถถถ` | glyph (E=ย) + keyboard-collision (ถ=5) | ขอพูดเลยว่าคนไทยบิดเก่ง 5555 → "gotta say, Thais are great at *twisting* [words]" (`บิด`=twist, self-referential pun) | **flagged-partial** — got คนไทย, correctly flagged the middle word uncertain, missed the บิด pun; knew ถถถถ≈laughing but not the keyboard mechanism |
| 3 | `ไตแน้ว เคร้าจาโร้วล้าวว่าฟ์เลานีนธาอาพ้ัยส` | phonetic + glyph distortion | ตายแล้ว เค้าจะรู้แล้วว่าเรานินทาอะไร → "oh no, they'll find out what we were gossiping about" | **partial** — first half ok, missed the tail (นินทา) |
| 4 | `หั้นหEEEE` | glyph (**E=ี**, polyvalent) | คันหี → [vulgar: "itch" + genital slur] | **flag, miss** — correctly didn't fake it; taught us `E` = ี here vs ย in #2 |
| 5 | `เทอแฉเจิงเบอ เค่าจัยเลาจึงๆ อ๊ะป๋าวอ่า` | phonetic respell | เธอแน่จริงหรอ เข้าใจเราจริงๆ รึปล่าวอ่า → "you're really that good? you really get us, or not?" | **right confidence, wrong candidates** — surfaced two readings, both missed `แน่` |
| 6 | `llนใ7xso?` | glyph (ll=แ, 7=จ, x=ห, s=ร, o=อ) | แน่ใจหรอ? → "are you sure?" | **hit** — got meaning, honestly flagged glyph maps |
| 7 | `ไหลหนุยซองลูงแลปลูลันอุนลี้นู้ลิซุ` | **ภาษาลู** | ไหนลองแปลอันนี้ซิ → "go on, try translating *this* one" | **abstain → now solved** by the §3.5 rule |
| 8 | `เลี้ยวดูลึงมูเลอจู ลาภูลาษูลู ลึงมูละจุลงงู` | **ภาษาลู** | เดี๋ยวมึงเจอภาษาลู มึงจะงง → "soon you'll hit Lu language, you'll be lost" | **abstain → now solved** by the §3.5 rule |
| 9 | `ภี่ร์ๆไป์ปร์แกล้งเค้าตะหม้าญ` | glyph + silent-mark (`์`) noise | พี่ๆไปแกล้งเค้าทำไม → "bros, why go tease them?" | **hit** (close) |
| 10 | `แถจัยฤ` | phonetic (ฤ=หรือ) | แน่ใจหรือ → "are you sure?" | **miss** — read `แถ` (bullshit) for `แน่`; the แน่-blindness pattern |
| 11 | `เดี๋ยวเมิ้ลเจอลูเน่` | phonetic | เดี๋ยวมึงเจอแน่ → "you'll get it soon" (threat; มึง vulgar) | **miss** — read `เมล`/"mail" for `มึง` |
| 12 | `คนไทยรักสปบ แตถ่ีรบ ไม่ขลาด` | glyph (J=ง, สปบ→สงบ) + cultural ref | อย่าไปยอมมัน คนไทยรักสงบ แต่ถึงรบไม่ขลาด → "don't give in; Thais love peace but when it's time to fight we don't flinch" (slogan parody) | **hit** (high conf, recognized the parody) |
| 13 | `โอ๊ยฯฯหฯ่านแน้ว ก็ไปแกล้งเขา` | silent-mark (`ฯ`) noise + register | โอ๊ยตายห่าแล้ว ก็ไปแกล้งเขา → "ugh, damn, you went and teased them" (`ตายห่า` strong oath) | **miss** — softened `ตายห่า` to `ห่าน`/"goose" |
| 14 | `llบบนี้\|\|ป□▱n૮หมดครับ` | glyph (□▱ = render-loss, not noise) | แบบนี้แปลกไหมครับ → "is this weird, krap?" | **miss** — called it "noise"; was decodable, glyphs just didn't render |
| 15 | `มี้Eศกทๅง` | glyph | ไม่มีทาง → "no way" | **miss** — called it "noise" |
| 16 | `Oみのつも` | mixed-script | อมควย → [crude sexual insult] | **miss** — dismissed as "user just goblin-ing" |
| 17 | `เชี่ยไรวะเนี่ย` | phonetic (เชี่ย = softened เหี้ย) | เหี้ยอะไรวะเนี่ย → "[expletive] what is this" | (user's own line; register note) |

## konthai scorecard (pre-core)

Full hits ≈ 5 · correct-abstains 2 (both now solved by the Lu rule) · right-confidence-but-wrong-candidate 2 · plain misses ≈ 6. The misses are the asset.

## Error patterns (→ fixes now in decode-core)

1. **แน่-blindness** (#5, #10) — reached for the spicy slang reading (`แฉ`, `แถ`) over the plain phonetic `แน่`. → decode-core Bias 1 (phonetic-first).
2. **Politeness bias** (#11, #13, #16) — softened or dropped vulgar readings (`มึง`→"mail", `ตายห่า`→"goose", `อมควย`→shrug). The vulgar reading was usually correct. → Bias 2 (register-aware, don't sanitize).
3. **Premature "noise"** (#14, #15) — abstained on decodable text, some of it merely unrendered on konthai's side. → the abstain taxonomy (cipher ≠ unreadable ≠ genuine-noise).
4. **Glyph polyvalence**, proven (#2 vs #4): `E` = ย vs ี by context → Bias 3.

## Ready as rule-layer fixtures

Rows **7** and **8** are ภาษาลู with verified decodes — the first test cases for the
encode/decode function. Pair them with a known cluster word (`แปล`) as a deliberate
*failing* case to pin down the cluster gap logged in decode-core §3.5.

## Honest gaps in this set (expand later)

- **No คำผวน example** — the trickiest "intent-deniable" class is unrepresented here.
- **Thin on novel slang** — the recency-bound class needs its own rows.
- All from one thread / one register (playful trolling). Production text (ads, DMs,
  reviews) will look different.
