from dataclasses import field, dataclass
from typing import List

from typeguard import typechecked
from valid8 import validate

from medical_office.domain import Reservation


@typechecked
@dataclass(frozen=True)
class Office:
    __reservations: List[Reservation] = field(default_factory=list, init=False)

    def reservations(self) -> int:
        return len(self.__reservations)

    def reservation(self, index: int) -> Reservation:
        validate('index', index, min_value=0, max_value=self.reservations() - 1)
        return self.__reservations[index]

    def add_reservation(self, reservation: Reservation) -> None:
        self.__reservations.append(reservation)
        self.__reservations.sort(key=lambda res: res.scheduled_time)

    def remove_reservation(self, index: int) -> None:
        validate('index', index, min_value=0, max_value=self.reservations() - 1)
        del self.__reservations[index]