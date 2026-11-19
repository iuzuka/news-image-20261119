[![make.fun · news-image-20261119](https://make.fun/badge/news-image-20261119.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![rank](https://make.fun/badge/news-image-20261119/iuzuka/news-image-20261119/rank.svg)](https://make.fun/bounty/news-image-20261119/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![reward](https://make.fun/badge/news-image-20261119/iuzuka/news-image-20261119/reward.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)

# The World in One Page — Thursday 19 November 2026

One image summing up the world's news of Thursday 19 November 2026, as a
newspaper front page: `main.ts` copies `entry.png` to `/output/entry.png`.

## The day's news (researched 19 Nov 2026)

- **Lead — APEC summit, Shenzhen:** the first-ever Trump–Xi–Putin trilateral
  meeting opens; nuclear arms and AI on the agenda.
- **Gaming:** Grand Theft Auto VI begins its global rollout; gamers return to
  Vice City on PlayStation 5 and Xbox.
- **Business:** Anthropic prices its Nasdaq debut as ANT, one of the biggest
  IPOs ever, with Amazon and Google among its backers.
- **Law:** the ICJ delivers its verdict in The Gambia v. Myanmar — the first
  time a state could be found guilty of genocide.
- **Also:** Crimea bridge hit again; Israeli tanks cross the Gaza ceasefire
  line; Cyclone Akvan nears India's east coast; Fed minutes point to more
  rate hikes; oil falls, WTI $83.26; a Van Gogh sells for a record $190.4m;
  Voyager 1 passes a light-day from Earth.

## How it was built

`draw_news19.py` (PIL) composites two generated press-style illustrations
(`assets/*.webp`) with crisp programmatic typesetting — no AI-generated text.
The illustrations picture the events; they are not the events themselves.
Rebuild with `python3 draw_news19.py`; it writes a 1024x1024 PNG under 1 MiB.
