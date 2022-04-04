import requests
import pandas as pd

headers = {
    'authority': 'fantasy.espncdn.com',
    'accept': '*/*',
    'sec-gpc': '1',
    'origin': 'https://fantasy.espn.com',
    'sec-fetch-site': 'cross-site',
    'sec-fetch-mode': 'cors',
    'sec-fetch-dest': 'empty',
    'referer': 'https://fantasy.espn.com/',
    'accept-language': 'en-US,en;q=0.9',
}

def get_picks(group_id: str) -> pd.DataFrame:
    params = {
        'groupID': group_id,
        'start': '0',
        'length': '10000',
    }

    response = requests.get('https://fantasy.espncdn.com/tournament-challenge-bracket/2022/en/api/v7/group', headers=headers, params=params)

    brackets = response.json()['g']['e']

    all_picks = []

    for bracket in brackets:
        name = bracket["n_e"]
        picks = bracket["ps"]
        row = {"name": name}
        for idx, pick in enumerate(picks.split("|")):
            key = f"pick {idx}"
            row[key] = int(pick)
        all_picks.append(row)


    df = pd.DataFrame(all_picks)

    return df
