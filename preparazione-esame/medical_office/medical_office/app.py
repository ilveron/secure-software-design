import csv
import sys
from pathlib import Path
from typing import Callable, Any, Tuple

from valid8 import validate, ValidationError

from medical_office.domain import Reservation, ScheduledTime, PatientName, VisitType, Cost
from medical_office.office import Office
from menu.menu import Menu, Entry, Description


def print_sep():
    print("-" * 100)


class App:
    __filename = Path(__file__).parent / 'medical_office.csv'
    __delimiter = '\t'
    __fmt_str = '%3s %-30s %-25s %-14s %-12s'

    def __init__(self):
        self.__menu = Menu.Builder(Description("Medical Office"), auto_select=lambda: self.__print_office(None)) \
            .with_entry(Entry.create('1', 'Add reservation', on_selected=lambda: self.__add_reservation())) \
            .with_entry(Entry.create('2', 'Remove reservation', on_selected=lambda: self.__remove_reservation())) \
            .with_entry(Entry.create('3', 'Filter reservations by scheduled time',
                                     on_selected=lambda: self.__filter_by_scheduled_time())) \
            .with_entry(Entry.create('0', 'Exit', on_selected=lambda: print('See you soon!'), is_exit=True)) \
            .build()
        self.__office = Office()

    def __print_office(self, scheduled_time: ScheduledTime | None) -> None:
        print_sep()
        print(self.__fmt_str % ('#', "Patient Name", "Visit Type", "Scheduled Time", "Cost"))
        print_sep()
        for index in range(self.__office.reservations()):
            reservation = self.__office.reservation(index)
            if scheduled_time is None or reservation.scheduled_time > scheduled_time:
                print(self.__fmt_str % (index + 1, str(reservation.patient_name), str(reservation.visit_type),
                                        str(reservation.scheduled_time), str(reservation.cost)))
        print_sep()
        if scheduled_time is not None:
            input("Press enter to continue...")

    def __add_reservation(self) -> None:
        res = Reservation(*self.__read_reservation())
        self.__office.add_reservation(res)
        self.__save()
        print("Reservation added!")

    def __remove_reservation(self) -> None:
        def builder(value: str) -> int:
            validate(value, int(value), min_value=0, max_value=self.__office.reservations())
            return int(value)

        index = self.__read("Index (0 to cancel)", builder)
        if index == 0:
            print("Cancelled!")
            return
        self.__office.remove_reservation(index - 1)
        self.__save()
        print("Reservation removed!")

    def __filter_by_scheduled_time(self) -> None:
        scheduled_time = self.__read_scheduled_time()
        self.__print_office(scheduled_time)

    @staticmethod
    def __read(prompt: str, builder: Callable) -> Any:
        while True:
            try:
                line = input(f'{prompt}: ')
                res = builder(line.strip())
                return res
            except (TypeError, ValueError, ValidationError) as e:
                print(e)

    def __read_reservation(self) -> Tuple[PatientName, VisitType, ScheduledTime, Cost]:
        patient_name = self.__read("Patient name", PatientName)
        visit_type = self.__read("Visit type", VisitType)
        scheduled_time = self.__read("Scheduled time", ScheduledTime.parse)
        cost = self.__read("Cost", Cost.parse)
        return patient_name, visit_type, scheduled_time, cost

    def __read_scheduled_time(self) -> ScheduledTime:
        scheduled_time = self.__read("Starting scheduled time", ScheduledTime.parse)
        return scheduled_time

    def __save(self) -> None:
        with open(self.__filename, 'w') as file:
            writer = csv.writer(file, delimiter=self.__delimiter, lineterminator='\n')
            for index in range(self.__office.reservations()):
                res = self.__office.reservation(index)
                writer.writerow([res.patient_name, res.visit_type, res.scheduled_time, res.cost])

    def __load(self) -> None:
        if not Path(self.__filename).exists():
            return

        with open(self.__filename) as file:
            reader = csv.reader(file, delimiter=self.__delimiter)
            for row in reader:
                # Author - Title - Genre - Duration -> 4
                validate('row length', row, length=4)
                patient_name = PatientName(row[0])
                visit_type = VisitType(row[1])
                scheduled_time = ScheduledTime.parse(row[2])
                cost = Cost.parse(row[3])
                self.__office.add_reservation(Reservation(patient_name, visit_type, scheduled_time, cost))

    def __run(self) -> None:
        try:
            self.__load()
        except ValueError as e:
            print(e)
            print('There are reservations in the agenda!')

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
