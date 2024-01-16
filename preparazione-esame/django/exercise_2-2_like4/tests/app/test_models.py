import random

import pytest
from django.core.exceptions import ValidationError
from mixer.backend.django import mixer
from app.models import Song


def test_song_author_of_length_101_raises_exception(db):
    song = mixer.blend(Song, author='a' * 101)
    with pytest.raises(ValidationError):
        song.full_clean(exclude=['title', 'genre', 'duration_in_seconds'])


def test_song_title_of_length_101_raises_exception(db):
    song = mixer.blend(Song, title='a' * 101)
    with pytest.raises(ValidationError):
        song.full_clean(exclude=['author', 'genre', 'duration_in_seconds'])


def test_song_genre_of_length_11_raises_exception(db):
    song = mixer.blend(Song, genre='a' * 11)
    with pytest.raises(ValidationError):
        song.full_clean(exclude=['author', 'title', 'duration_in_seconds'])


def test_song_strings_of_length_0_raises_exception(db):
    # first with author
    song = mixer.blend(Song, author='')
    with pytest.raises(ValidationError):
        song.full_clean(exclude=['title', 'genre', 'duration_in_seconds'])
    # then with title
    song = mixer.blend(Song, title='')
    with pytest.raises(ValidationError):
        song.full_clean(exclude=['author', 'genre', 'duration_in_seconds'])
    # then with genre
    song = mixer.blend(Song, genre='')
    with pytest.raises(ValidationError):
        song.full_clean(exclude=['author', 'title', 'duration_in_seconds'])


@pytest.mark.parametrize('test_author', [
    'a',
    'a' * 100,
    "this is a test author",
    "this is a test author with numbers 123",
])
def test_song_author_of_correct_length_creates_object(db, test_author):
    song = mixer.blend(Song, author=test_author)
    song.full_clean(exclude=['title', 'genre', 'duration_in_seconds'])


@pytest.mark.parametrize('test_str', [
    'abcd!damnitswrong',
    '#$%&*()',
    '0h1t1s4t3st?'
])
def test_song_strings_with_special_characters_raises_exception(db, test_str):
    song = mixer.blend(Song, author=test_str)
    with pytest.raises(ValidationError):
        song.full_clean(exclude=['title', 'genre', 'duration_in_seconds'])

    song = mixer.blend(Song, title=test_str)
    with pytest.raises(ValidationError):
        song.full_clean(exclude=['author', 'genre', 'duration_in_seconds'])

    song = mixer.blend(Song, genre=test_str)
    with pytest.raises(ValidationError):
        song.full_clean(exclude=['author', 'title', 'duration_in_seconds'])


@pytest.mark.parametrize('test_title', [
    'a',
    'a' * 100,
    "this is a test title",
    "this is a test title with numbers 123",
])
def test_song_title_of_correct_length_creates_object(db, test_title):
    song = mixer.blend(Song, title=test_title)
    song.full_clean(exclude=['author', 'genre', 'duration_in_seconds'])


@pytest.mark.parametrize('test_genre', [
    'ROCK',
    'RAP',
    'TRAP',
    'COUNTRY',
    'PUNK',
    'HOUSE',
    'DANCE',
])
def test_song_genre_of_correct_length_creates_object(db, test_genre):
    song = mixer.blend(Song, genre=test_genre)
    song.full_clean(exclude=['author', 'title', 'duration_in_seconds'])


@pytest.mark.parametrize('test_genre', [
    "POP",
    "FOLK",
    "BLUES",
    "JAZZ",
    "CLASSICAL",
])
def test_song_genre_not_in_choices_raises_exception(db, test_genre):
    song = mixer.blend(Song, genre=test_genre)
    with pytest.raises(ValidationError):
        song.full_clean(exclude=['author', 'title', 'duration_in_seconds'])


def test_song_duration_in_seconds_of_value_0_creates_object(db):
    song = mixer.blend(Song, duration_in_seconds=0)
    song.full_clean(exclude=['author', 'title', 'genre'])


def test_song_duration_in_seconds_of_value_3600_creates_object(db):
    song = mixer.blend(Song, duration_in_seconds=3600)
    song.full_clean(exclude=['author', 'title', 'genre'])


def test_song_str(db):
    song = mixer.blend(Song, author="Stone Temple Pilots", title="Plush", genre="ROCK", duration_in_seconds=317)
    assert str(song) == "Stone Temple Pilots - Plush [ROCK] (5:17)"
