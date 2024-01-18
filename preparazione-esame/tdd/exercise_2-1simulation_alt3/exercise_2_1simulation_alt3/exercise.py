import dataclasses
import re
from typing import List, Optional, Any, Callable

from dataclass_type_validator import dataclass_type_validator, TypeValidationError
from typeguard import typechecked
from dataclasses import dataclass, field, InitVar

from valid8 import validate


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
class ModelName:
    value: str
    create_key: InitVar[Any] = field(default=None)

    __create_key = object()
    __MIN_MODEL_NAME_LEN: int = 5
    __MAX_MODEL_NAME_LEN: int = 50
    __PARSE_PATTERN = r'^[A-Za-z0-9][A-Za-z0-9 ]*$'

    def __post_init__(self, create_key: Any):
        validate('create_key', create_key, equals=self.__create_key)
        validate_dataclass(self)

    @staticmethod
    def create(value: str) -> 'ModelName':
        validate('value', value, max_len=ModelName.__MAX_MODEL_NAME_LEN)  # let's avoid operations on huge strings
        without_extra_spaces = re.sub(r' +', r' ', value.strip())
        validate('without_extra_spaces', without_extra_spaces, min_len=ModelName.__MIN_MODEL_NAME_LEN, custom=pattern(ModelName.__PARSE_PATTERN))
        return ModelName(without_extra_spaces, ModelName.__create_key)


@typechecked
@dataclass(frozen=True, order=True)
class Feature:
    value: str
    create_key: InitVar[str] = field(default=None)

    __create_key = object()
    __PARSE_PATTERN = r'^[A-Za-z][A-Za-z ]*'
    __MIN_MODEL_NAME_LEN: int = 3
    __MAX_MODEL_NAME_LEN: int = 50

    def __post_init__(self, create_key: Any):
        validate('create_key', create_key, equals=self.__create_key)
        validate_dataclass(self)

    @staticmethod
    def create(value: str):
        validate('value', value, max_len=Feature.__MAX_MODEL_NAME_LEN)
        without_extra_spaces = re.sub(r' +', ' ', value.strip())
        validate('without_extra_spaces', without_extra_spaces, min_len=Feature.__MIN_MODEL_NAME_LEN, custom=pattern(Feature.__PARSE_PATTERN))
        return Feature(without_extra_spaces, Feature.__create_key)

    def __str__(self):
        return self.value


@typechecked
@dataclass(frozen=True, order=True)
class EngineType:
    value: str
    create_key: InitVar[Any] = field(default=None)

    __create_key = object()
    __ACCEPTED_TYPES = ["electric", "hybrid", "gasoline", "diesel"]

    def __post_init__(self, create_key: Any):
        validate('create_key', create_key, equals=self.__create_key)
        validate_dataclass(self)

    @staticmethod
    def create(value: str) -> 'EngineType':
        validate('value', value, is_in=EngineType.__ACCEPTED_TYPES)
        return EngineType(value, EngineType.__create_key)


@typechecked
@dataclass(frozen=True)
class CarConfiguration:
    __model_name: ModelName
    __engine_type: EngineType
    __features: List[Feature] = field(default_factory=list, repr=False, init=False)

    create_key: InitVar[Any] = field(default=None)

    def __post_init__(self, create_key: Any):
        validate('create_key', create_key, custom=CarConfiguration.Builder.is_valid_key)
        validate_dataclass(self)

    def _add_feature(self, feature: Feature, create_key: Any) -> None:
        validate('create_key', create_key, custom=CarConfiguration.Builder.is_valid_key)
        self.__features.append(feature)

    @property
    def model_name(self) -> str:
        return self.__model_name.value

    @property
    def engine_type(self) -> str:
        return self.__engine_type.value

    @property
    def features(self) -> List[str]:
        return [str(f) for f in self.__features]

    @property
    def has_sunroof(self) -> bool:
        return "sunroof" in self.features

    @property
    def number_of_features(self) -> int:
        return len(self.__features)

    @typechecked
    @dataclass
    class Builder:
        __instance: Optional['CarConfiguration'] = field(default=None)
        __built = False
        __create_key = object()

        def __init__(self, model_name: str, engine_type: str):
            self.__instance = CarConfiguration(ModelName.create(model_name), EngineType.create(engine_type), self.__create_key)

        @staticmethod
        def is_valid_key(key: Any) -> bool:
            return key == CarConfiguration.Builder.__create_key

        def with_feature(self, feature: str) -> 'CarConfiguration.Builder':
            validate('number_of_features', self.__instance.number_of_features, max_value=9)
            self.__instance._add_feature(Feature.create(feature), CarConfiguration.Builder.__create_key)
            return self

        def build(self) -> 'CarConfiguration':
            validate('built', self.__built, equals=False)
            validate('number_of_features', self.__instance.number_of_features, min_value=3)
            validate('chassis_in_features', "chassis", is_in=self.__instance.features)
            self.__built = True
            return self.__instance
