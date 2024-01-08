import pytest

from music_archive.domain import Author, Title, Genre, Duration, Song


@pytest.fixture(scope="module")
def authors_fixture():
    return [
        Author("Marco il duca"),
        Author("Ciccio il gallo"),
        Author("Francesca la filice"),
        Author("Emanuele il conforti"),
        Author("Supermalvi"),
        Author("TDD 101")
    ]


@pytest.fixture(scope="module")
def titles_fixture():
    return [
        Title("My first awesome song"),
        Title("My second more awesome song"),
        Title("Do you want to see the DDD")
    ]


@pytest.fixture(scope="module")
def genres_fixture():
    return [
        Genre("Rock"),
        Genre("Pop"),
        Genre("Jazz"),
        Genre("Rhythm and blues")
    ]


@pytest.fixture(scope="module")
def durations_fixture():
    return [
        Duration.create(3, 14),
        Duration.create(minutes=10, seconds=50),
        Duration.create(0, 52),
        Duration.create(0, 0)
    ]


@pytest.mark.parametrize("test_author", [
    "Correct Author",
    "Another Correct Author",
    "Various Artists 123",
    " ",
    "Hotpause",
    "A" * 100
])
def test_author_with_correct_values_creates_object(test_author):
    assert Author(test_author).value == test_author


@pytest.mark.parametrize("test_author", [
    "",
    "A" * 101,
    "incorrect value!"
])
def test_author_with_incorrect_values_raises_exception(test_author):
    with pytest.raises(ValueError):
        Author(test_author)


def test_author_str(authors_fixture):
    assert str(authors_fixture[0]) == authors_fixture[0].value


@pytest.mark.parametrize("test_title", [
    "Every little thing she does is magic",
    "Fortuna",
    "BYOB",
    "Z" * 100,
    " " * 100,
    " "
])
def test_title_with_correct_value_creates_object(test_title):
    assert Title(test_title).value == test_title


@pytest.mark.parametrize("test_title", [
    "",
    "A" * 101,
    "incorrect value!"
])
def test_title_with_incorrect_value_raises_exception(test_title):
    with pytest.raises(ValueError):
        Title(test_title)


def test_title_str(titles_fixture):
    assert str(titles_fixture[0]) == titles_fixture[0].value


@pytest.mark.parametrize("test_genre", [
    "Rock",
    "Pop",
    "Jazz",
    "Rhythm and blues",
    " "
])
def test_genre_with_correct_value_creates_object(test_genre):
    assert Genre(test_genre).value == test_genre


@pytest.mark.parametrize("test_genre", [
    "",
    "A" * 101,
    "incorrect value!"
])
def test_genre_with_incorrect_value_raises_exception(test_genre):
    with pytest.raises(ValueError):
        Genre(test_genre)


def test_genre_str(genres_fixture):
    assert str(genres_fixture[0]) == genres_fixture[0].value


@pytest.mark.parametrize("test_minutes,test_seconds", [
    (0, 0),
    (0, 59),
    (1, 0),
    (59, 59),
    (59, 0),
    (0, 1),
    (0, 0),
    (0, 0)
])
def test_duration_with_correct_values_creates_object(test_minutes, test_seconds):
    duration = Duration.create(test_minutes, test_seconds)
    assert duration.minutes == test_minutes
    assert duration.seconds == test_seconds


@pytest.mark.parametrize("test_minutes,test_seconds", [
    (-1, 0),
    (60, 0),
    (0, -1),
    (0, 60)
])
def test_duration_with_incorrect_values_raises_exception(test_minutes, test_seconds):
    with pytest.raises(ValueError):
        Duration.create(test_minutes, test_seconds)


def test_duration_parse_with_correct_value_returns_object():
    string_value = "3:14"
    d = Duration.parse(string_value)
    assert d.minutes == 3 and d.seconds == 14


def test_duration_parse_with_incorrect_minutes_raises_exception():
    string_value = "300:14"
    with pytest.raises(AttributeError):
        Duration.parse(string_value)


def test_duration_parse_with_too_few_seconds_digits_raises_exception():
    string_value = "3:0"
    with pytest.raises(AttributeError):
        Duration.parse(string_value)


def test_duration_parse_with_too_much_seconds_digits_raises_exception():
    string_value = "3:024"
    with pytest.raises(AttributeError):
        Duration.parse(string_value)


def test_duration_parse_with_generically_wrong_value_raises_exception():
    string_value = "1000"  # MILLE!
    with pytest.raises(AttributeError):
        Duration.parse(string_value)


def test_duration_str(durations_fixture):
    assert str(durations_fixture[0]) == "3:14"


def test_song_with_correct_values_creates_object(authors_fixture, titles_fixture, genres_fixture, durations_fixture):
    author = authors_fixture[0]
    title = titles_fixture[0]
    genre = genres_fixture[0]
    duration = durations_fixture[0]
    s = Song(author, title, genre, duration)
    assert (s.author.value == author.value and
            s.title.value == title.value and
            s.genre.value == genre.value and
            s.duration.value_in_seconds == duration.value_in_seconds)


def test_song_str(authors_fixture, titles_fixture, genres_fixture, durations_fixture):
    author = authors_fixture[0]
    title = titles_fixture[0]
    genre = genres_fixture[0]
    duration = durations_fixture[0]
    s = Song(author, title, genre, duration)
    assert str(s) == f"{author.value} - {title.value} [{genre.value}] ({duration})"


def test_song_type(authors_fixture, titles_fixture, genres_fixture, durations_fixture):
    author = authors_fixture[0]
    title = titles_fixture[0]
    genre = genres_fixture[0]
    duration = durations_fixture[0]
    s = Song(author, title, genre, duration)
    assert s.type == "Song"
