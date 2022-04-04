from typing import Dict

import pandas as pd

import requests

headers = {
    "authority": "fantasy.espncdn.com",
    "accept": "*/*",
    "sec-gpc": "1",
    "origin": "https://fantasy.espn.com",
    "sec-fetch-site": "cross-site",
    "sec-fetch-mode": "cors",
    "sec-fetch-dest": "empty",
    "referer": "https://fantasy.espn.com/",
    "accept-language": "en-US,en;q=0.9",
}


def _get_data(group_id: str) -> Dict:
    params = {
        "groupID": group_id,
        "start": "0",
        "length": "10000",
    }

    response = requests.get(
        "https://fantasy.espncdn.com/tournament-challenge-bracket/2022/en/api/v7/group",
        headers=headers,
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
