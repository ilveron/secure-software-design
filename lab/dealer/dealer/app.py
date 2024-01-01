import csv
import sys
from pathlib import Path
from typing import Any, Tuple, Callable

from valid8 import validate, ValidationError

from dealer.domain import Dealer, Car, Moto, Plate, Producer, Model, Price
from dealer.menu import Menu, Entry, Description



class App:
    __filename = Path(__file__).parent.parent / 'default.csv'
    __delimiter = '\t'

    def __init__(self):
        self.__menu = Menu.Builder(Description('LaRusso Auto Group'), auto_select=lambda: self.__print_vehicles())\
            .with_entry(Entry.create('1', 'Add car', on_selected=lambda: self.__add_car()))\
            .with_entry(Entry.create('2', 'Add moto', on_selected=lambda: self.__add_moto()))\
            .with_entry(Entry.create('3', 'Remove vehicle', on_selected=lambda: self.__remove_vehicle()))\
            .with_entry(Entry.create('4', 'Sort by producer', on_selected=lambda: self.__sort_by_producer()))\
            .with_entry(Entry.create('5', 'Sort by price', on_selected=lambda: self.__sort_by_price()))\
            .with_entry(Entry.create('0', 'Exit', on_selected=lambda: print('Bye!'), is_exit=True))\
            .build()
        self.__dealer = Dealer()

    def __print_vehicles(self) -> None:
        print_sep = lambda: print('-' * 100)
        print_sep()
        fmt = '%3s %-10s %-30s %-30s %10s %10s'
        print(fmt % ('#', 'PLATE', 'PRODUCER', 'MODEL', 'PRICE', 'FINAL PR.'))
        print_sep()
        for index in range(self.__dealer.vehicles()):
            vehicle = self.__dealer.vehicle(index)
            print(fmt % (index + 1, vehicle.plate.value, vehicle.producer.value, vehicle.model.value, vehicle.price, vehicle.final_price))
        print_sep()

    def __add_car(self) -> None:
        car = Car(*self.__read_vehicle())
        self.__dealer.add_car(car)
        self.__save()
        print('Car added!')

    def __add_moto(self) -> None:
        moto = Moto(*self.__read_vehicle())
        self.__dealer.add_moto(moto)
        self.__save()
        print('Moto added!')

    def __remove_vehicle(self) -> None:
        def builder(value: str) -> int:
            validate('value', int(value), min_value=0, max_value=self.__dealer.vehicles())
            return int(value)

        index = self.__read('Index (0 to cancel)', builder)
        if index == 0:
            print('Cancelled!')
            return
        self.__dealer.remove_vehicle(index - 1)
        self.__save()
        print('Vehicle removed!')

    def __sort_by_producer(self) -> None:
        self.__dealer.sort_by_producer()
        self.__save()

    def __sort_by_price(self) -> None:
        self.__dealer.sort_by_price()
        self.__save()

    def __run(self) -> None:
        try:
            self.__load()
        except ValueError as e:
            print(e)
            print('Continuing with an empty list of vehicles...')

        self.__menu.run()

    def run(self) -> None:
        try:
            self.__run()
        except:
            print('Panic error!', file=sys.stderr)

    def __load(self) -> None:
        if not Path(self.__filename).exists():
            return

        with open(self.__filename) as file:
            reader = csv.reader(file, delimiter=self.__delimiter)
            for row in reader:
                validate('row length', row, length=5)
                typ = row[0]
                plate = Plate(row[1])
                producer = Producer(row[2])
                model = Model(row[3])
                price = Price.parse(row[4])
                if typ == 'Car':
                    self.__dealer.add_car(Car(plate, producer, model, price))
                elif typ == 'Moto':
                    self.__dealer.add_moto(Moto(plate, producer, model, price))
                else:
                    raise ValueError('Unknown vehicle type in default.csv')

    def __save(self) -> None:
        with open(self.__filename, 'w') as file:
            writer = csv.writer(file, delimiter=self.__delimiter, lineterminator='\n')
            for index in range(self.__dealer.vehicles()):
                vehicle = self.__dealer.vehicle(index)
                writer.writerow([vehicle.type, vehicle.plate, vehicle.producer, vehicle.model, vehicle.price])

    @staticmethod
    def __read(prompt: str, builder: Callable) -> Any:
        while True:
            try:
                line = input(f'{prompt}: ')
                res = builder(line.strip())
                return res
            except (TypeError, ValueError, ValidationError) as e:
                print(e)

    def __read_vehicle(self) -> Tuple[Plate, Producer, Model, Price]:
        plate = self.__read('Plate', Plate)
        producer = self.__read('Producer', Producer)
        model = self.__read('Model', Model)
        price = self.__read('Price', Price.parse)
        return plate, producer, model, price


def main(name: str):
    if name == '__main__':
        App().run()

main(__name__)
