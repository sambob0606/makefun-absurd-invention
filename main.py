#!/usr/bin/env python3
"""One-Sentence Absurd Invention Pitch.

Writes a single sentence pitching a ridiculous invention that fixes a
tiny everyday annoyance, to /output/entry.txt.

The pitch: a fridge that will not open until you confess out loud what
you came for, so a 2 a.m. snack has to justify itself first. The laugh
comes from the invention itself (a fridge acting as a confessional),
the fix is silly yet weirdly plausible (shame as a portion-control
device), and the sentence names the annoyance, the invention and its
mechanism in one clean line.

Standard library only; no network, no input files.
"""

import os
import sys

PITCH = (
    "A fridge that refuses to open until you confess out loud what you "
    "came for, so your midnight snack has to justify itself first."
)

MAX_CHARS = 220


def is_single_sentence(text):
    """True when the text is one sentence: exactly one terminal period."""
    stripped = text.strip()
    if not stripped:
        return False
    # Abbreviations such as "a.m." carry periods that do not end a
    # sentence, so hide them before counting sentence terminators.
    probe = stripped
    for abbr in ("a.m.", "p.m.", "e.g.", "i.e.", "Mr.", "Mrs.", "Dr."):
        probe = probe.replace(abbr, abbr.replace(".", ""))
    # One sentence means one terminating full stop, at the end, and no
    # other sentence-ending punctuation inside.
    if probe.count(".") != 1 or not probe.endswith("."):
        return False
    return not any(mark in probe[:-1] for mark in ("!", "?", ";", ":"))


def build_pitch():
    """Return the pitch, validated against the competition gate."""
    pitch = PITCH.strip()
    if not (1 <= len(pitch) <= MAX_CHARS):
        raise ValueError(
            "pitch must be 1 to 220 characters, got %d" % len(pitch)
        )
    if pitch != pitch.encode("utf-8").decode("utf-8"):
        raise ValueError("pitch is not valid UTF-8 text")
    if "  " in pitch or pitch != pitch.strip():
        raise ValueError("pitch has stray whitespace")
    if not is_single_sentence(pitch):
        raise ValueError("pitch must be exactly one sentence")
    return pitch


def main():
    output_path = os.environ.get("MAKEFUN_OUTPUT", "/output/entry.txt")
    pitch = build_pitch()
    out_dir = os.path.dirname(output_path)
    if out_dir:
        os.makedirs(out_dir, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as handle:
        handle.write(pitch)
    print("wrote %d characters to %s" % (len(pitch), output_path))
    return 0


if __name__ == "__main__":
    sys.exit(main())
