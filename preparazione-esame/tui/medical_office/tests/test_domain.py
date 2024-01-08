import pytest

from medical_office import domain
from medical_office.domain import *


@pytest.fixture(scope='module')
def patient_names_fixture():
    return [
        PatientName("Patient"),
        PatientName("Yet Another Patient"),
        PatientName("A"),
        PatientName("R2D2"),
        PatientName("k" * 100)
    ]


@pytest.mark.parametrize("test_name", [
    "Patient",
    "Yet Another Patient",
    "A",
    "R2D2",
    "k" * 100
])
def test_patient_name_with_correct_length_creates_object(test_name):
    assert PatientName(test_name).value == test_name


@pytest.mark.parametrize("test_name", [
    "",
    "z" * 101,
])
def test_patient_name_with_incorrect_length_raises_exception(test_name):
    with pytest.raises(ValueError):
        PatientName(test_name)


@pytest.mark.parametrize("test_name", [
    1,
    ["list"],
    {"dict": "ionary"},
    ("tuple",),
])
def test_patient_name_with_incorrect_type_raises_exception(test_name):
    with pytest.raises(TypeError):
        PatientName(test_name)


def test_patient_name_str(patient_names_fixture):
    assert str(patient_names_fixture[0]) == patient_names_fixture[0].value


def test_patient_name_eq(patient_names_fixture):
    assert patient_names_fixture[0] == patient_names_fixture[0]
    assert patient_names_fixture[0] != patient_names_fixture[1]


def test_patient_name_lt(patient_names_fixture):
    assert patient_names_fixture[0] < patient_names_fixture[1]

####################################################################

####################################################################
### I test per VisitType sono analoghi a quelli per PatientName. ###
####################################################################

####################################################################

# ScheduledTime tests


@pytest.fixture(scope='module')
def scheduled_times_fixture():
    return [
        ScheduledTime.create(0, 0),
        ScheduledTime.create(0, 59),
        ScheduledTime.create(1, 0),
        ScheduledTime.create(23, 59),
        ScheduledTime.create(23, 0),
        ScheduledTime.create(0, 1)
    ]

@pytest.mark.parametrize("test_hours,test_minutes", [
    (0, 0),
    (0, 59),
    (1, 0),
    (23, 59),
    (23, 0),
    (0, 1),
])
def test_scheduled_time_with_correct_values_creates_object(test_hours, test_minutes):
    assert ScheduledTime.create(test_hours, test_minutes).value_in_minutes_from_midnight == test_hours * 60 + test_minutes


@pytest.mark.parametrize("test_hours,test_minutes", [
    (-1, 0),
    (24, 0),
    (0, -1),
    (0, 60),
])
def test_scheduled_time_with_incorrect_values_raises_exception(test_hours, test_minutes):
    with pytest.raises(ValueError):
        ScheduledTime.create(test_hours, test_minutes)


@pytest.mark.parametrize("test_hours,test_minutes", [
    (1, 0),
    (23, 59),
    (23, 0),
    (0, 1),
])
def test_scheduled_time_str(test_hours, test_minutes):
    assert str(ScheduledTime.create(test_hours, test_minutes)) == f"{test_hours:02}:{test_minutes:02}"


def test_scheduled_time_parse():
    string_value = "23:59"
    st = ScheduledTime.parse(string_value)
    assert st.hours == 23 and st.minutes == 59

####################################################################

# Cost tests


@pytest.mark.parametrize("test_euro,test_cents", [
    (0, 0),
    (0, 99),
    (1, 0),
    (999999, 99),
])
def test_cost_with_correct_value_creates_object(test_euro, test_cents):
    assert Cost.create(test_euro, test_cents).value_in_cents == test_euro * 100 + test_cents


@pytest.mark.parametrize("test_euro,test_cents", [
    (-1, 0),
    (1000000, 0),
    (0, -1),
    (0, 100),
])
def test_cost_with_incorrect_value_raises_exception(test_euro, test_cents):
    with pytest.raises(ValueError):
        Cost.create(test_euro, test_cents)


def test_cost_str():
    assert str(Cost.create(1, 0)) == "1.00"
    assert str(Cost.create(1, 1)) == "1.01"
    assert str(Cost.create(1, 99)) == "1.99"
    assert str(Cost.create(999999, 99)) == "999999.99"


def test_cost_parse_with_correct_value_returns_object():
    string_value = "123456.78"
    c = Cost.parse(string_value)
    assert c.euro == 123456 and c.cents == 78


def test_cost_parse_with_incorrect_euro_raises_exception():
    string_value = "1234567.78"
    with pytest.raises(AttributeError):
        Cost.parse(string_value)

####################################################################

# Reservation tests


@pytest.fixture(scope='module')
def reservations_fixture():
    return [
        Reservation(PatientName("Patient"), VisitType("Cardiology"), ScheduledTime.create(0, 0), Cost.create(0, 0)),
        Reservation(PatientName("Yet Another Patient"), VisitType("Dermatology"), ScheduledTime.create(0, 59), Cost.create(0, 99)),
        Reservation(PatientName("A"), VisitType("Neurology"), ScheduledTime.create(1, 0), Cost.create(1, 0)),
        Reservation(PatientName("R2D2"), VisitType("Otolaryngology"), ScheduledTime.create(23, 59), Cost.create(999999, 99)),
        Reservation(PatientName("k" * 100), VisitType("Radiology"), ScheduledTime.create(23, 0), Cost.create(0, 1))
    ]


def test_reservation_str(reservations_fixture):
    assert str(reservations_fixture[0]) == "Patient - Cardiology - 00:00 - 0.00"
    assert str(reservations_fixture[1]) == "Yet Another Patient - Dermatology - 00:59 - 0.99"
    assert str(reservations_fixture[2]) == "A - Neurology - 01:00 - 1.00"
    assert str(reservations_fixture[3]) == "R2D2 - Otolaryngology - 23:59 - 999999.99"
    assert str(reservations_fixture[4]) == "k" * 100 + " - Radiology - 23:00 - 0.01"


def test_reservation_type(reservations_fixture):
    assert reservations_fixture[0].type == "Reservation"
    assert reservations_fixture[1].type == "Reservation"
    assert reservations_fixture[2].type == "Reservation"
    assert reservations_fixture[3].type == "Reservation"
    assert reservations_fixture[4].type == "Reservation"
