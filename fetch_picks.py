from __future__ import annotations

import pandas as pd
import streamlit as st

import requests


def _get_data(group_id: str) -> dict:
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


@st.cache_data(ttl=60 * 60 * 24)
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


@st.cache_data(ttl=60 * 60 * 24)
def _matchups():
    url = (
        "https://fantasy.espncdn.com/tournament-challenge-bracket/2022/en/api/matchups"
    )

    data = requests.get(url).json()

    return data


def get_matchups() -> pd.DataFrame:
    data = _matchups()

    matchups = []

    for row in data["m"]:
        team1, team2 = row["o"]
        team1["n"]
        team2["n"]

        game_id = row["id"]
        matchups.append(
            {"team_1": team1["n"], "team_2": team2["n"], "game_id": game_id}
        )

    return pd.DataFrame(matchups).set_index("game_id").sort_index()


def get_team_ids() -> dict[str, int]:
    data = _matchups()

    teams = {}

    for row in data["m"]:
        team1, team2 = row["o"]
        teams[team1["n"]] = team1["id"]
        teams[team2["n"]] = team2["id"]

    return teams
