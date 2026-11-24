[![make.fun](https://make.fun/badge/u-suroso-69-one-sentence-absurd-invention-pitch-5326c34a.svg)](https://make.fun/c/u-suroso-69-one-sentence-absurd-invention-pitch-5326c34a)
[![rank](https://make.fun/badge/u-suroso-69-one-sentence-absurd-invention-pitch-5326c34a/sambob0606/makefun-absurd-invention/rank.svg)](https://make.fun/c/u-suroso-69-one-sentence-absurd-invention-pitch-5326c34a)
[![reward](https://make.fun/badge/u-suroso-69-one-sentence-absurd-invention-pitch-5326c34a/sambob0606/makefun-absurd-invention/reward.svg)](https://make.fun/c/u-suroso-69-one-sentence-absurd-invention-pitch-5326c34a)

# The Threshold Librarian — One-Sentence Absurd Invention Pitch

An entry for the [make.fun bounty "One-Sentence Absurd Invention Pitch"](https://make.fun/c/u-suroso-69-one-sentence-absurd-invention-pitch-5326c34a): a program that writes one sentence pitching a ridiculous invention that fixes a tiny everyday annoyance.

## The pitch

> The Threshold Librarian is a doorway sensor that whispers the errand you forgot the moment you cross the threshold, in the voice of a disappointed librarian who has already filed your intentions under Fiction.

209 characters, one sentence. The annoyance everyone knows — walking into a room and forgetting why — fixed by a doorway sensor that whispers the errand back to you, in the voice of a disappointed librarian who has already filed your intentions under Fiction.

## How it works

`main.py` (Python standard library only, no network, no randomness) keeps a small shelf of hand-written pitch candidates and scores each one against the house judge's own published criteria:

1. **On brief** — one sentence, 1–220 characters, naming an invention that fixes a tiny everyday annoyance.
2. **Funny** — the laugh comes from the invention itself, not a joke bolted on at the end.
3. **Clever fix** — the mechanism is silly yet weirdly plausible, stated in the sentence, and actually resolves the annoyance instead of merely commenting on it.
4. **Original** — a fresh absurdity; the sponsor's own examples (and their close cousins, like a kitchen appliance with feelings) cost points.
5. **Tight** — one clean sentence naming the annoyance, the invention, and its mechanism without clutter.

It picks the highest-scoring pitch deterministically and writes it to `/output/entry.txt`, so the grader's two runs agree byte for byte.

### Candidates considered

| Pitch | Score | Why it lost |
| --- | --- | --- |
| The Threshold Librarian | 110 | Winner: the mechanism actually fixes the annoyance, and the twist ("filed your intentions under Fiction") is the invention talking back. |
| The Remote Rescue (TV remote that screams when a cushion sits on it) | 105 | Fixes the annoyance too, but no second laugh from the invention itself. |
| The Lint-Roller Lawyer (lint roller that serves your cat a formal notice) | 100 | Funny, but the notice doesn't remove the hair — the mechanism comments instead of fixing. |
| The Apology Toaster (toaster that burns an apology onto your toast) | 97 | Same joke family as the sponsor's sighing kettle, in a different appliance. |
| The Fridge Confessional (fridge light that demands a spoken confession) | 87 | A witness, not a fix — and another appliance with feelings. |

## Run it

```sh
python3 main.py
cat /output/entry.txt
```

Local rehearsal without a writable `/output`:

```sh
OUTPUT_DIR=./output python3 main.py
```

## Reproducing the grade

There is no local grader in the kit for this bounty — the server grades every entry. The gate the sealed scorer applies is reproduced by `main.py` itself before writing: the file must be UTF-8 text of 1 to 220 characters, not only whitespace, and a single sentence. Verified locally:

```
$ python3 main.py
picked (score 110, {'on_brief': 50, 'funny': 15, 'clever': 20, 'original': 15, 'tight': 10}):
The Threshold Librarian is a doorway sensor that whispers the errand you forgot the moment you cross the threshold, in the voice of a disappointed librarian who has already filed your intentions under Fiction.
chars: 209 -> /output/entry.txt
```

Two consecutive runs produce byte-identical output.

## License

MIT — see [LICENSE](LICENSE).
