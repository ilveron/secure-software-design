import re

from dataclasses import dataclass, field, InitVar
from typing import List, Union, Any

from typeguard import typechecked
from valid8 import validate

from validation.regex import pattern


@typechecked
@dataclass(frozen=True, order=True)
class Plate:
    value: str

    def __post_init__(self):
        validate('value', self.value, min_len=5, max_len=10, custom=pattern(r'[0-9A-Z]*'))

    def __str__(self):
        return self.value


@typechecked
@dataclass(frozen=True, order=True)
class Producer:
    value: str

    def __post_init__(self):
        validate('value', self.value, min_len=2, max_len=100, custom=pattern(r'[0-9A-Za-z -]*'))

    def __str__(self):
        return self.value


@typechecked
@dataclass(frozen=True, order=True)
class Model:
    value: str

    def __post_init__(self):
        validate('value', self.value, min_len=1, max_len=100, custom=pattern(r'[0-9A-Za-z -]*'))

    def __str__(self):
        return self.value


@typechecked
@dataclass(frozen=True, order=True)
class Discount:
    value_in_thousands: int

    def __post_init__(self):
        validate('value_in_thousands', self.value_in_thousands, min_value=0, max_value=1000)

    def __str__(self):
        return f'{self.value_in_thousands // 10}.{self.value_in_thousands % 10}%'

    def apply(self, value: int) -> int:
        return value * (1000 - self.value_in_thousands) // 1000


@typechecked
@dataclass(frozen=True, order=True)
class Price:
    value_in_cents: int
    create_key: InitVar[Any] = field(default='it must be the __create_key')

    __create_key = object()
    __max_value = 100000000000 - 1
    __parse_pattern = re.compile(r'(?P<euro>\d{0,11})(?:\.(?P<cents>\d{2}))?')

    def __post_init__(self, create_key):
        validate('create_key', create_key, equals=self.__create_key)
        validate('value_in_cents', self.value_in_cents, min_value=0, max_value=self.__max_value)

    def __str__(self):
        return f'{self.value_in_cents // 100}.{self.value_in_cents % 100:02}'

    @staticmethod
    def create(euro: int, cents: int=0) -> 'Price':
        validate('euro', euro, min_value=0, max_value=Price.__max_value // 100)
        validate('cents', cents, min_value=0, max_value=99)
        return Price(euro * 100 + cents, Price.__create_key)

    @staticmethod
    def parse(value: str) -> 'Price':
        m = Price.__parse_pattern.fullmatch(value)
        validate('value', m)
        euro = m.group('euro')
        cents = m.group('cents') if m.group('cents') else 0
        return Price.create(int(euro), int(cents))

    @property
    def cents(self) -> int:
        return self.value_in_cents % 100

    @property
    def euro(self) -> int:
        return self.value_in_cents // 100

    def add(self, other: 'Price') -> 'Price':
        return Price(self.value_in_cents + other.value_in_cents, self.__create_key)

    def apply_discount(self, discount: Discount) -> 'Price':
        return Price(discount.apply(self.value_in_cents), self.__create_key)



@typechecked
@dataclass(frozen=True, order=True)
class Car:
    plate: Plate
    producer: Producer
    model: Model
    price: Price

    @property
    def type(self) -> str:
        return 'Car'

    @property
    def final_price(self) -> Price:
        if self.price <= Price.create(10000):
            return self.price.apply_discount(Discount(50))
        if self.price <= Price.create(20000):
            return self.price.apply_discount(Discount(100))
        return self.price


@typechecked
@dataclass(frozen=True, order=True)
class Moto:
    plate: Plate
    producer: Producer
    model: Model
    price: Price

    @property
    def type(self) -> str:
        return 'Moto'

    @property
    def final_price(self) -> Price:
        if self.price <= Price.create(7000):
            return self.price.apply_discount(Discount(30))
        if self.price <= Price.create(15000):
            return self.price.apply_discount(Discount(75))
        return self.price


@typechecked
@dataclass(frozen=True)
class Dealer:
    __vehicles: List[Union[Car, Moto]] = field(default_factory=list, init=False)

    def vehicles(self) -> int:
        return len(self.__vehicles)

    def vehicle(self, index: int) -> Union[Car, Moto]:
        validate('index', index, min_value=0, max_value=self.vehicles() - 1)
        return self.__vehicles[index]

    def add_car(self, car: Car) -> None:
        self.__vehicles.append(car)

    def add_moto(self, moto: Moto) -> None:
        self.__vehicles.append(moto)

    def remove_vehicle(self, index: int) -> None:
        validate('index', index, min_value=0, max_value=self.vehicles() - 1)
        del self.__vehicles[index]

    def sort_by_producer(self) -> None:
        self.__vehicles.sort(key=lambda x: x.producer)

    def sort_by_price(self) -> None:
        self.__vehicles.sort(key=lambda x: x.price)
