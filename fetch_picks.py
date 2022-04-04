from typing import Dict

import pandas as pd

import requests


def _get_data(group_id: str) -> Dict:
    params = {
        "groupID": group_id,
        "start": "0",
        "length": "10000",
    }

    response = requests.get(
        "https://fantasy.espncdn.com/tournament-challenge-bracket/2022/en/api/v7/group",
        params=params,
    )

    return response.json()


def get_name(group_id) -> str:
    data = _get_data(group_id)
    return data["g"]["n"]


def get_picks(group_id: str) -> pd.DataFrame:
    data = _get_data(group_id)
    brackets = data["g"]["e"]

    all_picks = []

    for bracket in brackets:
        name = bracket["n_e"]
        owner = bracket["n_m"]
        picks = bracket["ps"]
        row = {
            "name": name,
            "owner": owner,
            "points": bracket["p"],
            "max_point": bracket["max"],
            "percentage": bracket["pct"],
        }
        for idx, pick in enumerate(picks.split("|")):
            key = f"pick {idx}"
            row[key] = int(pick)
        all_picks.append(row)

    df = pd.DataFrame(all_picks).sort_values("points", ascending=False)

    return df


def get_matchups() -> pd.DataFrame:
    url = (
        "https://fantasy.espncdn.com/tournament-challenge-bracket/2022/en/api/matchups"
    )

    data = requests.get(url).json()

    matchups = []

    for row in data["m"]:
        team1, team2 = row["o"]
        team1["n"]
        team2["n"]

        matchups.append({"team 1": team1["n"], "team 2": team2["n"]})

    return pd.DataFrame(matchups)
