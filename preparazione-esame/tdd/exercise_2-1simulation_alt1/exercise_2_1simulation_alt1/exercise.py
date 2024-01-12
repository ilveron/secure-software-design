import re
from typing import List, Optional, Any, Callable

from dataclass_type_validator import dataclass_type_validator, TypeValidationError
from typeguard import typechecked
from dataclasses import dataclass, field, InitVar
from valid8 import validate
from valid8.validation_lib import lt, gt


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

    __create_key = object()
    __ACCEPTED_BASES = ["lettuce", "spinach"]

    def __post_init__(self, create_key: Any):
        validate('create_key', create_key, equals=self.__create_key)

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
    __parse_pattern = r'^[A-Za-z][A-Za-z ]*( \(gluten\))?$'

    def __post_init__(self, create_key: Any):
        validate('create_key', create_key, equals=self.__create_key)

    @staticmethod
    def create(value: str) -> 'Ingredient':
        sanitized_value = Ingredient.__sanitize_ingredient(value)
        if '(gluten)' in sanitized_value:
            validate('sanitized_value', sanitized_value, min_len=4+len(' (gluten)'), max_len=50+len(' (gluten)'))
        else:
            validate('sanitized_value', sanitized_value, min_len=4, max_len=50)
        validate('sanitized_value', sanitized_value, custom=pattern(Ingredient.__parse_pattern))
        return Ingredient(sanitized_value, Ingredient.__create_key)

    @staticmethod
    def __sanitize_ingredient(value: str) -> str:
        with_fixed_gluten_info = re.sub(r'(.)\(\s*gluten\s*\)', r'\1 (gluten)', value)
        without_extra_spaces = " ".join(re.split(r' +', with_fixed_gluten_info)).strip()
        return without_extra_spaces


@typechecked
@dataclass(frozen=True)
class Salad:
    __base: Base
    __ingredients: List[Ingredient] = field(default_factory=list, repr=False, init=False)

    create_key: InitVar[Any] = field(default=None)

    def _add_ingredient(self, ingredient: Ingredient, create_key: Any):
        validate('create_key', create_key, custom=Salad.Builder.is_valid_key)
        self.__ingredients.append(ingredient)

    @property
    def base(self) -> str:
        return self.__base.value

    @property
    def ingredients(self) -> List[str]:
        return [i.value for i in self.__ingredients]

    @property
    def gluten_free(self) -> bool:
        return all("(gluten)" not in i for i in self.ingredients)

    @property
    def number_of_ingredients(self):
        return len(self.ingredients)

    class Builder:
        __instance: Optional['Salad'] = field(default=None)
        __create_key = object()
        __built = False

        def __init__(self, base: str):
            self.__instance = Salad(Base.create(base), self.__create_key)

        @staticmethod
        def is_valid_key(key: Any) -> bool:
            return key == Salad.Builder.__create_key

        def with_ingredient(self, ingredient: str) -> 'Salad.Builder':
            self.__instance._add_ingredient(Ingredient.create(ingredient), Salad.Builder.__create_key)
            return self

        def build(self) -> 'Salad':
            validate('built', self.__built, equals=False)
            self.__built = True
            if self.__instance.base == "lettuce":
                validate('number_of_ingredients', self.__instance.number_of_ingredients, custom=[lt(5, False), gt(0, True)])
            else:  # spinach
                validate('number_of_ingredients', self.__instance.number_of_ingredients, custom=[lt(4, False), gt(0, True)])
            return self.__instance
