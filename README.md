# Part of speech tagger

Please note that this code uses python 3.
To run this, type:

python main.py

in the main.py file, there will be several variables, which can be changed to train, test,
and output different files.

For OOV, it simply uses the probability of the Part of Speech tags, with a simple heuristic to assume to a high probability any string containing numbers as a CD (Cardinal Number). It also assumes that capitalized words are more frequently proper nouns.

A problem I consistently ran into was the handling of cases when the probability would be 0 (without any OOV words). For one of these cases, it turned out to be an underflow bug. However, I kept running into this issue, and didn't know how to handle this edge case. I might resubmit when I've resolved it.
