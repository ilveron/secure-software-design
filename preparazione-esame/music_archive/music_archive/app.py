import csv
import sys
from pathlib import Path
from typing import Any, Callable, Tuple

from valid8 import validate, ValidationError

from menu.menu import Menu, Description, Entry
from music_archive.archive import Archive
from music_archive.domain import Author, Title, Genre, Duration, Song
from utils.constants import MENU_DESCRIPTION, FMT_STR


def print_sep():
    print("-" * 95)


class App:
    __filename = Path(__file__).parent / 'music_archive.csv'
    __delimiter = '\t'

    def __init__(self):
        self.__menu = Menu.Builder(Description(MENU_DESCRIPTION), auto_select=lambda: self.__print_archive(None)) \
            .with_entry(Entry.create('1', 'Add song', on_selected=lambda: self.__add_song())) \
            .with_entry(Entry.create('2', 'Remove song', on_selected=lambda: self.__remove_song())) \
            .with_entry(Entry.create('3', 'Sort by author', on_selected=lambda: self.__sort_by_author())) \
            .with_entry(Entry.create('4', 'Sort by title', on_selected=lambda: self.__sort_by_title())) \
            .with_entry(Entry.create('5', 'Sort by genre', on_selected=lambda: self.__sort_by_genre())) \
            .with_entry(Entry.create('6', 'Sort by duration', on_selected=lambda: self.__sort_by_duration())) \
            .with_entry(Entry.create('7', 'Filter songs by author', on_selected=lambda: self.__filter_by_author())) \
            .with_entry(Entry.create('0', 'Exit', on_selected=lambda: print('See you soon!'), is_exit=True)) \
            .build()
        self.__archive = Archive()

    def __print_archive(self, author: Author | None) -> None:
        print_sep()
        print(FMT_STR % ('#', "Author", "Title", "Genre", "Duration"))
        print_sep()
        for index in range(self.__archive.songs()):
            song = self.__archive.song(index)
            if author is None or author == song.author:
                print(FMT_STR % (index + 1, str(song.author), str(song.title), str(song.genre), str(song.duration)))
        print_sep()
        if author is not None:
            input("Press enter to continue...")

    def __add_song(self) -> None:
        song = Song(*self.__read_song())
        self.__archive.add_song(song)
        self.__save()
        print('Song added!')

    def __remove_song(self) -> None:
        def builder(value: str) -> int:
            validate(value, int(value), min_value=0, max_value=self.__archive.songs())
            return int(value)

        index = self.__read("Index (0 to cancel)", builder)
        if index == 0:
            print("Cancelled!")
            return
        self.__archive.remove_song(index - 1)
        self.__save()
        print("Song removed!")

    def __sort_by_author(self) -> None:
        self.__archive.sort_by_author()
        self.__save()

    def __sort_by_title(self) -> None:
        self.__archive.sort_by_title()
        self.__save()

    def __sort_by_genre(self) -> None:
        self.__archive.sort_by_genre()
        self.__save()

    def __sort_by_duration(self) -> None:
        self.__archive.sort_by_duration()
        self.__save()

    def __filter_by_author(self) -> None:
        author = self.__read_author()
        self.__print_archive(author)

    @staticmethod
    def __read(prompt: str, builder: Callable) -> Any:
        while True:
            try:
                line = input(f'{prompt}: ')
                res = builder(line.strip())
                return res
            except (TypeError, ValueError, ValidationError) as e:
                print(e)

    def __read_song(self) -> Tuple[Author, Title, Genre, Duration]:
        author = self.__read('Author', Author)
        title = self.__read('Title', Title)
        genre = self.__read('Genre', Genre)
        duration = self.__read('Duration', Duration.parse)
        return author, title, genre, duration

    def __read_author(self) -> Author:
        author = self.__read('Author to filter', Author)
        return author

    def __load(self) -> None:
        if not Path(self.__filename).exists():
            return

        with open(self.__filename) as file:
            reader = csv.reader(file, delimiter=self.__delimiter)
            for row in reader:
                # Author - Title - Genre - Duration -> 4
                validate('row length', row, length=4)
                author = Author(row[0])
                title = Title(row[1])
                genre = Genre(row[2])
                duration = Duration.parse(row[3])
                self.__archive.add_song(Song(author, title, genre, duration))

    def __save(self) -> None:
        with open(self.__filename, 'w') as file:
            writer = csv.writer(file, delimiter=self.__delimiter, lineterminator='\n')
            for index in range(self.__archive.songs()):
                song = self.__archive.song(index)
                writer.writerow([song.author, song.title, song.genre, song.duration])

    def __run(self) -> None:
        try:
            self.__load()
        except ValueError as e:
            print(e)
            print('There are songs in the archive!')

        self.__menu.run()

    def run(self) -> None:
        try:
            self.__run()
        except Exception as e:
            print(e)
            print("Panic error!", file=sys.stderr)


def main(name: str):
    if name == '__main__':
        App().run()


main(__name__)