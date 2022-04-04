import base64

import streamlit as st

from fetch_picks import get_picks

st.set_page_config(page_title="Tournament Challenge Picks", layout="wide", page_icon="basketball")

st.title("Get picks in a usable format")

"Paste in group id or url (e.g. https://fantasy.espn.com/tournament-challenge-bracket/2022/en/group?groupID=...)"

url = st.text_input("Group url / group id")

if not url:
    st.info("Put in url or group id")
    st.stop()

group_id = url.split("=")[-1] # may or may not be right

picks = get_picks(group_id)

picks

data = base64.b64encode(picks.to_csv(index=False).encode()).decode()

st.download_button(data=picks.to_csv().encode("utf-8"), label="Download as csv", file_name="picks.csv")
