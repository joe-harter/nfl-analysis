import pandas as pd
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

ROOT_NFL_VERSE_PLAYERS_FILES = "players/"


def get_or_retrieve_file(local_path, nflverse_dir, file):
    if not os.path.isfile(local_path):
        print(f"Retrieving {file} from NFLVerse Repository")
        urlretrieve(
            f"{ROOT_NFL_VERSE_FILES}{nflverse_dir}{file}",
            local_path,
        )
    return pd.read_parquet(local_path)


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


def get_players_info():
    """Returns the source of truth for player metadata"""
    file = "players.parquet"
    local_path = f"{ROOT_PATH}/nflverse_data/{ROOT_NFL_VERSE_PLAYERS_FILES}{file}"
    return get_or_retrieve_file(local_path, ROOT_NFL_VERSE_PLAYERS_FILES, file)
