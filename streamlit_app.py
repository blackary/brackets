import base64

import streamlit as st
from st_pages import add_page_title, show_pages_from_config

from fetch_picks import get_matchups, get_name, get_picks

st.set_page_config(
    page_title="Tournament Challenge Picks", layout="wide", page_icon="basketball"
)

add_page_title()

show_pages_from_config()

st.title("Get picks in a usable format")

"Paste in group id or url (e.g. https://fantasy.espn.com/tournament-challenge-bracket/2022/en/group?groupID=...)"

params = st.experimental_get_query_params()

if "group_id" in params:
    group_id = params["group_id"][0]
else:
    group_id = "4337635"

url = st.text_input("Group url / group id", value=group_id)

if not url:
    st.info("Put in url or group id")
    st.stop()

group_id = url.split("=")[-1]  # may or may not be right

st.experimental_set_query_params(group_id=group_id)

name = get_name(group_id)

f"## {name}"

picks = get_picks(group_id)

picks

data = base64.b64encode(picks.to_csv(index=False).encode()).decode()

st.download_button(
    data=picks.to_csv().encode("utf-8"), label="Download as csv", file_name="picks.csv"
)

"## Matchups"

matchups = get_matchups()

matchups
