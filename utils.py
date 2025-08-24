import pandas as pd
import functools
import os
from urllib.request import urlretrieve
from common import ROOT_PATH
from typing import Union


def style_rankings(styler, title, columns):
    styler.set_caption(title)
    styler.background_gradient(axis=None, vmin=1, vmax=3)
    styler.hide()  # Hide index
    styler.format(precision=1)
    styler.format_index(columns.get, axis=1)
    return styler


ROOT_NFL_VERSE_FILES = "https://github.com/nflverse/nflverse-data/releases/download/"

ROOT_NFL_VERSE_PLAYER_STATS_FILES = "player_stats/"

ROOT_NFL_VERSE_PBP_PARTICIPATION_FILES = "pbp_participation/"

ROOT_NFL_VERSE_PBP_FILES = "pbp/"

ROOT_NFL_VERSE_PLAYERS_FILES = "players/"

ROOT_NFL_VERSE_CONTRACT_FILES = "contracts/"


def get_or_retrieve_file(local_path, nflverse_dir, file):
    if not os.path.isfile(local_path):
        print(f"Retrieving {file} from NFLVerse Repository")
        urlretrieve(
            f"{ROOT_NFL_VERSE_FILES}{nflverse_dir}{file}",
            local_path,
        )
    return pd.read_parquet(local_path)


def get_contract_data():
    """
    Returns the source of truth for player contract data
    """
    file = "historical_contracts.parquet"
    local_path = f"{ROOT_PATH}/nflverse_data/{ROOT_NFL_VERSE_CONTRACT_FILES}{file}"
    return get_or_retrieve_file(local_path, ROOT_NFL_VERSE_CONTRACT_FILES, file)


def get_stats(
    years: Union[list, int, str], nflverse_dir: str, file_template: str
) -> pd.DataFrame:
    if not isinstance(years, list):
        years = [str(years)]

    data_frames = []
    for year in years:
        file = str.format(file_template, year)
        local_path = f"{ROOT_PATH}/nflverse_data/{nflverse_dir}{file}"
        data_frames.append(get_or_retrieve_file(local_path, nflverse_dir, file))
    return pd.concat(data_frames)


def get_def_player_stats(years):
    return get_stats(
        years, ROOT_NFL_VERSE_PLAYER_STATS_FILES, "player_stats_def_{0}.parquet"
    )


def get_pbp_participation_stats(years):
    return get_stats(
        years, ROOT_NFL_VERSE_PBP_PARTICIPATION_FILES, "pbp_participation_{0}.parquet"
    )


def get_pbp_data(years):
    return get_stats(years, ROOT_NFL_VERSE_PBP_FILES, "play_by_play_{0}.parquet")


def get_players_info():
    """Returns the source of truth for player metadata"""
    file = "players.parquet"
    local_path = f"{ROOT_PATH}/nflverse_data/{ROOT_NFL_VERSE_PLAYERS_FILES}{file}"
    return get_or_retrieve_file(local_path, ROOT_NFL_VERSE_PLAYERS_FILES, file)


def get_off_player_stats(years):
    return get_stats(
        years, ROOT_NFL_VERSE_PLAYER_STATS_FILES, "player_stats_{0}.parquet"
    )


@functools.cache
def get_player_id_from_play_metadata(
    player_tag: str, home_team: str, away_team: str, season: str
):
    """
    WIP: THIS DOESN'T WORK YET
    Returns the player id (gsis_id) from the players df based on pbp data like the description player tag (##-F.Last) the home team, away team and jersey number
    """
    try:
        last_name = player_tag.split(".")[1]
        first_initial = player_tag.split(".")[0].split("-")[1]
        jersey_number = int(player_tag.split("-")[0])
    except Exception as e:
        print("Error parsing player tag: ", player_tag, e)
        return None

    players_df = get_players_info()
    possible_players = players_df[
        (players_df["last_name"] == last_name)
        & (
            (players_df["first_name"].str.startswith(first_initial))
            | (players_df["display_name"].str.startswith(first_initial))
            | (players_df["football_name"].str.startswith(first_initial))
        )
        & (players_df["entry_year"].notna())
    ]
    if possible_players.empty:
        return None
    elif possible_players.shape[0] == 1:
        return possible_players.iloc[0]["gsis_id"]
    possible_ids = possible_players["gsis_id"].unique()
    # If more than one possible match then we need to do more filtering
    off_df = get_off_player_stats([season])[["player_name", "recent_team", "player_id"]]
    off_df["team"] = off_df["recent_team"]
    def_df = get_def_player_stats([season])[["player_name", "team", "player_id"]]
    off_def_df = pd.concat([off_df, def_df])
    print(
        off_def_df[off_def_df["player_name"].str.contains(last_name)]
        .groupby("player_id")
        .nth(0)
    )
    player = off_def_df[
        (off_def_df["player_name"].str.contains(last_name))
        & (off_def_df["team"].isin([home_team, away_team]))
        & (off_def_df["player_name"].str.startswith(first_initial))
    ]["player_id"].unique()
    if len(player) == 1:
        return player[0]
    print("Can't Resolve: ", player_tag, home_team, away_team, season)
    return None
