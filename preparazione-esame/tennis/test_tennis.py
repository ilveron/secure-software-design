import subprocess

import pytest

TEST_FILE = "./tennis.py"


def run(the_input: str):
    res = subprocess.run(["python", TEST_FILE], input='\n'.join(list(the_input)).encode(),
                         capture_output=True)
    return res.stdout.decode()


@pytest.mark.parametrize("the_input", [
    "SSSS",
    "RSSSS",
    "RRSSSS",
    "RRRSSSSS",
    "RSRRSSSS",
    "SRSSS",
    "SRSRSS",
    "SRSRSRSS",
    "SRSRSRSRSS",
    "SRSRSRSRRSSS",
])
def test_game_win_by_serving_player(the_input):
    assert "End of the game: Serving player win" in run(the_input=the_input)


@pytest.mark.parametrize("the_input", [
    "RRRR",
    "SRRRR",
    "SSRRRR",
    "SSSRRRRR",
    "SRSSRRRR",
    "RSRRR",
    "RSRSRR",
    "RSRSRSRR",
    "RSRSRSRSRR",
    "RSRSRSRSSRRR",
])
def test_game_win_by_receiving_player(the_input):
    assert "End of the game: Receiving player win" in run(the_input=the_input)


@pytest.mark.parametrize("the_input", [
    "RS",
    "SR",
])
def test_15_all(the_input):
    assert "Running score: 15-all" in run(the_input=the_input)


@pytest.mark.parametrize("the_input", [
    "RSSR",
    "RSRS",
    "SRRS",
    "SRSR",
])
def test_30_all(the_input):
    assert "Running score: 30-all" in run(the_input=the_input)


@pytest.mark.parametrize("the_input", [
    "RSSSRR",
    "RSSSRR",
])
def test_deuce(the_input):
    assert "Running score: deuce" in run(the_input=the_input)


@pytest.mark.parametrize("the_input", [
    "RSSSRRS",
    "SSSRRRS",
    "SSSRRRRSS",
])
def test_ad_in(the_input):
    assert "Running score: ad-in" in run(the_input=the_input)


@pytest.mark.parametrize("the_input", [
    "RSSSRRR",
    "SSSRRRR",
    "SSSRRRSRR",
])
def test_ad_in(the_input):
    assert "Running score: ad-out" in run(the_input=the_input)


@pytest.mark.parametrize("the_input", [
    "A",
    "0",
    "!",
    "RS!",
    "RS+",
])
def test_wrong_values_are_ignored(the_input):
    assert "Wrong value ignored!" in run(the_input=the_input)
