"""Tests for the ภาษาลู (Lu-language) encode/decode module.

Written test-first (TDD). Decodes are compared *tone-normalized* and
*space-normalized*: ภาษาลู is documented to lose tone (decode-core §3.5), and the
spaces in ciphertext are rhythmic grouping, not semantic word boundaries — the
row-8 ground truth merges/splits them differently from its input. So we strip Thai
tone marks (U+0E48–U+0E4B) and ASCII spaces from BOTH sides before asserting.

Run: python3 -m pytest skills/konthai/tests/test_lu.py -v
"""

import os
import subprocess
import sys

import pytest

# Make `lu` importable whether pytest is run from repo root or elsewhere.
SRC = os.path.join(os.path.dirname(__file__), "..", "src")
sys.path.insert(0, os.path.abspath(SRC))

import lu  # noqa: E402


# Thai tone marks: ่ ้ ๊ ๋  (U+0E48 .. U+0E4B)
_TONE_MARKS = {"่", "้", "๊", "๋"}


def norm(s: str) -> str:
    """Strip tone marks (lossy) and spaces (rhythmic) for comparison."""
    return "".join(ch for ch in s if ch not in _TONE_MARKS and ch != " ")


def assert_decode(cipher: str, expected_standard_thai: str):
    got = lu.decode(cipher)
    assert norm(got) == norm(expected_standard_thai), (
        f"\n  cipher   : {cipher!r}"
        f"\n  decoded  : {got!r}  -> norm {norm(got)!r}"
        f"\n  expected : {expected_standard_thai!r}  -> norm {norm(expected_standard_thai)!r}"
    )


# ---------------------------------------------------------------------------
# Fixture decodes (eval-seed rows 7 & 8, with verified ground truth)
# ---------------------------------------------------------------------------

def test_decode_row8():
    # eval-seed row 8 — the canonical worked example.
    assert_decode(
        "เลี้ยวดูลึงมูเลอจู ลาภูลาษูลู ลึงมูละจุลงงู",
        "เดี๋ยวมึงเจอภาษาลู มึงจะงง",
    )


def test_decode_row7():
    # eval-seed row 7 — flagged "sloppy" (spurious finals on อู-syllables: หนุย, ลูง,
    # นู้; stray น/้). The general rule "every ล-syllable's initial is ล/ซ/ห-digraph"
    # lets us identify and drop those leaked finals without per-string hacks.
    assert_decode(
        "ไหลหนุยซองลูงแลปลูลันอุนลี้นู้ลิซุ",
        "ไหนลองแปลอันนี้ซิ",
    )


def test_decode_trailing_leaked_final():
    # A leaked อู-final stranded at TOKEN-END (no following ล-syllable to absorb it).
    # Report-INDEPENDENT: built from row-8 mechanics (ลงงู -> งง, ละจู -> จะ) with a stray
    # consonant appended. Without the strip, decode would surface งงบ / จะบ.
    assert_decode("ลงงูบ", "งง")
    assert_decode("ละจูบ", "จะ")


def test_trailing_literal_with_vowel_is_kept():
    # Guard: a genuine trailing literal carries a vowel, so it must NOT be stripped.
    # ละจู -> จะ, then a real trailing " มา" (has vowel า) stays.
    assert_decode("ละจูมา", "จะมา")


def test_literal_uu_word_with_final_passthrough():
    # Regression guard (Codex review, PR #7): a LITERAL word that just happens to contain
    # ู/ุ + a final consonant (ลูก "child", ถูก "correct/cheap") forms only an empty-lu_syl
    # pseudo-pair — NOT a real Lu pair. The trailing-final strip must NOT fire, or the final
    # is corrupted (ลูก -> ลู). Exact equality: these are clean passthroughs, tone included.
    assert lu.decode("ลูก") == "ลูก"
    assert lu.decode("ถูก") == "ถูก"
    assert lu.decode("หมูป่า") == "หมูป่า"


def test_mixed_lu_then_literal_uu_final_passthrough():
    # Regression guard (Codex review round 2, PR #7): a REAL Lu pair immediately followed by a
    # literal ู/ุ-word with a final, no Thai space — ละจูถูก = จะ + ถูก. The last pair is the
    # empty-lu_syl literal ถู, so its real final ก must NOT be stripped (gate on the LAST pair,
    # not "any" pair). Without the fix this returned จะถู.
    assert_decode("ละจูถูก", "จะถูก")


def test_decode_cluster_แปล():
    # The consonant-cluster case (decode-core §3.5 "known gap").
    # ล-syllable = แล (ล + leading-vowel rime แ);
    # อู-syllable = ปลู (full cluster ปล + อู).
    # Naive one-consonant rule yields แลป (WRONG); correct is แปล.
    assert_decode("แลปลู", "แปล")


# ---------------------------------------------------------------------------
# Round-trip: decode(encode(x)) == x  for the expected standard-Thai strings
# ---------------------------------------------------------------------------

@pytest.mark.parametrize(
    "standard_thai",
    [
        "เดี๋ยวมึงเจอภาษาลู มึงจะงง",  # row 8 expected
        "ไหนลองแปลอันนี้ซิ",            # row 7 expected
        "แปล",                          # cluster word
    ],
)
def test_round_trip(standard_thai):
    encoded = lu.encode(standard_thai)
    decoded = lu.decode(encoded)
    assert norm(decoded) == norm(standard_thai), (
        f"\n  original : {standard_thai!r}"
        f"\n  encoded  : {encoded!r}"
        f"\n  decoded  : {decoded!r}"
    )


# ---------------------------------------------------------------------------
# CLI / stdin path (the shell-injection-safe invocation — see SKILL.md)
# ---------------------------------------------------------------------------

LU_PY = os.path.join(os.path.abspath(SRC), "lu.py")


def _cli_stdin(op: str, text: str) -> str:
    """Invoke the CLI with NO shell — argv list + stdin — mirroring the quoted
    heredoc the skill is told to use for untrusted spans."""
    r = subprocess.run(
        [sys.executable, LU_PY, op], input=text, capture_output=True, text=True
    )
    assert r.returncode == 0, r.stderr
    return r.stdout.rstrip("\n")


def test_cli_stdin_decode():
    assert norm(_cli_stdin("decode", "แลปลู")) == norm("แปล")


def test_cli_untrusted_metachars_are_inert():
    # A hostile span fed via stdin must be treated as plain TEXT — the shell never
    # sees it, so command substitution can't fire. The literal metachars survive in
    # the output (passed through), and the decodable prefix still decodes.
    payload = "แลปลู$(echo PWNED)`echo PWNED`"
    out = _cli_stdin("decode", payload)
    assert "$(echo PWNED)" in out      # passed through literally, not executed
    assert "แปล" in norm(out)           # the decodable prefix still decodes


# ---------------------------------------------------------------------------
# Documented decode ambiguity: bare ู/ุ rimes (decode-core §3.5)
# ---------------------------------------------------------------------------

def test_bare_uu_rime_is_documented_ambiguous():
    # `ลูดู` genuinely means EITHER ดู (one pair) OR the literal "ลู"+"ดู". The codec
    # takes the conservative literal reading rather than fabricating a decode; the
    # skill layer surfaces such spans as `ambiguous`. See decode-core §3.5.
    assert lu.decode("ลูดู") == "ลูดู"
    # The literal word ลู inside ภาษาลู must still pass through correctly:
    assert lu.decode("ลาภูลาษูลู") == "ภาษาลู"
