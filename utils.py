import pandas as pd
import os
from urllib.request import urlretrieve
from common import ROOT_PATH


def style_rankings(styler, title, columns):
    styler.set_caption(title)
    styler.background_gradient(axis=None, vmin=1, vmax=3)
    styler.hide()  # Hide index
    styler.format(precision=1)
    styler.format_index(columns.get, axis=1)
    return styler


def get_def_player_stats(year):
    file = f"player_stats_def_{year}.parquet"
    local_path = f"{ROOT_PATH}/nflverse_data/player_stats/{file}"
    if not os.path.isfile(local_path):
        print("Retrieving file from NFLVerse Repository")
        urlretrieve(
            f"https://github.com/nflverse/nflverse-data/releases/download/player_stats/{file}",
            local_path,
        )

    return pd.read_parquet(local_path)
