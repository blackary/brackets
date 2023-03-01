import datetime as datetime

import numpy as np
import pandas as pd
import streamlit as st

from fetch_picks import get_matchups, get_team_ids

st.set_page_config("Make your picks", layout="wide")

matchups = get_matchups()[["team_1", "team_2"]]

# st.write(matchups)

ids = get_team_ids()

# st.write(ids)

WEST = matchups[:8]
EAST = matchups[8:16]
SOUTH = matchups[16:24]
MIDWEST = matchups[24:32]

YOUR_PICKS = []

if st.checkbox("Randomize", key="randomize"):
    if "random_seed" not in st.session_state:
        st.session_state["random_seed"] = datetime.datetime.now().microsecond

    if st.button("Re-randomize"):
        st.session_state["random_seed"] = datetime.datetime.now().microsecond


def make_next_round(input_df: pd.DataFrame) -> pd.DataFrame:
    global YOUR_PICKS

    next_round = {}
    for row in input_df.itertuples():
        if row.LEFT_WINS:
            next_round[row.Index] = row.team_1
        else:
            next_round[row.Index] = row.team_2
    YOUR_PICKS += list(next_round.values())

    # st.write(next_round)
    # Group these 8 teams into the next round, in dataframe with columns "team_1" and "team_2"
    # next_round_df = pd.DataFrame(next_round.items(), columns=["game_id", "team"])
    team_1s = list(next_round.values())[::2]
    team_2s = list(next_round.values())[1::2]

    next_round_df = pd.DataFrame({"team_1": team_1s, "team_2": team_2s})
    add_wins_col(next_round_df)

    return next_round_df


def add_wins_col(df):
    if st.session_state["randomize"]:
        np.random.seed(st.session_state["random_seed"])
        df["LEFT_WINS"] = np.random.choice([True, False], len(df))
    else:
        df["LEFT_WINS"] = True


"# Make your picks"

final_four = {}

region_names = ["West", "East", "South", "Midwest"]

for idx, region in enumerate([WEST, EAST, SOUTH, MIDWEST]):
    st.write(f"## {region_names[idx]}")
    cols = st.tabs([f"Round {i}" for i in range(1, 5)])
    add_wins_col(region)
    with cols[0]:
        output = st.experimental_data_editor(region, key=f"region_{idx}_0")
    with cols[1]:
        next_round_df = make_next_round(output)
        output2 = st.experimental_data_editor(next_round_df, key=f"region_{idx}_1")
    with cols[2]:
        next_round_df = make_next_round(output2)
        output3 = st.experimental_data_editor(next_round_df, key=f"region_{idx}_2")
    with cols[3]:
        next_round_df = make_next_round(output3)
        output4 = st.experimental_data_editor(next_round_df, key=f"region_{idx}_3")
    final_four[f"region_{idx}"] = (
        output4["team_1"].values[0]
        if output4["LEFT_WINS"].values[0]
        else output4["team_2"].values[0]
    )

# st.write(final_four)

YOUR_PICKS += list(final_four.values())

team_1s = list(final_four.values())[::2]
team_2s = list(final_four.values())[1::2]

final_four_df = pd.DataFrame({"team_1": team_1s, "team_2": team_2s})

add_wins_col(final_four_df)
# final_four_df["LEFT_WINS"] = True

st.write("# Your Final Four")

cols = st.columns(2)

with cols[0]:
    output = st.experimental_data_editor(final_four_df, key="final_four_0")
with cols[1]:
    next_round_df = make_next_round(output)
    output2 = st.experimental_data_editor(next_round_df, key="final_four_1")

winner = (
    output2["team_1"].values[0]
    if output2["LEFT_WINS"].values[0]
    else output2["team_2"].values[0]
)

YOUR_PICKS.append(winner)

st.write(f"# Your Champion: {winner}")

st.write("# Your picks")

rows = []
for idx, pick in enumerate(YOUR_PICKS):
    rows.append({"game_number": idx, "team_name": pick, "team_id": ids[pick]})

picks_df = pd.DataFrame(rows).set_index("game_number")

st.write(picks_df)

st.download_button("Download your picks", picks_df.to_csv(), file_name="your_picks.csv")
