import datetime as datetime

import streamlit as st

from fetch_picks import get_logos, get_matchups

st.set_page_config("Pick your bracket by Logos", layout="wide", page_icon="🖼️")

st.title("🖼️ Pick your bracket by Logos")

logos = get_logos()

matchups = get_matchups()[["team_1", "team_2"]]

st.write(get_matchups())

if "pick_num" not in st.session_state:
    st.session_state["pick_num"] = 62


for i in range(st.session_state["pick_num"] + 1):
    try:
        logo1 = logos[matchups.iloc[i]["team_1"]]
    except KeyError:
        logo1 = None
    try:
        logo2 = logos[matchups.iloc[i]["team_2"]]
    except KeyError:
        logo2 = None
    if logo1:
        st.image(logo1)
    else:
        st.write("???")
    if logo2:
        st.image(logo2)
    else:
        st.write("???")

    st.write(matchups.iloc[i]["team_1"], "vs", matchups.iloc[i]["team_2"])
    st.write("")
