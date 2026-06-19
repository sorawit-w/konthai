"""Tests for the ภาษาลู (Lu-language) encode/decode module.

Written test-first (TDD). Decodes are compared *tone-normalized* and
*space-normalized*: ภาษาลู is documented to lose tone (decode-core §3.5), and the
spaces in ciphertext are rhythmic grouping, not semantic word boundaries — the
row-8 ground truth merges/splits them differently from its input. So we strip Thai
tone marks (U+0E48–U+0E4B) and ASCII spaces from BOTH sides before asserting.

Run: python3 -m pytest skills/konthai/tests/test_lu.py -v
"""

import os
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
