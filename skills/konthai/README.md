<p align="center">
  <img src="../../assets/banner.png" alt="konthai — decode obfuscated Thai into standard Thai and English" width="100%"/>
</p>

# konthai

A Claude Code skill that decodes deliberately obfuscated Thai (ภาษาวิบัติ) into standard Thai
+ English — and is honest about what it can't recover.

It reads mangled Thai the way a local who grew up online does: on instinct, fast. But it
**never bluffs** — a named *"can't crack this"* beats a fluent lie. That discipline is the
whole point, and it's calibrated to the fluent-human ceiling: if a native speaker would
abstain cold, abstaining (with the cipher named) is success.

## What it decodes

| family | what it is | recoverable? |
|---|---|---|
| romanized / karaoke | Thai in Latin phonetics (`kon tai`) | yes, high |
| phonetic respell | casual sound-spelling (`ค้าบ`, `มั้ย`) | yes, high |
| glyph substitution (สก๊อย) | look-alike glyphs (`E`=ย/ี, `ll`=แ, `7`=จ) | yes — maps are context-dependent |
| keyboard-layout collision | same physical key, layout toggled (`ถถถถ`=`5555`) | yes — via the layout map |
| **ภาษาลู** (Lu cipher) | syllables expanded into `ล-`/`อู-` pairs | **deterministic** — rule-decoded by `src/lu.py` |
| RO-leet | gamer symbol/letter soup | partial at best |
| คำผวน (spoonerism) | swapped rime + tone; intent is deniable | surface candidates, don't assert |
| slang | a real word with a non-literal current meaning | yes if known, else flag |

## How it decides to stop

Five outcomes, never collapsed into "noise" — `decoded`, `ambiguous`, `cipher-detected`,
`unreadable-encoding`, `no-decode`. It works **per span**, and the message-level confidence is
the **weakest** span, never an average. See [`SKILL.md`](SKILL.md) for the full output contract.

## The ภาษาลู codec (deterministic)

ภาษาลู is a fixed, invertible cipher — not an abstain case. The skill calls the codec instead
of guessing:

```sh
# Untrusted input (DMs, comments) — pipe via a quoted heredoc so the shell does
# NO expansion (a span like `…$(…)` must never reach the shell):
python3 src/lu.py decode <<'LU'
ไหลหนุยซองลูงแลปลูลันอุนลี้นู้ลิซุ
LU
# → ไหนลองแปลอันนี้ซิ   ("go on, try translating this one"; tone is lossy)
```

The consonant-cluster transform (e.g. `แลปลู → แปล`) is derived and locked under test —
`tests/test_lu.py`, and written up in [`references/decode-core.md`](references/decode-core.md) §3.5.

## Files

- [`SKILL.md`](SKILL.md) — the triggering wrapper + decode procedure + output contract.
- [`references/decode-core.md`](references/decode-core.md) — the calibrated decode logic (read first).
- [`references/eval-seed.md`](references/eval-seed.md) — the native-labelled calibration corpus.
  Weighted toward the *misses* — the hard rows are the point.
- [`src/lu.py`](src/lu.py) — the deterministic ภาษาลู codec. [`tests/`](tests/) — `pytest` fixtures.

## What it won't do

Decode clean standard Thai (over-decoding is a failure mode), translate i18n / locale files
(that's `i18n`), or define a single in-context word (that's `define`).

## License

MIT — see the repo root [LICENSE](../../LICENSE).
