from utils import get_player_id_from_play_metadata
import pytest


@pytest.mark.parametrize(
    "tag,home_team,away_team,season,expected",
    [
        pytest.param("70-C.Hubbard", "PHI", "NYG", 2024, "00-0029963"),
        pytest.param("8-L.Jackson", "BAL", "CIN", 2018, "00-0034796"),
        pytest.param("27-D.Washington", "CIN", "NO", 2018, "00-0032450"),
        pytest.param("7-T.Hill", "CIN", "NO", 2018, "00-0033357"),
        pytest.param("30-M.Carter", "CAR", "NYJ", 2021, "00-0036501"),
    ],
)
def test_get_player_id_from_play_metadata(tag, home_team, away_team, season, expected):
    result = get_player_id_from_play_metadata(tag, home_team, away_team, season)
    assert result == expected
