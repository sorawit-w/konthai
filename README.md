<p align="center">
  <img src="assets/konthai-dad-meme.svg" alt="konthai" width="420"/>
</p>

<h1 align="center">konthai</h1>

<p align="center"><em>Reads the Thai that translators choke on. And tells you when it can't.</em></p>

---

Thai social text is full of writing that is *deliberately* unreadable to machines — สก๊อย
glyph-swaps, phonetic respelling, karaoke-romanized Thai, keyboard-layout collisions, the
ภาษาลู cipher, gamer leet, gen-z slang, spoonerisms, coded truncation-euphemisms.
Auto-translators faceplant on it. A
fluent human reads it on instinct.

konthai is that fluent human. It recovers standard Thai + an English reading — and when a
span genuinely can't be cracked, it **says so and names the cipher**, instead of inventing a
confident answer.

## What it looks like

Romanized Thai, the kind that dares you:

```
in   Yar tar tai kon tai harharhar
th   อย่าท้าทายคนไทย 555
en   "don't challenge Thais, lol"
```

The ภาษาลู cipher — a fixed, invertible Thai play-language. konthai rule-decodes it
deterministically:

```
in   ไหลหนุยซองลูงแลปลูลันอุนลี้นู้ลิซุ
th   ไหนลองแปลอันนี้ซิ
en   "go on, try translating this one"
```

And the part that matters most — the honest stop:

```
in   <a span in a cipher konthai doesn't have the key for>
→    cipher-detected: looks like a keyed substitution, but I can't recover it.
     Not noise, not unreadable bytes — I just don't have this key. (no fabricated decode)
```

## What it is

konthai is a single **skill** — a loadable decode procedure plus one deterministic helper
(the ภาษาลู cipher). The procedure was calibrated against a small, native-speaker-labelled
set of real obfuscated-Thai comments; every rule in it fixes an *observed* miss, not a
hypothetical one. It works span-by-span, classifies each into a family, decodes what it can,
and is precise about *why* it stopped on the rest. Regional dialect
(Northern/Southern/Isan) is a separate lane — a valid dialect word is not broken
Central Thai, so konthai recognizes the variant and translates clean dialect as a
self-contained fallback, flagging dialect words beyond its vendored reference rather
than guessing. This is a fallback, not a headline trigger.

The discipline is one line: **flag > fabricate.** The target is the fluent-human ceiling — if
a native speaker would abstain cold, abstaining (with the cipher named) is success, not
failure. konthai distinguishes several outcomes and never collapses them into "noise":

| status | meaning |
|---|---|
| `clean` | parses literally as standard Thai — nothing to decode |
| `decoded` | one reading clearly wins |
| `ambiguous` | readings genuinely compete — **all** are surfaced, none picked silently |
| `translated` | a clean regional-dialect span (Northern/Southern/Isan) rendered to standard Thai — a fallback lane, not a trigger |
| `cipher-detected` | a cipher it can't key — named, never faked |
| `unreadable-encoding` | the bytes/glyphs didn't render — *not* a failed decode |
| `no-decode` | genuine noise |

Confidence is reported per span, and the message-level confidence is the **weakest** span —
never an average.

## Install

```
/plugin marketplace add sorawit-w/konthai
/plugin install konthai@konthai
```

Or via the cross-platform CLI:

```
npx skills add sorawit-w/konthai
```

konthai fires on mangled / mixed-script Thai. It deliberately does **not** fire on clean
standard Thai (no over-decoding), on i18n / locale-file translation, or on single-word
in-context definitions.

Current release: `0.6.0`

## How it works

The depth lives in [`skills/konthai/`](skills/konthai/) — the decode procedure is
[`references/decode-core.md`](skills/konthai/references/decode-core.md) (detection, per-span
classification, the three candidate-generation biases, the abstain taxonomy, and §3.5 the
ภาษาลู rule). The native-labelled calibration set is
[`references/eval-seed.md`](skills/konthai/references/eval-seed.md). The deterministic ภาษาลู
codec is [`src/lu.py`](skills/konthai/src/lu.py).

## Future work

Two things are intentionally **not** built yet, because they need a model in the loop and
aren't needed for v1:

- **A runnable eval harness** that scores konthai's decode across the eval-seed rows
  (hit / miss / abstain vs the native-labelled ground truth) and re-measures against the
  pre-calibration baseline.
- **Stability-based confidence** — sampling the decode k≈5 times and clustering on the
  recovered standard-Thai form, so near-ties surface automatically as `ambiguous` instead of
  relying on a self-reported read.

Both are addable later without reworking what ships now.

## Sources

The Thai dialect reference
[`references/thai-dialects.md`](skills/konthai/references/thai-dialects.md) is vendored and adapted
(Thai slice only, notes-only) from `references/locale-knowledge.md` in
[`sorawit-w/agent-skills`](https://github.com/sorawit-w/agent-skills), synced 2026-06-20. It lets
konthai recognize regional dialect (Northern / Southern / Isan) as a prior and translate clean
dialect itself as a fallback — a single-owner copy, re-synced if the upstream Thai entries change.

## License

MIT — see [LICENSE](LICENSE). Packaging pattern adapted from
[`sorawit-w/kerby`](https://github.com/sorawit-w/kerby); see [NOTICE](NOTICE).
