import dataclasses
import re
from typing import List, Optional, Any, Callable

from dataclass_type_validator import dataclass_type_validator, TypeValidationError
from typeguard import typechecked
from dataclasses import *
from valid8 import *


def validate_dataclass(data):
    try:
        dataclass_type_validator(data)
    except TypeValidationError as e:
        raise TypeError(e)


@typechecked
def pattern(regex: str) -> Callable[[str], bool]:
    r = re.compile(regex)

    def res(value):
        return bool(r.fullmatch(value))

    res.__name__ = f'pattern({regex})'
    return res


@typechecked
@dataclass(frozen=True, order=True)
class Base:
    value: str
    create_key: InitVar[Any] = field(default=None)

    __ACCEPTED_BASES = ["espresso", "latte"]
    __create_key = object()

    def __post_init__(self, create_key: Any):
        validate('create_key', create_key, equals=self.__create_key)
        validate_dataclass(self)

    @staticmethod
    def create(value: str) -> 'Base':
        validate('value', value, is_in=Base.__ACCEPTED_BASES)
        return Base(value, Base.__create_key)


@typechecked
@dataclass(frozen=True, order=True)
class Ingredient:
    value: str
    create_key: InitVar[Any] = field(default=None)

    __create_key = object()
    __parse_pattern = r'^[A-Za-z][A-Za-z ]*( \(organic\))?$'

    def __post_init__(self, create_key: Any):
        validate('create_key', create_key, equals=self.__create_key)
        validate_dataclass(self)

    @staticmethod
    def create(value: str) -> 'Ingredient':
        sanitized_value = Ingredient.__sanitize_ingredient(value)
        if '(organic)' in sanitized_value:
            validate('sanitized_value', sanitized_value, min_len=3 + len(' (organic)'), max_len=40 + len(' (organic)'))
        else:
            validate('sanitized_value', sanitized_value, min_len=3, max_len=40)
        validate('sanitized_value', sanitized_value, custom=pattern(Ingredient.__parse_pattern))
        return Ingredient(sanitized_value, Ingredient.__create_key)

    @staticmethod
    def __sanitize_ingredient(ingredient: str) -> str:
        with_fixed_organic_info = re.sub(r'(.)\(\s*organic\s*\)', r'\1 (organic)', ingredient)
        return " ".join(re.split(r' +', with_fixed_organic_info)).strip()


@typechecked
@dataclass(frozen=True)
class CoffeeOrder:
    __base: Base
    __ingredients: List[Ingredient] = field(default_factory=list, repr=False, init=False)

    create_key: InitVar[Any] = field(default=None)

    def __post_init__(self, create_key: Any):
        # is_valid_key
        validate_dataclass(self)

    def _add_ingredient(self, ingredient: Ingredient, create_key: Any):
        validate('create_key', create_key, custom=CoffeeOrder.Builder.is_valid_key)
        self.__ingredients.append(ingredient)

    @property
    def base(self) -> str:
        return self.__base.value

    @property
    def ingredients(self) -> List[str]:
        return [ingredient.value for ingredient in self.__ingredients]

    @property
    def organic(self) -> bool:
        return any("organic" in ingredient for ingredient in self.ingredients)

    @property
    def number_of_ingredients(self) -> int:
        return len(self.ingredients)

    class Builder:
        __instance: Optional['CoffeeOrder'] = dataclasses.field(default=None)
        __built = False
        __create_key = object()

        def __init__(self, base: str):
            self.__instance = CoffeeOrder(Base.create(base), self.__create_key)

        @staticmethod
        def is_valid_key(key: Any) -> bool:
            return key == CoffeeOrder.Builder.__create_key

        def with_ingredient(self, ingredient: str) -> 'CoffeeOrder.Builder':
            self.__instance._add_ingredient(Ingredient.create(ingredient), self.__create_key)
            return self

        def build(self) -> 'CoffeeOrder':
            validate('built', self.__built, equals=False)
            self.__built = True
            if self.__instance.base == "espresso":
                validate('number_of_ingredients', self.__instance.number_of_ingredients, min_value=1, max_value=3)
            else:  # it is a latte
                validate('number_of_ingredients', self.__instance.number_of_ingredients, min_value=1, max_value=4)
            return self.__instance
