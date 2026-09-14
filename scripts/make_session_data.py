"""scripts/make_session_data.py - Generate synthetic player session data.

Author: Josiah Davis
Date: 2026-09-14

WHY THIS FILE EXISTS:

The CSV this script writes is synthetic. Publishing numbers without
publishing the code that made them asks the reader to take them on faith.
The script is seeded, so running it reproduces the same file every time.

WHY THE DATA IS SYNTHETIC:

I spent four years in casino and iGaming analytics. None of that data can
go in a public repository, and anything committed to Git stays in the
history even after the file is deleted. Generating realistic structure is
how you demonstrate a pipeline in a regulated industry without creating a
problem you cannot undo.

WHAT IS BUILT IN ON PURPOSE:

Net revenue is negative on many sessions, because players win. That matters
for the statistics: it means the minimum is a large negative number and the
standard deviation dwarfs the mean.

RUN (only needed to regenerate the raw data):

  uv run python scripts/make_session_data.py
"""

import csv
import random
from datetime import date, timedelta
from pathlib import Path

# A fixed seed makes this reproducible. Without it, every run would
# produce different numbers and the results in the README would drift.
random.seed(24)

OUT_DIR = Path("data") / "raw"
OUT_FILE = OUT_DIR / "player_sessions.csv"

PLAYER_COUNT = 900
START_DATE = date(2025, 1, 1)

CHANNELS = ["Affiliate", "Paid Search", "Paid Social", "Organic", "Retail Crossover"]
GAMES = ["Slots", "Sportsbook", "Live Dealer", "Table Games", "Bingo"]
DEVICES = ["iOS App", "Android App", "Mobile Web", "Desktop"]

# House edge by vertical. Slots hold more than table games, which is why
# the vertical a player prefers changes what they are worth.
HOUSE_EDGE = {
    "Slots": 0.055,
    "Sportsbook": 0.042,
    "Live Dealer": 0.021,
    "Table Games": 0.018,
    "Bingo": 0.070,
}


def main() -> None:
    """Write the synthetic session file to data/raw/."""
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    rows = []
    session_id = 0

    for player_number in range(1, PLAYER_COUNT + 1):
        player_id = f"P{100000 + player_number}"
        signup = START_DATE + timedelta(days=random.randint(0, 180))
        channel = random.choice(CHANNELS)

        # Most players play a handful of times and stop. A few play a lot.
        # A skewed count is closer to reality than a uniform one.
        session_count = max(1, int(random.lognormvariate(1.2, 0.9)))

        day = 0
        for _ in range(session_count):
            session_id += 1
            game = random.choice(GAMES)

            minutes = max(1, int(random.lognormvariate(3.0, 0.75)))
            bets = max(1, int(minutes * random.uniform(0.4, 3.2)))

            # Amount wagered, then the operator's share of it, then noise.
            # The noise is what makes individual sessions unpredictable.
            handle = bets * random.uniform(0.8, 18.0)
            revenue = handle * HOUSE_EDGE[game] + random.gauss(0, handle * 0.28)

            rows.append(
                {
                    "session_id": f"S{session_id:06d}",
                    "player_id": player_id,
                    "acquisition_channel": channel,
                    "session_date": (signup + timedelta(days=day)).isoformat(),
                    "days_since_signup": day,
                    "game_category": game,
                    "device": random.choice(DEVICES),
                    "session_minutes": minutes,
                    "bets_placed": bets,
                    "net_revenue_usd": round(revenue, 2),
                }
            )

            day += random.choice([1, 1, 2, 3, 5, 8, 14])

    # newline="" and lineterminator="\n" keep the file LF, which is what
    # the repository's pre-commit hooks expect.
    with OUT_FILE.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=[
                "session_id",
                "player_id",
                "acquisition_channel",
                "session_date",
                "days_since_signup",
                "game_category",
                "device",
                "session_minutes",
                "bets_placed",
                "net_revenue_usd",
            ],
            lineterminator="\n",
        )
        writer.writeheader()
        writer.writerows(rows)

    print(f"Wrote {len(rows)} sessions for {PLAYER_COUNT} players to {OUT_FILE}")


if __name__ == "__main__":
    main()
