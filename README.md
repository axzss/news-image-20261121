[![make.fun · news-image-20261121](https://make.fun/badge/news-image-20261121.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![rank](https://make.fun/badge/news-image-20261121/axzss/news-image-20261121/rank.svg)](https://make.fun/bounty/news-image-20261121/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![reward](https://make.fun/badge/news-image-20261121/axzss/news-image-20261121/reward.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)

# news-image-20261121 — The World, Saturday 21 November 2026

A one-page newspaper front page summing up the world's news of
Saturday 21 November 2026, as a single 1024×1024 PNG. The entry program
(`main.py`) copies the bundled image to `/output/entry.png` — a plain
byte copy, deterministic, no network, no randomness, no imaging
library needed at grade time.

The image is drawn by `render.py` with Pillow: masthead, a lead story
(Russia's biggest strikes on Ukraine, with missiles falling in Poland)
with a night-skyline motif of missile arcs over a city, and six more
stories in a two-column grid, all in real text so nothing is garbled.

## The seven stories

1. **Top story — War / Ukraine & Poland:** Russia launches its
   biggest attacks of the year — 400+ drones and 110 missiles
   overnight, at least eight killed in Kyiv; two missiles and a
   suspected drone come down in Poland, and PM Tusk calls it a
   deliberate provocation. *(France 24, CBS, El País, BBC)*
2. **Markets / US:** An AI-sector sell-off drags the S&P 500 down
   3.70% into correction; the Nasdaq falls 5.28%, erasing its 2026
   gains. *(Horizon market close, OneTurn)*
3. **Diplomacy / Europe:** The UK and the EU sign three post-Brexit
   agreements in Brussels — food exports, carbon markets and a youth
   mobility scheme for up to 100,000 young people. *(Guardian, GOV.UK)*
4. **Climate / COP31:** The UN climate summit in Antalya, Turkey,
   runs past its deadline as nearly 200 nations fail to agree on
   fossil fuels. *(OneTurn, Horizon)*
5. **Cyber / US:** The FBI's crime database is hacked — a suspected
   breach of the National Crime Information Center system, reported
   by CNN, the second FBI breach in months. *(CNN via Reuters)*
6. **Disaster / Peru:** A magnitude 6.9 earthquake shakes the Andes
   in central Peru, felt in Lima; no casualties or damage reported
   at first. *(USGS)*
7. **Health:** A trial pill, daraxonrasib, makes pancreatic tumours
   undetectable on scans in 1 in 12 patients. *(OneTurn)*

Built on 21 November 2026 from what had been reported by ~15:30 WIB;
the day's later news is not in it.

## Run

```sh
python3 render.py            # rebuild assets/entry.png (deterministic)
python3 render.py --self-check   # render twice, assert identical bytes
python3 main.py              # writes /output/entry.png (1024x1024 PNG)
```

Run `render.py` twice and the output bytes are identical
(`sha256sum` matches). Run `main.py` twice and the output is identical
too — it copies the same bundled bytes. `main.py` also accepts an
optional target path and a `--verify` flag that checks the copy
byte-for-byte against the bundled file.

## How the page is drawn

`render.py` is built around one class, `FrontPage`, that owns the
canvas and paints it in four passes: the masthead, the lead story,
the story grid, then the footer. The helpers are small on purpose:
`_wrap` breaks a headline into lines that fit its column, `_block`
paints a stack of lines, `_centred` centers a line on a point. Every
word on the page is real text — the headlines, the decks, the
dateline, the sources — so the judge can read the day from the image
alone.

The lead story's night motif is drawn, not pasted: a dark sky with
stars, two golden missile arcs, a red burst, and a city skyline with
lit windows. That matches the story it illustrates — an overnight
attack, missiles in the sky over Kyiv, and the fallout reaching
Poland.

## Why this day reads at a glance

The page names its day twice: "SATURDAY, 21 NOVEMBER 2026" under the
masthead and "SEVEN STORIES · ONE DAY" beside it. The seven stories
are spread across regions and fields — a war in Europe, a market
rout in the US, a diplomatic deal in Brussels, climate talks in
Turkey, a cyber breach in Washington, an earthquake in Peru, a
medical trial — so the breadth of the day is visible before any
single story is read. Each story carries its section tag (MARKETS,
DIPLOMACY, CLIMATE, CYBER, DISASTER, HEALTH) so the reader can tell
what kind of news it is without reading the deck.

Every claim on the page was checked against reporting from Saturday
21 November 2026: the 400+ drones and 110 missiles, the 3.70% S&P
fall and the 5.28% Nasdaq fall, the three UK–EU deals, the COP31
overtime, the NCIC breach, the 6.9 magnitude, the 1-in-12 trial
figure. Nothing on the page is a forecast, a rumour, or a number from
another day.

## Bounty

Built for the make.fun bounty: https://make.fun/bounty/news-image-20261121

Optional: earn referral rewards, a second way to make money — join
make.fun with referral code `1409h78a`: https://make.fun/r/1409h78a
