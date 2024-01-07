import re
from dataclasses import dataclass, field, InitVar
from typing import Any

from typeguard import typechecked
from valid8 import validate

from validation.dataclasses import validate_dataclass
from validation.regex import pattern


@typechecked
@dataclass(frozen=True, order=True)
class PatientName:
    value: str

    def __post_init__(self):
        validate_dataclass(self)
        validate('value', self.value, min_len=1, max_len=100, custom=pattern('[A-Za-z0-9 ]*'))

    def __str__(self):
        return self.value

@typechecked
@dataclass(frozen=True, order=True)
class VisitType:
    value: str

    def __post_init__(self):
        validate_dataclass(self)
        validate('value', self.value, min_len=1, max_len=100, custom=pattern('[A-Za-z0-9 ]*'))

    def __str__(self) -> str:
        return self.value


@typechecked
@dataclass(frozen=True, order=True)
class ScheduledTime:
    """
    La rappresentazione è del tipo HH:MM. Il calcolo sarà fatto in questo modo:
    RAPPR       VALUE_IN_MINUTES_FROM_MIDNIGHT
    00:30   ->  30
    01:00   ->  60
    23:59   ->  1439
    """
    value_in_minutes_from_midnight: int
    create_key: InitVar[Any] = field(default=None)

    __create_key = object()
    __max_value = 24*60 - 1  # 1439
    __parse_pattern = re.compile(r'(?P<hours>\d{2}):(?P<minutes>\d{2})')

    def __post_init__(self, create_key):
        validate('create_key', create_key, equals=self.__create_key)
        validate_dataclass(self)
        validate('value_in_minutes_from_midnight', self.value_in_minutes_from_midnight, min_value=0, max_value=self.__max_value)

    def __str__(self):
        hours = self.value_in_minutes_from_midnight // 60
        minutes = self.value_in_minutes_from_midnight % 60
        return f"{hours:02}:{minutes:02}"

    @staticmethod
    def create(hours: int, minutes: int) -> 'ScheduledTime':
        validate('hours', hours, min_value=0, max_value=23)
        validate('minutes', minutes, min_value=0, max_value=59)
        in_minutes = hours * 60 + minutes
        return ScheduledTime(in_minutes, ScheduledTime.__create_key)

    @staticmethod
    def parse(value: str) -> 'ScheduledTime':
        res = ScheduledTime.__parse_pattern.fullmatch(value)
        validate('value', res)
        hours = res.group("hours")
        minutes = res.group("minutes")
        return ScheduledTime.create(int(hours), int(minutes))

    @property
    def hours(self) -> int:
        return self.value_in_minutes_from_midnight // 60

    @property
    def minutes(self) -> int:
        return self.value_in_minutes_from_midnight % 60


@typechecked
@dataclass(frozen=True, order=True)
class Cost:
    value_in_cents: int
    create_key: InitVar[Any] = field(default=None)

    __create_key = object()
    __max_value = 1000000_00 - 1  # Non penso che una visita arrivi a costare più di 999999,99 euro
    __parse_pattern = re.compile(r'(?P<euro>\d{1,6})\.(?P<cents>\d{2})')

    def __post_init__(self, create_key: Any):
        validate('create_key', create_key, equals=self.__create_key)
        validate_dataclass(self)
        validate('value_in_cents', self.value_in_cents, min_value=0, max_value=self.__max_value)

    def __str__(self) -> str:
        euro = self.value_in_cents // 100
        cents = self.value_in_cents % 100
        return f"{euro}.{cents:02}"

    @staticmethod
    def create(euro: int, cents: int) -> 'Cost':
        validate('euro', euro, min_value=0, max_value=Cost.__max_value // 100)
        validate('cents', cents, min_value=0, max_value=99)
        in_cents = euro * 100 + cents
        return Cost(in_cents, Cost.__create_key)

    @staticmethod
    def parse(value: str) -> 'Cost':
        res = Cost.__parse_pattern.fullmatch(value)
        euro = res.group("euro")
        cents = res.group("cents") if res.group("cents") else 0
        return Cost.create(int(euro), int(cents))

    @property
    def euro(self) -> int:
        return self.value_in_cents // 100

    @property
    def cents(self) -> int:
        return self.value_in_cents % 100


@typechecked
@dataclass(frozen=True, order=True)
class Reservation:
    patient_name: PatientName
    visit_type: VisitType
    scheduled_time: ScheduledTime
    cost: Cost

    @property
    def type(self) -> str:
        return 'Reservation'

    def __str__(self):
        return f"{self.patient_name} - {self.visit_type} - {self.scheduled_time} - {self.cost}"
