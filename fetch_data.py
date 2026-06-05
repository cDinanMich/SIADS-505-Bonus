"""
fetch_data.py
Fetches NFL team standings from the ESPN public API and saves to data/nfl_stats.json.
No API key required.

Usage:
    python fetch_data.py
"""

import json
import os
import urllib.request
import urllib.error
from datetime import datetime

STANDINGS_URL = "https://site.api.espn.com/apis/v2/sports/football/nfl/standings"
OUTPUT_PATH = os.path.join(os.path.dirname(__file__), "data", "nfl_stats.json")

TEAM_COLORS = {
    "ARI": "#97233F", "ATL": "#A71930", "BAL": "#241773", "BUF": "#00338D",
    "CAR": "#0085CA", "CHI": "#0B162A", "CIN": "#FB4F14", "CLE": "#311D00",
    "DAL": "#003594", "DEN": "#FB4F14", "DET": "#0076B6", "GB":  "#203731",
    "HOU": "#03202F", "IND": "#002C5F", "JAX": "#006778", "KC":  "#E31837",
    "LAC": "#0080C6", "LAR": "#003594", "LV":  "#000000", "MIA": "#008E97",
    "MIN": "#4F2683", "NE":  "#002244", "NO":  "#D3BC8D", "NYG": "#0B2265",
    "NYJ": "#125740", "PHI": "#004C54", "PIT": "#FFB612", "SF":  "#AA0000",
    "SEA": "#002244", "TB":  "#D50A0A", "TEN": "#4B92DB", "WAS": "#5A1414",
}


def fetch_standings():
    print(f"Fetching NFL standings from ESPN API...")
    req = urllib.request.Request(
        STANDINGS_URL,
        headers={"User-Agent": "Mozilla/5.0 (compatible; nfl-dashboard/1.0)"}
    )
    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            raw = json.loads(response.read().decode("utf-8"))
    except urllib.error.URLError as e:
        raise SystemExit(f"Network error: {e}")
    except json.JSONDecodeError as e:
        raise SystemExit(f"Failed to parse API response: {e}")

    teams = []

    for conference in raw.get("children", []):
        conf_name = conference.get("name", "")  # AFC or NFC
        conf_abbr = conference.get("abbreviation", "")

        for division in conference.get("children", []):
            div_name = division.get("name", "")

            for entry in division.get("standings", {}).get("entries", []):
                team_data = entry.get("team", {})
                abbr = team_data.get("abbreviation", "")
                stats_raw = {s["name"]: s for s in entry.get("stats", [])}

                def stat(key, default=0):
                    s = stats_raw.get(key, {})
                    return s.get("value", default)

                wins         = int(stat("wins"))
                losses       = int(stat("losses"))
                ties         = int(stat("ties"))
                games_played = wins + losses + ties
                win_pct      = round(stat("winPercent"), 3)
                pts_for      = int(stat("pointsFor"))
                pts_against  = int(stat("pointsAgainst"))
                pt_diff      = pts_for - pts_against
                streak       = stats_raw.get("streak", {}).get("displayValue", "—")
                home_record  = stats_raw.get("Home", {}).get("displayValue", "—")
                away_record  = stats_raw.get("Away", {}).get("displayValue", "—")

                teams.append({
                    "abbr":        abbr,
                    "name":        team_data.get("displayName", abbr),
                    "shortName":   team_data.get("shortDisplayName", abbr),
                    "logo":        next(
                                     (l["href"] for l in team_data.get("logos", [])
                                      if "scoreboard" in l.get("rel", [])),
                                     team_data.get("logos", [{}])[0].get("href", "") if team_data.get("logos") else ""
                                   ),
                    "color":       TEAM_COLORS.get(abbr, "#1a1a2e"),
                    "conference":  conf_name,
                    "confAbbr":    conf_abbr,
                    "division":    div_name,
                    "wins":        wins,
                    "losses":      losses,
                    "ties":        ties,
                    "gamesPlayed": games_played,
                    "winPct":      win_pct,
                    "ptsFor":      pts_for,
                    "ptsAgainst":  pts_against,
                    "ptDiff":      pt_diff,
                    "streak":      streak,
                    "homeRecord":  home_record,
                    "awayRecord":  away_record,
                })

    teams.sort(key=lambda t: (-t["wins"], t["losses"]))

    output = {
        "fetchedAt": datetime.utcnow().isoformat() + "Z",
        "source":    STANDINGS_URL,
        "teams":     teams,
    }

    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "w") as f:
        json.dump(output, f, indent=2)

    print(f"Saved {len(teams)} teams → {OUTPUT_PATH}")
    return output


if __name__ == "__main__":
    data = fetch_standings()
    print(f"\nSample (first 3 teams):")
    for t in data["teams"][:3]:
        print(f"  {t['abbr']:4s}  {t['wins']}-{t['losses']}  "
              f"PF:{t['ptsFor']:4d}  PA:{t['ptsAgainst']:4d}  DIFF:{t['ptDiff']:+4d}")
