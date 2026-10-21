#!/usr/bin/env python3
"""Generates test-epg.xml: guide data for the 4 public test channels of test-playlist.m3u.

Programmes are generic placeholders ("Test programme ...", no real shows) every 30-60 minutes, from 1 day ago to 7 days ahead
(UTC), so the guide always has a programme on air now and in the next days. Run daily by .github/workflows/epg.yml.
"""
import datetime as dt
from xml.sax.saxutils import escape

CHANNELS = [
    ("test1", "Test channel 1"),
    ("test2", "Test channel 2"),
    ("test3", "Test channel 3"),
    ("test4", "Test channel 4"),
]
THEMES = ["Morning test show", "Sample film", "Test news bulletin", "Demo documentary", "Test music hour",
          "Open movie sample", "Test magazine", "Demo cartoon", "Test sports-free hour", "Sample series episode"]
FMT = "%Y%m%d%H%M%S +0000"


def main() -> None:
    now = dt.datetime.now(dt.timezone.utc).replace(minute=0, second=0, microsecond=0)
    start0 = (now - dt.timedelta(days=1)).replace(hour=0)
    end = now + dt.timedelta(days=7)
    out = ['<?xml version="1.0" encoding="UTF-8"?>', '<tv generator-info-name="txiptv-privacy test epg">']
    for cid, name in CHANNELS:
        out.append(f'  <channel id="{cid}"><display-name>{escape(name)}</display-name></channel>')
    for ci, (cid, _) in enumerate(CHANNELS):
        t = start0
        n = 0
        while t < end:
            # 30, 45 or 60 minutes, different per channel so the grid blocks do not line up
            mins = (30, 60, 45, 60, 30)[(n + ci) % 5]
            stop = t + dt.timedelta(minutes=mins)
            theme = THEMES[(n * 3 + ci) % len(THEMES)]
            title = f"{theme} #{n + 1}"
            desc = f"Generic placeholder programme on test channel {ci + 1}. Used only to test the TV guide."
            out.append(
                f'  <programme start="{t.strftime(FMT)}" stop="{stop.strftime(FMT)}" channel="{cid}">'
                f'<title lang="en">{escape(title)}</title><desc lang="en">{escape(desc)}</desc></programme>'
            )
            t = stop
            n += 1
    out.append('</tv>')
    with open("test-epg.xml", "w", encoding="utf-8") as f:
        f.write("\n".join(out) + "\n")


if __name__ == "__main__":
    main()
