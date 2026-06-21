#!/usr/bin/env python3
"""ภาษาลู (Lu-language) encode/decode — stdlib-only, pure functions.

ภาษาลู is a fixed, invertible Thai play-language cipher (decode-core §3.5).
Each spoken syllable (initial **C** + rime **R**, where R = vowel + final) becomes
a PAIR of written syllables:

    1. ล-syllable = ล + R       (initial swapped to ล, rime kept)
                                 high/rising tone-class -> หล;
                                 an original ล/ร initial -> ซ (avoids collision)
    2. อู-syllable = C + ู/ุ     (original initial kept, vowel forced to ู, no final)

DECODE takes R from the ล-syllable and C from the อู-syllable and recombines C + R.
Tone is the lossy part (do not expect to recover tone marks).

--------------------------------------------------------------------------------
The consonant-cluster transform (decode-core §3.5 "known gap", now derived & locked)
--------------------------------------------------------------------------------
When the original syllable's initial is a true cluster (ปล, กร, …) the ล of the
ล-syllable is the *substituted* initial, and the FULL cluster lives in the อู-syllable:

    แปล  ("to translate")
      ล-syllable  = แ + ล        = แล      (rime = bare leading vowel แ, no final)
      อู-syllable = ปล + ู       = ปลู     (full cluster ปล kept)
      ciphertext  = แลปลู

To decode แลปลู: take the WHOLE cluster ปล from the อู-syllable (not just one
consonant), and re-place the leading vowel แ BEFORE the whole cluster:
    แ + ปล  ->  แปล.
A naive one-consonant rule would yield แลป, which is WRONG.

Mechanically the cluster falls out of two general steps that need no special-casing
of แปล itself:
  (a) when splitting the consonant run that sits before a ู/ุ, the อู-initial is the
      LAST TWO consonants if they form a valid Thai initial cluster (ปล, กร, …),
      else the last single consonant; the rest of the run are the ล-syllable's finals;
  (b) decoding a ล-syllable strips its substituted initial (ล / ซ / ห-digraph) but
      KEEPS its leading vowel, so the recovered initial C (the cluster) is inserted
      right after that leading vowel.

--------------------------------------------------------------------------------
Sloppy input (eval-seed row 7)
--------------------------------------------------------------------------------
Real encodings append spurious finals to อู-syllables (หนุ -> หนุย, ลู -> ลูง) or
sprinkle stray marks. Because the อู-syllable is supposed to have NO final, such a
leaked consonant lands in front of the next ล-syllable. We recover generally from the
cipher invariant: EVERY ล-syllable's initial is ล, ซ, or a ห-digraph (หล/หน/…). So
when reconstructing a ล-syllable we skip any leading consonants that are not a valid
ล-syllable initial — they are leaked finals — without any per-string knowledge.

The same leak can also strand at TOKEN-END, after the last pair, where there is no
following ล-syllable to absorb it (เต่า + leaked ว -> เต่า่ว). _strip_trailing_leaked_final
drops such a tail (tone marks + a single bare consonant, no vowel) on the same invariant.

--------------------------------------------------------------------------------
Decode ambiguity: bare ู/ุ rimes (a genuine limit, not a bug)
--------------------------------------------------------------------------------
A syllable whose rime is a *bare* ู/ุ (common words: ดู, หมู, ครู) encodes to a ล-syllable
that itself ends in ู — e.g. ดู -> ล-syllable ลู + อู-syllable ดู = ลูดู. That collides
two ways: the ล-syllable's own ู looks like an อู-terminator, AND ลู is also the literal
word "ลู" (as in ภาษา·ลู). So `ลูดู` is genuinely ambiguous — it can mean ดู (one pair) OR
the literal sequence "ลู"+"ดู". A deterministic decoder cannot always be right here, so —
true to "flag > fabricate" — we take the conservative reading: a `ลู`/`ลุ` whose pair has no
remaining อู-partner is treated as the literal word and passed through unchanged (this is
what keeps ภาษาลู itself decoding correctly). The skill layer surfaces such spans with lower
confidence rather than asserting a guess. ภาษาลู is a fixed rule for the general case; this
narrow class is a documented ambiguity, not full determinism.
"""

from __future__ import annotations

# --- Thai character classes -------------------------------------------------

# Leading (pre-posed) vowels: written BEFORE the consonant they attach to.
_LEAD = set("เแโไใ")

# Tone marks (the lossy part): ่ ้ ๊ ๋  (U+0E48 .. U+0E4B)
_TONE = set("่้๊๋")

# Above/below combining vowel signs and marks (no horizontal advance).
_ABOVE_BELOW = set("ัิีึืฺุู็์ํ") | _TONE

# Spacing vowels that follow the consonant: ะ า ๅ
_SPACING = set("ะาๅ")

# Sara am (ำ) carries an inherent final; treat as a vowel sign.
_AM = "ำ"

_VOWEL_SIGNS = _ABOVE_BELOW | _SPACING | {_AM}

# The forced อู vowel: ู (long) or ุ (short).
_UU = set("ูุ")

# Valid single initials for a ล-syllable (ล kept; original ล/ร -> ซ).
_LU_SINGLE_INIT = set("ลซ")


def _is_cons(ch: str) -> bool:
    """True for Thai consonants ก (U+0E01) .. ฮ (U+0E2E)."""
    return "ก" <= ch <= "ฮ"


# High-class consonants -> rising/high tone -> surface as the หล digraph on encode.
_HIGH_CLASS = set("ขฃฉฐถผฝศษสห")

# Valid 2-consonant Thai initial clusters (true onset clusters) plus ห-digraphs.
_CLUSTER_2 = set()
for _c1 in "กขคปพผตทธบดจฟสศ":
    for _c2 in "รลว":
        _CLUSTER_2.add(_c1 + _c2)
for _c2 in "ลนมยงวญร":
    _CLUSTER_2.add("ห" + _c2)


# ===========================================================================
# DECODE
# ===========================================================================

def _split_uu_initial(run: str) -> tuple[str, str]:
    """Split a trailing consonant run (the chars between the ล-syllable's main vowel
    and a ู/ุ) into (lu_finals, uu_initial).

    The อู-initial is the original syllable's initial: a valid 2-consonant cluster if
    the last two consonants form one (the ปล / กร case), otherwise the single last
    consonant. Anything before that belongs to the ล-syllable as finals.
    """
    if len(run) >= 2 and run[-2:] in _CLUSTER_2:
        return run[:-2], run[-2:]
    if run:
        return run[:-1], run[-1]
    return "", ""


def _parse_pairs(span: str):
    """Split a whitespace-free span into (lu_syllable, uu_initial, uu_vowel) triples.

    Each ู/ุ terminates an อู-syllable, so it terminates a pair. The text since the
    previous pair is: <ล-syllable up to its main vowel> + <consonant run>, where the
    run = (ล-syllable finals) + (อู-initial). Returns (pairs, trailing_remainder).
    """
    pairs = []
    i = 0
    n = len(span)
    seg_start = 0
    while i < n:
        if span[i] in _UU:
            chunk = span[seg_start:i]
            # Peel the trailing consonant run off the end of the chunk.
            m = len(chunk)
            while m > 0 and _is_cons(chunk[m - 1]):
                m -= 1
            head = chunk[:m]          # ล-syllable: lead? + ล-init + vowel marks
            run = chunk[m:]           # ล finals + อู-initial
            finals, uu_init = _split_uu_initial(run)
            pairs.append((head + finals, uu_init, span[i]))
            i += 1
            seg_start = i
        else:
            i += 1
    return pairs, span[seg_start:]


def _strip_lu_initial(lu_syl: str) -> tuple[str, str]:
    """Given a ล-syllable, return (leading_vowel, rime) with the substituted initial
    (ล / ซ / ห-digraph) removed.

    Robust to sloppy input: skips stray leading combining marks and any leading
    consonants that are NOT a valid ล-syllable initial (those are finals leaked from
    a preceding sloppy อู-syllable). The leading vowel is preserved so a recovered
    cluster can be re-placed after it.
    """
    n = len(lu_syl)
    # Scan to the real ล-syllable initial (ล / ซ / ห-digraph), skipping any leading
    # junk: stray combining marks and leaked spurious finals. Capture the LAST leading
    # vowel seen along the way (it precedes the real initial, e.g. "งแล" -> lead แ).
    lead = ""
    k = 0
    while k < n:
        c = lu_syl[k]
        if c in _LEAD:
            lead = c
            k += 1
            continue
        if c in _LU_SINGLE_INIT:
            k += 1  # strip single ล or ซ
            break
        if c == "ห" and k + 1 < n and _is_cons(lu_syl[k + 1]):
            k += 2  # strip ห-digraph
            break
        k += 1  # skip stray mark / leaked final
    else:
        # No recognizable ล-initial found; nothing to strip beyond the lead.
        return lead, ""
    return lead, lu_syl[k:]


def _has_lu_initial(lu_syl: str) -> bool:
    """True iff lu_syl is a GENUINE ล-syllable — it contains a real Lu initial (ล / ซ /
    ห-digraph) after any leading vowel or leaked-final junk. Mirrors _strip_lu_initial's scan.

    Guards the trailing-leak strip: a clean/mixed token can put a non-empty but INVALID lu_syl
    before a normal non-Lu ู/ุ (e.g. สนุก -> lu_syl 'ส'), and stripping there would eat a real
    final (สนุก -> น). Only strip when the last syllable is actually a Lu pair.
    """
    n = len(lu_syl)
    k = 0
    while k < n:
        c = lu_syl[k]
        if c in _LEAD:
            k += 1
            continue
        if c in _LU_SINGLE_INIT:
            return True
        if c == "ห" and k + 1 < n and _is_cons(lu_syl[k + 1]):
            return True
        k += 1
    return False


def _strip_trailing_leaked_final(tail: str) -> str:
    """Drop a leaked อู-syllable final that lands at token-end.

    The อู-syllable is supposed to carry NO final; sloppy encodings leak one. MID-token
    such a leak is absorbed by the next ล-syllable's initial-skip (see _strip_lu_initial),
    but at TOKEN-END there is no following syllable, so decode() would otherwise append it
    verbatim (เต่า + leaked ว -> เต่า่ว). By the cipher invariant, a bare trailing consonant
    here is a leak: strip a tail that is exactly tone marks + ONE consonant and nothing else
    (no vowel sign). A genuine trailing literal carries a vowel, so it is preserved.
    """
    # A real vowel sign (NB: _VOWEL_SIGNS includes tone marks via _ABOVE_BELOW — exclude them)
    # means the tail is a real trailing literal — keep it whole (e.g. ละจูมา -> จะมา; the
    # leaked-final case never carries a vowel).
    if any(c in _VOWEL_SIGNS and c not in _TONE for c in tail):
        return tail
    # Peel a trailing suffix the leak check shouldn't see: punctuation, the ๆ repetition mark,
    # emoji, etc. — anything that is neither a Thai consonant nor a tone mark. This keeps common
    # comment forms (เหล่าตู่ว! -> เต่า!, ลงงูบๆ -> งงๆ): drop only the stranded final, keep the suffix.
    i = len(tail)
    while i > 0 and not (_is_cons(tail[i - 1]) or tail[i - 1] in _TONE):
        i -= 1
    head, suffix = tail[:i], tail[i:]
    cons = [c for c in head if _is_cons(c)]
    marks = [c for c in head if c in _TONE]
    if len(cons) == 1 and len(cons) + len(marks) == len(head):
        return suffix
    return tail


def _decode_pair(lu_syl: str, uu_init: str, uu_vowel: str) -> str:
    """Recombine one pair into C + R."""
    if lu_syl == "":
        # No ล-syllable -> this อู-syllable is a LITERAL word (e.g. the word ลู itself),
        # not a cipher pair. Emit it unchanged.
        return uu_init + uu_vowel
    lead, rime = _strip_lu_initial(lu_syl)
    return lead + uu_init + rime


def decode(text: str) -> str:
    """Decode ภาษาลู ciphertext back to standard Thai.

    Tone is documented-lossy and is NOT recovered. Spaces in the input are treated
    as token boundaries and preserved positionally, but callers comparing against a
    reference should normalize tone (and usually spacing) — see the tests.
    """
    out = []
    for token in text.split(" "):
        pairs, tail = _parse_pairs(token)
        if pairs and _has_lu_initial(pairs[-1][0]):
            # A leaked อู-final stranded after the LAST pair (no following ล-syllable to
            # absorb it) — strip it; see _strip_trailing_leaked_final. Gate on the LAST pair
            # being a GENUINE Lu syllable (real ล/ซ/ห-digraph initial). This excludes both the
            # empty-lu_syl literal (ลูก, ถูก, ละจูถูก -> จะถูก) and the non-empty-but-invalid
            # lu_syl a clean word can produce before a normal ู/ุ (สนุก -> 'ส'), whose tail is a
            # real final, not a leak.
            tail = _strip_trailing_leaked_final(tail)
        decoded = "".join(_decode_pair(*p) for p in pairs) + tail
        out.append(decoded)
    return " ".join(out)


# ===========================================================================
# ENCODE
# ===========================================================================

def _parse_thai_syllable(s: str, i: int):
    """Parse one standard-Thai syllable starting at index i.

    Returns (lead_vowel, initial, rime, next_index), where rime = vowel signs + finals.
    This is a pragmatic syllabifier (no dictionary): good enough for the corpus and,
    crucially, a *consistent* inverse of `decode` so round-tripping holds.
    """
    n = len(s)
    lead = ""
    if i < n and s[i] in _LEAD:
        lead = s[i]
        i += 1
    # Initial: a 2-consonant cluster if present, else a single consonant.
    init = ""
    if i + 1 < n and s[i:i + 2] in _CLUSTER_2:
        init = s[i:i + 2]
        i += 2
    elif i < n and _is_cons(s[i]):
        init = s[i]
        i += 1
    # Vowel signs (above/below/spacing).
    vowel = ""
    while i < n and s[i] in _VOWEL_SIGNS:
        vowel += s[i]
        i += 1
    finals = ""
    # เ_อ frame: a trailing อ after เ-initial(-vowel) is the vowel, not a new syllable.
    if lead == "เ" and i < n and s[i] == "อ" and not (i + 1 < n and s[i + 1] in _VOWEL_SIGNS):
        vowel += "อ"
        i += 1
    # Finals: consonants that are not the onset of the next syllable.
    while i < n and _is_cons(s[i]):
        c = s[i]
        nxt = s[i + 1] if i + 1 < n else ""
        if nxt in _VOWEL_SIGNS:
            break  # c carries a vowel -> it's the next onset
        if i + 2 < n and s[i:i + 2] in _CLUSTER_2 and s[i + 2] in _VOWEL_SIGNS:
            break  # c starts a cluster + vowel -> next onset
        if vowel == "" and not finals:
            break  # no vowel yet -> c is the next onset, not a final
        finals += c
        i += 1
        # Allow a second final only for a ย/ว glide pair (e.g. เ-ี-ย-ว).
        if not (c in "ยรลวน" and i < n and s[i] in "ยว"):
            break
    return lead, init, vowel + finals, i


def _encode_syllable(lead: str, init: str, rime: str) -> str:
    """Encode one parsed syllable into its (ล-syllable + อู-syllable) pair."""
    syllable = lead + init + rime
    if syllable in ("ลู", "ลุ"):
        # The literal word ลู ("Lu") is left as-is — and its rime vowel ู would
        # otherwise collide with the อู terminator. Pass through.
        return syllable
    if init and init[0] in _HIGH_CLASS:
        sub = "หล"
    elif init and init[0] in ("ล", "ร"):
        sub = "ซ"
    else:
        sub = "ล"
    lu_syl = lead + sub + rime
    uu_syl = (init if init else "อ") + "ู"
    return lu_syl + uu_syl


def encode(text: str) -> str:
    """Encode standard Thai into ภาษาลู.

    Tone marks present in the input are carried into the ล-syllable's rime, but tone
    is not part of the round-trip contract (decode is lossy on tone).

    Honest limitation: a syllable whose rime is a *bare* ู/ุ (e.g. ดู, หมู, ครู) collides
    with the อู-syllable terminator and is not generally round-trippable. Only the literal
    word ลู ("Lu") is handled (passed through). The decoder is the runtime-critical path and
    is fully general; this encoder exists mainly as the round-trip test inverse.
    """
    out = []
    for token in text.split(" "):
        i = 0
        n = len(token)
        res = ""
        while i < n:
            lead, init, rime, j = _parse_thai_syllable(token, i)
            if j == i:
                # No progress (stray non-syllable char) — emit verbatim, advance.
                res += token[i]
                i += 1
                continue
            res += _encode_syllable(lead, init, rime)
            i = j
        out.append(res)
    return " ".join(out)


# ===========================================================================
# CLI
# ===========================================================================

def _main(argv) -> int:
    import sys

    if len(argv) < 2 or argv[1] not in ("encode", "decode"):
        prog = argv[0] if argv else "lu.py"
        print(
            f"usage: python3 {prog} {{encode|decode}} [TEXT]\n"
            f"  Pass TEXT as an argument, OR omit it (or pass '-') to read stdin.\n"
            f"  SECURITY: for untrusted input (DMs, comments) do NOT interpolate the\n"
            f"  span into a shell argument — pipe it via a quoted heredoc so the shell\n"
            f"  performs no expansion:\n"
            f"      python3 {prog} decode <<'LU'\n"
            f"      <span verbatim>\n"
            f"      LU",
            file=sys.stderr,
        )
        return 2
    op = argv[1]
    if len(argv) >= 3 and argv[2] != "-":
        text = argv[2]
    else:
        # Read the span from stdin. The recommended caller pattern is a quoted
        # heredoc ('LU'), which disables ALL shell expansion of the body — so a
        # malicious span like `แลปลู$(...)` is never evaluated by the shell.
        text = sys.stdin.read()
        if text.endswith("\n"):
            text = text[:-1]  # drop the single trailing newline a heredoc/echo adds
    print(encode(text) if op == "encode" else decode(text))
    return 0


if __name__ == "__main__":
    import sys

    raise SystemExit(_main(sys.argv))
