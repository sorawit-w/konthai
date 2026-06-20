# Thai dialect reference (vendored)

> Synced from `agent-skills/skills/i18n/references/locale-knowledge.md` (Thai section) on 2026-06-20.
> Upstream: `github.com/sorawit-w/agent-skills`. Single-owner copy — re-sync if the upstream Thai
> entries change. Thai slice only, by design. Notes-only: the i18n persona role-tables and
> production-strategy prose were dropped; what remains is **recognition tells** a decoder uses.

This reference exists so konthai can tell a **regional dialect** apart from obfuscation and translate
clean dialect itself (no sibling skill). It is a recognition aid for the **common** cases, not a
complete lexicon. **flag > fabricate still governs:** when a span uses dialect vocabulary *beyond*
these notes, cap confidence and flag the unverifiable word — a flagged unknown beats a fluent wrong
gloss.

**Three `variant` targets** (a clean span in one of these → `status: translated`):
`th-lanna` (Northern) · `th-south` (Southern) · `th-isan`. The other two Thai entries below are
**negative-boundary** recognition — they are *not* regional dialects and must not be tagged `variant`:
`th-genz` → existing `slang` family; `th-bupphe` → classical/stylized register.

<!-- DO NOT ADD the eval beyond-reference probes to this file:
     `หลาว` (th-south, "again") and `ถอก` (th-isan, "to pour"). They are eval-seed.md rows 23/24
     (GATE-BR); adding them here silently kills the beyond-reference honesty test. Keep them out. -->

---

## th — Standard Thai (baseline, not a dialect)

The reference point. No spaces between words. Politeness particles ครับ/ค่ะ imply speaker gender.
Many tech terms stay transliterated (อีเมล, แดชบอร์ด). If a span parses as clean Standard Thai,
decode nothing — it is not dialect.

## th-lanna — Northern / คำเมือง  *(variant target → translated)*

Written in standard Thai script in digital use (historical ตัวเมือง script is not in play here).

**Tells:**
- Signature politeness particle **`เจ้า`** (the quintessential Lanna marker).
- Lexical divergences: **`อู้`** = พูด (speak) · **`แอ่ว`** = เที่ยว (go out / visit) · **`ลำ`** = สวย/อร่อย (beautiful / tasty) · **`ตะกี้`** = just now.
- Northern verb/pronoun forms and distinct tones; e.g. `เปิ้น` = เขา (he/she), `กิ๋น` = กิน (eat), question particle `กา`.

**Register:** soft, polite. Younger urban speakers (Chiang Mai) often mix only a handful of คำเมือง
words into Central Thai — recognize the Lanna word even inside an otherwise-Central span.

## th-south — Southern / ภาษาใต้  *(variant target → translated)*

**Tells:**
- Lexical: **`หรอย`** = อร่อย (delicious) — the classic one; do **not** mis-read as Central `ลอย` (float).
- Particles: **`หว่า`** (assertive, ~นะ) · **`ดิ`** · **`แหละ`** used differently from Central.
- Heavy **contraction / elision** — words shortened, speech fast and clipped. A Southern span often
  looks "missing letters" but is not corrupted.

**Register:** fast, direct, expressive — what reads as blunt in Central Thai is normal in ภาษาใต้. Do
not up-rank an aggression reading on register alone.

**Cultural note:** the deep South (Pattani, Yala, Narathiwat) is Muslim-majority — do not assume a
Buddhist cultural frame for Southern spans.

## th-isan — Isan / อีสาน  *(variant target → translated)*

Closely related to Lao; many words shared, written in Thai script in Thai digital contexts.
**Isan↔Lao overlap is real** — a span built only from shared Isan/Lao words may not be safely
attributable to one variant; prefer `unknown` over a confident pick (see also the shared-with-Lanna
case below).

**Tells:**
- Negation **`บ่`** = ไม่ (not). *(Shared with Lanna — `บ่` alone does not pin the variant.)*
- Particles: **`เด้อ/เด๊อ`** (~นะ) · **`สิ`** (future marker).
- Lexical: **`แซบ`** = อร่อย (delicious) · **`เว้า`** = พูด (speak) · intensifiers `บักหำ` / `อีหลี`.
- Agreement word **`แม่น`** = ใช่ (is / correct). *(Also used in Lanna — shared.)*

**Register:** decide nothing about formality from Isan markers alone; most Isan speakers are bilingual
and code-switch with Central Thai freely.

## th-genz — Gen Z Thai  *(NOT a dialect → `slang` family)*

Listed here so konthai does **not** mis-tag it as a regional dialect. Gen Z code-switching is the
existing `slang` family (decode-core §2), not `variant: th-*`.

**Tells (→ route to slang, not dialect):** heavy Thai↔English code-switching mid-sentence
("เรา vibe กับ feature นี้มาก"); stretched text (มากกกก); dropped ครับ/ค่ะ; fast-cycling slang
(อิอิ, 555+, ชิมิ — short shelf-life). Treat per the slang family's recency caveat.

## th-bupphe — Ayutthaya classical register  *(NOT a dialect → classical/stylized)*

Listed for the same negative-boundary reason. A modern-classic blend (popularized by บุพเพสันนิวาส),
**not** a regional dialect — never tag `variant`. If decoding is needed, treat as a stylized register,
not a cipher and not a regional variant.

**Tells:** archaic pronouns **`ข้า`** (I), **`เจ้า`** (you), **`ออเจ้า`** (affectionate address);
particles **`เพคะ`** / **`ขอรับ`** / **`เจ้าค่ะ`**; archaic **`จัก`** = จะ, **`มิ`** = ไม่; selective
ราชาศัพท์ (เสวย, บรรทม). Modern UI/tech terms stay modern even in this register.
