import pytest
from valid8 import ValidationError

from dealer.domain import Price, Plate, Producer, Model, Discount, Car, Moto, Dealer


def test_plate_format():
    wrong_values = ['', 'abcde', 'AA000bb', 'A'*11]
    for value in wrong_values:
        with pytest.raises(ValidationError):
            Plate(value)

    correct_values = ['CA220NE', 'ABCDE', 'A'*10]
    for value in correct_values:
        assert Plate(value).value == value


def test_plate_str():
    for value in ['CA220NE', 'ABCDE', 'A'*10]:
        assert str(Plate(value)) == value


def test_producer_format():
    wrong_values = ['', 'a', 'abcde.', 'AA000bb!', 'A'*101]
    for value in wrong_values:
        with pytest.raises(ValidationError):
            Producer(value)

    correct_values = ['Fiat', 'VW', 'A'*100]
    for value in correct_values:
        assert Producer(value).value == value


def test_producer_str():
    for value in ['Fiat', 'VW', 'A'*100]:
        assert str(Producer(value)) == value


def test_model_format():
    wrong_values = ['', '$', 'abcde.', 'AA000bb!', 'A'*101]
    for value in wrong_values:
        with pytest.raises(ValidationError):
            Model(value)

    correct_values = ['Punto', 'CC', 'A'*100]
    for value in correct_values:
        assert Model(value).value == value


def test_model_str():
    for value in ['Punto', 'CC', 'A'*100]:
        assert str(Model(value)) == value


def test_discount_cannot_be_negative():
    with pytest.raises(ValidationError):
        Discount(-1)


def test_discount_cannot_be_greater_than_1000():
    with pytest.raises(ValidationError):
        Discount(1001)


def test_discount_str():
    assert str(Discount(100)) == '10.0%'


def test_discount_apply_to_int():
    assert Discount(100).apply(90) == 81


def test_price_no_init():
    with pytest.raises(ValidationError):
        Price(1)


def test_price_cannot_be_negative():
    with pytest.raises(ValidationError):
        Price.create(-1, 0)


def test_price_no_cents():
    assert Price.create(1, 0) == Price.create(1)


def test_price_parse():
    assert Price.parse('10.20') == Price.create(10, 20)


def test_price_str():
    assert str(Price.create(9, 99)) == '9.99'


def test_price_euro():
    assert Price.create(11, 22).euro == 11


def test_price_cents():
    assert Price.create(11, 22).cents == 22


def test_price_add():
    assert Price.create(9, 99).add(Price.create(0, 1)) == Price.create(10)


def test_price_apply_discount():
    assert Price.create(100).apply_discount(Discount(100)) == Price.create(90)


@pytest.fixture
def cars():
    return [
        Car(Plate('AB123CD'), Producer('Car Producer'), Model('Model'), Price.create(100)),
        Car(Plate('AB123CE'), Producer('Car Producer'), Model('Model'), Price.create(11000)),
        Car(Plate('AB123CF'), Producer('Car Producer'), Model('Model'), Price.create(21000)),
    ]


def test_car_type_is_car(cars):
    assert cars[0].type == 'Car'


def test_car_final_price(cars):
    assert cars[0].final_price == cars[0].price.apply_discount(Discount(50))
    assert cars[1].final_price == cars[1].price.apply_discount(Discount(100))
    assert cars[2].final_price == cars[2].price


@pytest.fixture
def motos():
    return [
        Moto(Plate('AB123CD'), Producer('Moto Producer'), Model('Model'), Price.create(100)),
        Moto(Plate('AB123CE'), Producer('Moto Producer'), Model('Model'), Price.create(8000)),
        Moto(Plate('AB123CF'), Producer('Moto Producer'), Model('Model'), Price.create(16000)),
    ]


def test_moto_type_is_moto(motos):
    assert motos[0].type == 'Moto'


def test_moto_final_price(motos):
    assert motos[0].final_price == motos[0].price.apply_discount(Discount(30))
    assert motos[1].final_price == motos[1].price.apply_discount(Discount(75))
    assert motos[2].final_price == motos[2].price


def test_dealer_add_car(cars):
    dealer = Dealer()
    size = 0
    for car in cars:
        dealer.add_car(car)
        size += 1
        assert dealer.vehicles() == size
        assert dealer.vehicle(size - 1) == car


def test_dealer_add_motos(motos):
    dealer = Dealer()
    size = 0
    for moto in motos:
        dealer.add_moto(moto)
        size += 1
        assert dealer.vehicles() == size
        assert dealer.vehicle(size - 1) == moto


def test_dealer_remove_vehicle(cars, motos):
    dealer = Dealer()
    for car in cars:
        dealer.add_car(car)
    for moto in motos:
        dealer.add_moto(moto)

    dealer.remove_vehicle(0)
    assert dealer.vehicle(0) == cars[1]

    with pytest.raises(ValidationError):
        dealer.remove_vehicle(-1)
    with pytest.raises(ValidationError):
        dealer.remove_vehicle(dealer.vehicles())

    while dealer.vehicles():
        dealer.remove_vehicle(0)
    assert dealer.vehicles() == 0


def test_dealer_sort_by_producer(cars, motos):
    dealer = Dealer()
    dealer.add_moto(motos[0])
    dealer.add_car(cars[0])
    dealer.sort_by_producer()
    assert dealer.vehicle(0) == cars[0]


def test_dealer_sort_by_price(cars):
    dealer = Dealer()
    dealer.add_car(cars[1])
    dealer.add_car(cars[0])
    dealer.sort_by_price()
    assert dealer.vehicle(0) == cars[0]

