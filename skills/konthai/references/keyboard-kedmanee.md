# konthai — keyboard-layout collision reference (Kedmanee ↔ US-QWERTY)

> The decode key for the **keyboard-layout collision** family (decode-core §2).
> A *factual* physical-layout mapping (Thai Kedmanee, TIS 820-2538, the default Thai
> layout on Windows/macOS/iOS/Android) — authored from the standard layout, not copied
> from any project. Corroborated by the public `piruin/th-en-keyboard` table cited in the
> deep-research report.
>
> **Why this file exists:** decode-core says "look up the layout map; do not assume key
> positions." This is that map. Decode keyboard collisions *from the table*, not from
> memory.

A keyboard collision happens when text is typed with the OS set to the **wrong layout**
(or deliberately, as a cipher). The bytes are real characters on the *other* script's keys.
Before reverse-mapping, the text parses as neither language — that is the tell.

## The map (same physical key, both directions)

Each row: **QWERTY key** → **Thai (Kedmanee, unshifted)**. Read left→right to decode Thai
typed on a QWERTY-set machine; read right→left to decode English typed on a Thai-set machine.

| key | Thai | key | Thai | key | Thai | key | Thai |
|---|---|---|---|---|---|---|---|
| `q` | ๆ | `a` | ฟ | `z` | ผ | `1` | ๅ |
| `w` | ไ | `s` | ห | `x` | ป | `2` | / |
| `e` | ำ | `d` | ก | `c` | แ | `3` | - |
| `r` | พ | `f` | ด | `v` | อ | `4` | ภ |
| `t` | ะ | `g` | เ | `b` | ิ | `5` | ถ |
| `y` | ั | `h` | ้ | `n` | ื | `6` | ุ |
| `u` | ี | `j` | ่ | `m` | ท | `7` | ึ |
| `i` | ร | `k` | า | `,` | ม | `8` | ค |
| `o` | น | `l` | ส | `.` | ใ | `9` | ต |
| `p` | ย | `;` | ว | `/` | ฝ | `0` | จ |
| `[` | บ | `'` | ง | | | `-` | ข |
| `]` | ล | | | | | `=` | ช |

(Shift layer and the rarer **Pattajoti** layout are out of scope here; add them only if real
fixtures demand it. Kedmanee is what the overwhelming majority of Thai typists use.)

## Worked examples

**Thai-from-QWERTY** (English keys → Thai meaning):
- `mflv[` → `m`=ท `f`=ด `l`=ส `v`=อ `[`=บ → **`ทดสอบ`** ("test")
- `gik` → `g`=เ `i`=ร `k`=า → **`เรา`** ("we / I")
- `lvo` → `l`=ส `v`=อ `o`=น → **`สอน`** ("teach")

**English-from-Thai** (Thai chars → English meaning):
- `้ำสสน` → ้=`h` ำ=`e` ส=`l` ส=`l` น=`o` → **`hello`**
- `นา` → น=`o` า=`k` → **`ok`**

**Digit-row collision** (already in eval-seed row 2): on a Thai layout, the digit `5` sits
where `ถ` prints, so a run of `ถถถถ` is laughter `5555` (→ `ห้าๆๆ` / "hahaha").

## Decode notes (cardinal rule still holds)

- A collision only *looks* like gibberish until reverse-mapped — it is **not** `no-decode`
  and **not** `unreadable-encoding`. Map it, then translate the recovered text.
- Reverse-direction (English-on-Thai-layout) output is usually a short English word; confirm
  the result is a real word before asserting. If the reverse-map yields nonsense, it may not
  be a collision at all — abstain rather than force it.
- The map is deterministic, but a writer can still mix layouts mid-string. Decode per span.
- ⚠️ The deep-research report's *illustrative* reverse rows are not all self-consistent
  (#58 `สรรา` would be `สนนา` for "look"; #59/#61/#62 imply `r`=ไ when ไ=`w`). Trust **this
  table**, not the report's constructed examples. See `eval-seed.md` quarantine note.
