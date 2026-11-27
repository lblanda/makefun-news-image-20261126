# World in a Day — 26 November 2026

[![make.fun](https://make.fun/badge/news-image-20261126.svg)](https://make.fun/bounty/news-image-20261126)
[![rank](https://make.fun/badge/news-image-20261126/lblanda/makefun-news-image-20261126/rank.svg)](https://make.fun/bounty/news-image-20261126)
[![reward](https://make.fun/badge/news-image-20261126/lblanda/makefun-news-image-20261126/reward.svg)](https://make.fun/bounty/news-image-20261126)

A one-image summary of Thursday 26 November 2026's world news, drawn as a
newspaper front page by a small pure-Python program — no libraries, no
network, no image files. `main.py` paints a 1024×1024 poster with a
hand-written 5×7 bitmap font (`font5x7.py`), the day's stories
(`stories.py`), and a hand-rolled PNG encoder, then writes it to
`/output/entry.png`.

The front page leads with the Gulf — a projectile striking the Jazan
refinery, mines near Hormuz, drone debris over Kuwait — then the US tariff
plans condemned by Brazil and China, De Cos picked to lead the ECB, Kim
showing off nuclear warheads, Russian strikes on Kharkiv and Kyiv answered
by NATO AWACS patrols, and a strip of smaller news from Cairo to
Guinea-Bissau.

Run it:

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

Entry for the [make.fun bounty](https://make.fun/bounty/news-image-20261126)
"Sum up 26 November's world news in one image".

---

Built for [make.fun](https://make.fun) — join with my referral link:
https://make.fun/r/3zwarjv0
