import pandas as pd
import streamlit as st

from fetch_picks import get_matchups, get_team_ids

matchups = get_matchups()

# st.write(matchups)

ids = get_team_ids()

# st.write(ids)

WEST = matchups[:8]
EAST = matchups[8:16]
SOUTH = matchups[16:24]
MIDWEST = matchups[24:32]


def make_next_round(input_df: pd.DataFrame) -> pd.DataFrame:
    next_round = {}
    for row in input_df.itertuples():
        if row.LEFT_WINS:
            next_round[row.Index] = row.team_1
        else:
            next_round[row.Index] = row.team_2
    # st.write(next_round)
    # Group these 8 teams into the next round, in dataframe with columns "team_1" and "team_2"
    # next_round_df = pd.DataFrame(next_round.items(), columns=["game_id", "team"])
    team_1s = list(next_round.values())[::2]
    team_2s = list(next_round.values())[1::2]

    next_round_df = pd.DataFrame({"team_1": team_1s, "team_2": team_2s})

    next_round_df["LEFT_WINS"] = True

    return next_round_df


"# Make your picks"

final_four = {}

region_names = ["West", "East", "South", "Midwest"]

for idx, region in enumerate([WEST, EAST, SOUTH, MIDWEST]):
    st.write(f"## {region_names[idx]}")
    cols = st.columns(4)
    region["LEFT_WINS"] = True
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

team_1s = list(final_four.values())[::2]
team_2s = list(final_four.values())[1::2]

final_four_df = pd.DataFrame({"team_1": team_1s, "team_2": team_2s})

final_four_df["LEFT_WINS"] = True

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

st.write(f"# Your Champion: {winner}")
