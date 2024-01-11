import copy
import dataclasses
import re
from typing import List, Optional, Any

import typeguard as typeguard
from valid8 import validate
from valid8.validation_lib import lt, gt

from validation.regex import pattern


def sanitize_topping(value: str) -> str:
    return re.sub(r' +', ' ', re.sub(r'(.)\(\s*meet\s*\)', r'\1 (meet)', value.strip()))


@typeguard.typechecked
@dataclasses.dataclass(frozen=True, order=True)
class Base:
    value: str
    create_key: dataclasses.InitVar[Any] = dataclasses.field(default=None)

    __create_key = object()

    def __post_init__(self, create_key: Any):
        validate('create_key', create_key, equals=self.__create_key)

    @staticmethod
    def create(value: str) -> 'Base':
        if value not in ['deep pan', 'crispy']:
            raise ValueError()
        return Base(value, Base.__create_key)


@typeguard.typechecked
@dataclasses.dataclass(frozen=True, order=True)
class Topping:
    value: str
    __parse_pattern = r'^[A-Za-z ]+( \(meet\))?$'

    def __post_init__(self):
        validate('value', self.value, custom=pattern(self.__parse_pattern))


@typeguard.typechecked
@dataclasses.dataclass(frozen=True)
class Pizza:
    __base: Base
    __toppings: List[Topping] = dataclasses.field(default_factory=list, repr=False, init=False)

    create_key: dataclasses.InitVar[Any] = dataclasses.field(default=None)

    def __post_init__(self, create_key: Any):
        validate('create_key', create_key, custom=Pizza.Builder.is_valid_key)

    def _add_topping(self, value: Topping, create_key: Any) -> None:
        validate('create_key', create_key, custom=Pizza.Builder.is_valid_key)
        if self.base == "deep pan":
            validate('toppings_len', len(self.__toppings)+1, custom=lt(6, False))
        else:
            validate('toppings_len', len(self.__toppings)+1, custom=lt(5, False))
        self.__toppings.append(value)

    @property
    def toppings(self) -> List[str]:
        to_return = []
        for topping in self.__toppings:
            to_return.append(topping.value)
        return to_return

    @property
    def base(self) -> str:
        return self.__base.value

    @property
    def vegetarian(self) -> bool:
        return all("(meet)" not in topping for topping in self.toppings)

    @property
    def number_of_toppings(self) -> int:
        return len(self.__toppings)

    class Builder:
        __instance: Optional['Pizza'] = dataclasses.field(default=None)
        __built: bool = False
        __create_key = object()

        def __init__(self, base: str):
            self.__instance = Pizza(Base.create(base), Pizza.Builder.__create_key)

        @staticmethod
        def is_valid_key(key: Any) -> bool:
            return key == Pizza.Builder.__create_key

        def with_topping(self, topping: str) -> 'Pizza.Builder':
            to_add = sanitize_topping(topping)
            if to_add.endswith("(meet)"):
                validate('topping', to_add, min_len=4+len(" (meet)"), max_len=50+len(" (meet)"))
            else:
                validate('topping', to_add, min_len=4, max_len=50)
            self.__instance._add_topping(value=Topping(to_add), create_key=self.__create_key)
            return self

        def build(self) -> 'Pizza':
            validate('has_toppings', self.__instance.number_of_toppings, custom=gt(0, True))
            validate('built', self.__built, equals=False)
            self.__built = True
            return self.__instance

