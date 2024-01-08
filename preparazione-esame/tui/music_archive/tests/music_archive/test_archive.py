import pytest
from typeguard import TypeCheckError
from valid8 import ValidationError

from music_archive.archive import Archive
from music_archive.domain import *


@pytest.fixture(scope="function")
def empty_archive_fixture():
    yield Archive()


@pytest.fixture(scope="module")
def songs_fixture():
    yield [
        Song(Author("The Police"), Title("Every Little Thing She Does Is Magic"), Genre("New Wave"), Duration.parse("4:22")),
        Song(Author("Alice In Chains"), Title("No Excuses"), Genre("Acoustic Rock"), Duration.create(4, 15)),
        Song(Author("Lucio Battisti"), Title("Neanche un minuto di non amore"), Genre("Pop"), Duration.parse("5:22"))
    ]


def test_add_song_with_correct_values_works_correctly(empty_archive_fixture, songs_fixture):
    empty_archive_fixture.add_song(songs_fixture[0])
    assert empty_archive_fixture.songs() == 1 and empty_archive_fixture.song(0) == songs_fixture[0]


def test_add_song_with_incorrect_type_parameter_raises_exception(empty_archive_fixture):
    with pytest.raises(TypeCheckError):
        empty_archive_fixture.add_song("invalid lol")


def test_remove_song_works_correctly(empty_archive_fixture, songs_fixture):
    empty_archive_fixture.add_song(songs_fixture[0])
    empty_archive_fixture.add_song(songs_fixture[1])
    empty_archive_fixture.remove_song(0)
    assert empty_archive_fixture.song(0) == songs_fixture[1]


def test_remove_song_with_incorrect_type_argument_raises_exception(empty_archive_fixture, songs_fixture):
    empty_archive_fixture.add_song(songs_fixture[0])
    with pytest.raises(TypeCheckError):
        empty_archive_fixture.remove_song("notok")


def test_remove_song_with_out_of_bound_argument_raises_exception(empty_archive_fixture):
    with pytest.raises(ValidationError):
        empty_archive_fixture.remove_song(0)


def test_sort_by_author_works_correctly(empty_archive_fixture, songs_fixture):
    empty_archive_fixture.add_song(songs_fixture[0])
    empty_archive_fixture.add_song(songs_fixture[1])
    empty_archive_fixture.add_song(songs_fixture[2])
    empty_archive_fixture.sort_by_author()
    assert (empty_archive_fixture.song(0) == songs_fixture[1] and
            empty_archive_fixture.song(1) == songs_fixture[2] and
            empty_archive_fixture.song(2) == songs_fixture[0])


def test_sort_by_title_works_correctly(empty_archive_fixture, songs_fixture):
    empty_archive_fixture.add_song(songs_fixture[0])
    empty_archive_fixture.add_song(songs_fixture[1])
    empty_archive_fixture.add_song(songs_fixture[2])
    empty_archive_fixture.sort_by_title()
    assert (empty_archive_fixture.song(0) == songs_fixture[0] and
            empty_archive_fixture.song(1) == songs_fixture[2] and
            empty_archive_fixture.song(2) == songs_fixture[1])


def test_sort_by_genre_works_correctly(empty_archive_fixture, songs_fixture):
    empty_archive_fixture.add_song(songs_fixture[0])
    empty_archive_fixture.add_song(songs_fixture[1])
    empty_archive_fixture.add_song(songs_fixture[2])
    empty_archive_fixture.sort_by_genre()
    assert (empty_archive_fixture.song(0) == songs_fixture[1] and
            empty_archive_fixture.song(1) == songs_fixture[0] and
            empty_archive_fixture.song(2) == songs_fixture[2])


def test_sort_by_duration_works_correctly(empty_archive_fixture, songs_fixture):
    empty_archive_fixture.add_song(songs_fixture[0])
    empty_archive_fixture.add_song(songs_fixture[1])
    empty_archive_fixture.add_song(songs_fixture[2])
    empty_archive_fixture.sort_by_duration()
    assert (empty_archive_fixture.song(0) == songs_fixture[1] and
            empty_archive_fixture.song(1) == songs_fixture[0] and
            empty_archive_fixture.song(2) == songs_fixture[2])


def test_sorts_on_empty_archive_have_no_effect(empty_archive_fixture):
    empty_archive_fixture.sort_by_author()
    assert empty_archive_fixture.songs() == 0
    empty_archive_fixture.sort_by_title()
    assert empty_archive_fixture.songs() == 0
    empty_archive_fixture.sort_by_genre()
    assert empty_archive_fixture.songs() == 0
    empty_archive_fixture.sort_by_duration()
    assert empty_archive_fixture.songs() == 0
