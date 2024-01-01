import re
from dataclasses import dataclass, InitVar, field
from typing import Any

from typeguard import typechecked
from valid8 import validate

from validation.dataclasses import validate_dataclass
from validation.regex import pattern


@typechecked
@dataclass(frozen=True, order=True)
class Author:
    value: str

    def __post_init__(self):
        validate_dataclass(self)
        validate('value', self.value, max_len=100, custom=pattern(r'^[A-Za-z0-9 ]+$'))

    def __str__(self):
        return f"{self.value}"


@typechecked
@dataclass(frozen=True, order=True)
class Title:
    value: str

    def __post_init__(self):
        validate_dataclass(self)
        validate('value', self.value, max_len=100, custom=pattern(r'^[A-Za-z0-9 ]+$'))

    def __str__(self):
        return f"{self.value}"


@typechecked
@dataclass(frozen=True, order=True)
class Genre:
    value: str

    def __post_init__(self):
        validate_dataclass(self)
        validate('value', self.value, max_len=100, custom=pattern(r'^[A-Za-z0-9 ]+$'))

    def __str__(self):
        return f"{self.value}"


@typechecked
@dataclass(frozen=True, order=True)
class Duration:
    value_in_seconds: int
    create_key: InitVar[Any] = field(default=None)

    __create_key = object()
    __max_value = 3600 - 1
    __parse_pattern = re.compile(r'(?P<minutes>\d{1,2}):(?P<seconds>\d{2})')

    def __post_init__(self, create_key):
        validate('create_key', create_key, equals=self.__create_key)
        validate_dataclass(self)
        validate('value_in_seconds', self.value_in_seconds, min_value=0, max_value=self.__max_value)

    def __str__(self):
        minutes = self.value_in_seconds // 60
        seconds = self.value_in_seconds % 60
        return f"{minutes}:{seconds:02}"

    @staticmethod
    def create(minutes: int, seconds: int) -> 'Duration':
        validate('minutes', minutes, min_value=0, max_value=Duration.__max_value // 60)
        validate('seconds', seconds, min_value=0, max_value=59)
        in_seconds = minutes * 60 + seconds
        return Duration(in_seconds, Duration.__create_key)

    @staticmethod
    def parse(value: str) -> 'Duration':
        res = Duration.__parse_pattern.fullmatch(value)
        minutes = res.group("minutes")
        seconds = res.group("seconds")
        return Duration.create(int(minutes), int(seconds))

    @property
    def seconds(self) -> int:
        return self.value_in_seconds % 60

    @property
    def minutes(self) -> int:
        return self.value_in_seconds // 60


@typechecked
@dataclass(frozen=True, order=True)
class Song:
    author: Author
    title: Title
    genre: Genre
    duration: Duration

    @property
    def type(self) -> str:
        return 'Song'

    def __str__(self):
        return f"{self.author} - {self.title} [{self.genre}] ({self.duration})"
