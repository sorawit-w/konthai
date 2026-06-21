#!/usr/bin/env python3
"""
verify_ro_glyphs.py — pin glyph IDENTITY for konthai's ro-leet.md.

Verifies codepoint + Unicode name for the decorative-affix strip-list and scans the
Thai-consonant substitution map for garbled / duplicate cells. It does NOT verify
USAGE (whether a substitute is actually used in thRO) — that needs a native eye.

Usage:  python3 verify_ro_glyphs.py
Run it after pruning the map to re-pin codepoints on the surviving rows.
"""
import unicodedata as u


def info(s: str):
    cps = " + ".join(f"U+{ord(c):04X}" for c in s)
    names = " + ".join((u.name(c) if u.name(c, "") else "<no name>") for c in s)
    return cps, names


AFFIXES = {
    "๖ۣۜ": "flame/crown prefix (source mislabeled the 2nd mark)",
    "ﾂ": "cool/chill suffix",
    "ツ": "smile suffix",
    "シ": "cool suffix",
    "꧁": "frame bracket (source wrongly said 'Cham')",
    "꧂": "frame bracket (source wrongly said 'Cham')",
    "༒": "inner-frame ornament",
    "†": "dark framing",
    "★": "star framing",
    "✿": "flower",
}

# Verbatim from the source report §8.2 (deduped/garbled cells fixed in ro-leet.md, raw here).
SUBMAP = {
    "ก": "∩ ∏ Ω Ռ ח ν υ п л π ந ர ମ",
    "ข": "থ श ४ ရ ျ ∫ ဈ ૪ ឧ খ",
    "ค": "の ମ め ꢍ",
    "ง": "ງ פ ஜ এ ق ঐ ও ঞ ଏ ၅ ل σ ७",
    "จ": "ຈ す ब ন ল ম अ ज न ㅋ व",
    "ช": "જ Ճ ಶ ឋ",
    "ญ": "₪ വ ഖ ល ស ល ภ",
    "น": "Ա Њ थ ゆ њ થ य ਪ Ю ю ឍ ભ",
    "ด": "ດ ๑ இ ஏ ஞ ௭ ெ ໑",
    "ต": "๓ ຕ რ დ ព တ ო ถ",
    "ท": "η и מ ŋ ທ មមហ Ŋ",
    "ธ": "ຣ ຽ চ ន",
    "บ": "υ ບ ப ひ び",
    "ป": "ປ √ ច",
    "ผ": "ຜ ಛ ಟ ය చ ట",
    "ฝ": "ධ ඨ ຝ យ",
    "พ": "ш ಬ ധ ਘ ພ ဃ ឃ",
    "ภ": "ຟ ௰ ಚ ಭ ඩ",
    "ม": "ມ ஆ ௮ ঋ भ ಖ",
    "ย": "ε є ξ ઈ ຢ ع ধ ㄠ ঘ",
    "ร": "ຮ よ ی र ਙ 丂 હ វ",
    "ล": "ລ त ਫ਼ බ ढ द ट",
    "ว": "ວ ಞ Ձ",
    "ส": "さ ざ द ನ న ສ ឥ ৯ స",
    "ห": "ㄨ × Ҩ ண യ භ ຫ ӄ ம ﾒ א",
    "อ": "Ә ∂ Ο о ਹ ට ө Ө ბ ס ծ",
    "ฮ": "ར ອ",
}


def main():
    print("=== AFFIX STRIP-LIST (identity verified) ===")
    for ch, role in AFFIXES.items():
        cps, names = info(ch)
        print(f"{ch!r:6} {cps:30} {names}")
        print(f"        role: {role}")

    print("\n=== SUBMAP scan: garbled / duplicate cells ===")
    for th, subs in SUBMAP.items():
        cells = subs.split()
        flags = [f"MULTICHAR {c!r}" for c in cells if len(c) > 1]
        dups = sorted({x for x in cells if cells.count(x) > 1})
        if dups:
            flags.append("DUP " + ",".join(repr(d) for d in dups))
        print(f"{th}: {len(cells):2} cells" + (("  <<< " + " ; ".join(flags)) if flags else ""))
    print("\nNote: ਫ਼ (Gurmukhi PHA + nukta) is a legit 2-codepoint grapheme, not garbled.")
    print("Real garble to drop: មមហ (ท). Real dup to dedupe: ល (ញ).")


if __name__ == "__main__":
    main()
