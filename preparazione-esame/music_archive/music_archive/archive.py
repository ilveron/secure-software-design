from dataclasses import field, dataclass
from typing import List
import copy

from typeguard import typechecked
from valid8 import validate

from music_archive.domain import Song, Author


@typechecked
@dataclass(frozen=True)
class Archive:
    __songs: List[Song] = field(default_factory=list, init=False)  # init false esclude il campo dall'init

    def songs(self) -> int:
        return len(self.__songs)

    def song(self, index: int) -> Song:
        validate('index', index, min_value=0, max_value=self.songs()-1)
        # possiamo tranquillamente restituire l'oggetto della lista perché è immutabile
        return self.__songs[index]

    def add_song(self, song: Song) -> None:
        self.__songs.append(song)

    def remove_song(self, index: int) -> None:
        validate('index', index, min_value=0, max_value=self.songs() - 1)
        del self.__songs[index]

    def sort_by_author(self) -> None:
        self.__songs.sort(key=lambda song: song.author)

    def sort_by_title(self) -> None:
        self.__songs.sort(key=lambda song: song.title)

    def sort_by_genre(self) -> None:
        self.__songs.sort(key=lambda song: song.genre)

    def sort_by_duration(self) -> None:
        self.__songs.sort(key=lambda song: song.duration)

    '''Fatto da TUI'''
    # def filter_by_author(self, author: Author) -> List[Song]:
    #     # copy è ok perché gli oggetti contenuti al suo interno sono tutti immutabili
    #     return copy.copy(filter(lambda song: song.author == author, self.__songs))
