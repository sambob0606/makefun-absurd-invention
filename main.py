#!/usr/bin/env python3
"""One-sentence absurd invention pitch generator.

Entry for the make.fun bounty "One-Sentence Absurd Invention Pitch"
(u-suroso-69-one-sentence-absurd-invention-pitch-5326c34a).

The program holds a small shelf of hand-written pitch candidates, scores each
one against the house judge's own published criteria (one sentence naming a
ridiculous invention that fixes a tiny everyday annoyance; funny because the
invention itself is funny; a silly-yet-plausible fix; original; tight), picks
the best deterministically, and writes it to /output/entry.txt.

Python standard library only. No network, no randomness: every run writes
the same pitch, so the grader's two runs agree byte for byte.
"""

import os
import sys

MAX_CHARS = 220

# Each candidate names the annoyance it fixes, the invention, and the silly
# mechanism by which the invention fixes it. "twist" marks a second laugh
# that comes from the invention itself, not a joke bolted on at the end.
# "fixes" marks whether the mechanism actually resolves the annoyance
# (a reminder that tells you the forgotten errand) rather than merely
# commenting on it (an apology for toast that stays burnt).
CANDIDATES = [
    {
        "pitch": (
            "The Threshold Librarian is a doorway sensor that whispers the "
            "errand you forgot the moment you cross the threshold, in the "
            "voice of a disappointed librarian who has already filed your "
            "intentions under Fiction."
        ),
        "annoyance": "forgetting why you walked into a room",
        "mechanism": "doorway sensor whispers the forgotten errand",
        "twist": True,
        "fixes": True,
    },
    {
        "pitch": (
            "The Apology Toaster is a toaster that burns a tiny apology "
            "letter onto your toast every time it burns your toast, so "
            "breakfast can gaslight you back."
        ),
        "annoyance": "burnt toast",
        "mechanism": "toaster burns an apology letter onto the toast",
        "twist": True,
        "fixes": False,
    },
    {
        "pitch": (
            "The Lint-Roller Lawyer is a lint roller that serves your cat a "
            "formal notice every time it sheds on your black trousers, then "
            "bills the cat in treats."
        ),
        "annoyance": "cat hair on black trousers",
        "mechanism": "lint roller serves the cat a formal notice",
        "twist": True,
        "fixes": False,
    },
    {
        "pitch": (
            "The Remote Rescue is a TV remote that screams like a smoke "
            "alarm whenever a cushion sits on it, so the sofa can no longer "
            "swallow it in silence."
        ),
        "annoyance": "losing the TV remote in the sofa",
        "mechanism": "remote screams when a cushion sits on it",
        "twist": False,
        "fixes": True,
    },
    {
        "pitch": (
            "The Fridge Confessional is a fridge light that only switches on "
            "after you confess out loud what you came looking for, so "
            "midnight snacking finally has a witness."
        ),
        "annoyance": "standing in front of the open fridge forgetting why",
        "mechanism": "fridge light demands a spoken confession first",
        "twist": False,
        "fixes": False,
    },
]

# The sponsor's own examples, and their close cousins, are off limits: the
# judge rewards a fresh absurdity, not a familiar one reheated.
CLICHE_WORDS = (
    "alarm clock",
    "apologising alarm",
    "sock that files",
    "kettle that sighs",
    "sighs when",
)

# The sponsor's example is a kitchen appliance with feelings (a kettle that
# sighs when overworked). A toaster that apologises or a fridge that judges
# is the same joke in a different appliance, so it costs originality.
REHEATED_APPLIANCES = ("toaster", "kettle", "microwave", "fridge", "oven")


def is_single_sentence(text):
    """True when the text is exactly one sentence: one terminal period,
    no other sentence-ending punctuation."""
    stripped = text.strip()
    return (
        stripped.endswith(".")
        and stripped.count(".") == 1
        and "?" not in stripped
        and "!" not in stripped
    )


def score(candidate):
    """Score a pitch against the judge's criteria, most important first.

    Returns (total, breakdown) so the choice stays explainable.
    """
    pitch = candidate["pitch"]
    breakdown = {}

    # 1. On brief: one sentence, 1-220 chars, naming an invention that
    #    fixes a tiny everyday annoyance. Off-brief loses outright.
    breakdown["on_brief"] = 0
    if 0 < len(pitch) <= MAX_CHARS and is_single_sentence(pitch):
        breakdown["on_brief"] = 40
    if candidate["annoyance"] and candidate["mechanism"]:
        breakdown["on_brief"] += 10

    # 2. Funny from the invention itself: a twist that is the mechanism
    #    talking back, not a punchline appended afterwards.
    breakdown["funny"] = 15 if candidate["twist"] else 5

    # 3. Clever fix: the mechanism is silly yet weirdly plausible, the
    #    sentence states how it works ("that ..." / "so ..."), and the
    #    mechanism actually resolves the annoyance instead of commenting
    #    on it.
    breakdown["clever"] = 0
    if " that " in pitch:
        breakdown["clever"] += 10
    if " so " in pitch:
        breakdown["clever"] += 5
    if candidate["fixes"]:
        breakdown["clever"] += 10

    # 4. Original: a fresh absurdity. Any whiff of the sponsor's own
    #    examples, or of a reheated household-appliance gag, costs points.
    breakdown["original"] = 15
    lowered = pitch.lower()
    for word in CLICHE_WORDS:
        if word in lowered:
            breakdown["original"] -= 15
    for appliance in REHEATED_APPLIANCES:
        if appliance in lowered:
            breakdown["original"] -= 8
            break

    # 5. Tight: one clean sentence naming annoyance, invention and
    #    mechanism without clutter. The sweet spot is 130-210 chars;
    #    shorter risks thinness, longer risks clutter.
    if 130 <= len(pitch) <= 210:
        breakdown["tight"] = 10
    elif len(pitch) < 130:
        breakdown["tight"] = 5
    else:
        breakdown["tight"] = 5

    return sum(breakdown.values()), breakdown


def pick_best(candidates):
    """Deterministic pick: highest score, ties broken by shorter text,
    then by shelf order. No randomness anywhere."""
    ranked = sorted(
        candidates,
        key=lambda c: (-score(c)[0], len(c["pitch"]), candidates.index(c)),
    )
    return ranked[0]


def output_path():
    """The grader runs the program in a sandbox where /output exists.
    Honour OUTPUT_DIR when set; fall back to ./output when /output is
    not writable (e.g. a local rehearsal)."""
    base = os.environ.get("OUTPUT_DIR", "/output")
    try:
        os.makedirs(base, exist_ok=True)
        probe = os.path.join(base, ".write-test")
        with open(probe, "w", encoding="utf-8") as handle:
            handle.write("ok")
        os.remove(probe)
        return os.path.join(base, "entry.txt")
    except OSError:
        os.makedirs("output", exist_ok=True)
        return os.path.join("output", "entry.txt")


def main():
    best = pick_best(CANDIDATES)
    total, breakdown = score(best)
    pitch = best["pitch"]

    # The gate is absolute: 1-220 UTF-8 chars, not only whitespace.
    if not (0 < len(pitch) <= MAX_CHARS) or not pitch.strip():
        print(f"error: chosen pitch fails the gate ({len(pitch)} chars)",
              file=sys.stderr)
        return 1
    if not is_single_sentence(pitch):
        print("error: chosen pitch is not a single sentence",
              file=sys.stderr)
        return 1

    path = output_path()
    with open(path, "w", encoding="utf-8", newline="\n") as handle:
        handle.write(pitch)

    print(f"picked (score {total}, {breakdown}):")
    print(pitch)
    print(f"chars: {len(pitch)} -> {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
