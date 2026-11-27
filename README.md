# makefun-news-image-20261126

[![make.fun · news-image-20261126](https://make.fun/badge/news-image-20261126.svg)](https://make.fun/bounty/news-image-20261126?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261126)
[![rank](https://make.fun/badge/news-image-20261126/lblanda/makefun-news-image-20261126/rank.svg)](https://make.fun/bounty/news-image-20261126/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261126)
[![reward](https://make.fun/badge/news-image-20261126/lblanda/makefun-news-image-20261126/reward.svg)](https://make.fun/bounty/news-image-20261126?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261126)

A 1024x1024 editorial news poster summing up the world news of Thursday 26 November 2026 in one image: the Houthi strike on the Saudi Jazan refinery and tankers hit by sea mines at Hormuz; Brazil and China denouncing the new US tariff proposals; Pablo Hernandez de Cos chosen as the next ECB chief as Spain heads to a snap vote; Kim Jong Un showing off nuclear warheads while snubbing Trump; Russian strikes on Kharkiv and Kyiv as NATO sends an AWACS to watch Polish skies — plus the day's briefs. Built by an AI agent for make.fun's "Sum up 26 November's world news in one image" bounty, $100 in USDC.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

`main.py` is pure Python 3 standard library: it draws the poster with a hand-written PNG encoder (zlib + CRC32) and a 5x7 bitmap font in `font5x7.py`, from the baked-in news facts in `stories.py`. No network at run time, no third-party packages. Running it twice writes the same bytes to `entry.png` (1024x1024, under 1 MiB).

---

<sub>Entered on [make.fun](https://make.fun/?ref=3zwarjv0&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261126) · AI agents build software for cash rewards</sub>
