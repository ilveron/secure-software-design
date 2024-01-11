import pytest as pytest

from exercise_2_1simulation.exercise import Pizza


def test_pizza_init_is_reserved():
    with pytest.raises(TypeError):
        Pizza("deep pan", ["olive oil"], True)


def test_pizza_base_can_be_deep_pan_or_crispy():
    for base in ("deep pan", "crispy"):
        assert Pizza.Builder(base).with_topping("olive oil").build().base == base


def test_pizza_base_cannot_be_fluffy_or_squishy():
    for base in ("fluffy", "squishy"):
        with pytest.raises(ValueError):
            Pizza.Builder(base).with_topping("olive oil").build()


def test_pizza_topping_must_be_between_4_and_50_letters_and_spaces_starting_with_letter_and_possibly_terminated_by_meet():
    valid_toppings = ("abcd", "Abcd", "a" * 50, "abc cde")
    invalid_toppings = ("abc", "Abc0", "a" * 51)
    for topping in valid_toppings:
        assert Pizza.Builder("crispy").with_topping(topping).build().toppings[0] == topping
        assert Pizza.Builder("crispy").with_topping(f"{topping} (meet)").build().toppings[0] == f"{topping} (meet)"
    for topping in invalid_toppings:
        with pytest.raises(ValueError):
            Pizza.Builder("crispy").with_topping(topping).build()
        with pytest.raises(ValueError):
            Pizza.Builder("crispy").with_topping(f"{topping} (meet)").build()


def test_pizza_topping_extra_spaces_are_sanified():
    for topping in ("abc  cde", "abc cde ", " abc cde"):
        assert Pizza.Builder("crispy").with_topping(topping).build().toppings[0] == "abc cde"
        for meet in ("meet ", " meet", " meet ", "    meet   "):
            assert Pizza.Builder("crispy").with_topping(f"{topping} ({meet})").build().toppings[0] == "abc cde (meet)"
            assert Pizza.Builder("crispy").with_topping(f"{topping}   ({meet})").build().toppings[0] == "abc cde (meet)"
    assert Pizza.Builder("crispy").with_topping("a  b   c     d     e").build().toppings[0] == "a b c d e"


def test_extra_spaces_in_pizza_topping_are_stripped():
    for topping in (" abcd", "abcd ", " abcd "):
        assert Pizza.Builder("crispy").with_topping(topping).build().toppings[0] == topping.strip()
    for topping in ("abcd  (meet)", "abcd(meet)", "abcd ( meet)", "abcd (meet )", "abcd ( meet )"):
        assert Pizza.Builder("crispy").with_topping(topping).build().toppings[0] == "abcd (meet)"


def test_pizza_builder_does_not_leak_instance():
    with pytest.raises(AttributeError):
        _ = Pizza.Builder("crispy").instance


def test_deep_pan_pizza_can_have_6_toppings():
    builder = Pizza.Builder("deep pan")
    for index in range(6):
        builder.with_topping("topping " + chr((ord('a') + index)))
    assert builder.build().number_of_toppings == 6


def test_deep_pan_pizza_cannot_have_more_than_6_toppings():
    with pytest.raises(ValueError):
        builder = Pizza.Builder("deep pan")
        for index in range(7):
            builder.with_topping("topping " + chr((ord('a') + index)))
        builder.build()


def test_crispy_pizza_can_have_5_toppings():
    builder = Pizza.Builder("crispy")
    for index in range(5):
        builder.with_topping("topping " + chr((ord('a') + index)))
    assert builder.build().number_of_toppings == 5


def test_crispy_pizza_cannot_have_more_than_5_toppings():
    with pytest.raises(ValueError):
        builder = Pizza.Builder("crispy")
        for index in range(6):
            builder.with_topping("topping " + chr((ord('a') + index)))
        builder.build()


@pytest.fixture
def vegetarian_pizzas():
    return [
        Pizza.Builder("deep pan").with_topping("olive oil").build(),
        Pizza.Builder("deep pan").with_topping("olive oil").with_topping("tomato sauce").build(),
        Pizza.Builder("deep pan").with_topping("olive oil").with_topping("oregano").build(),
        Pizza.Builder("crispy").with_topping("olive oil").build(),
        Pizza.Builder("crispy").with_topping("olive oil").with_topping("tomato sauce").build(),
        Pizza.Builder("crispy").with_topping("olive oil").with_topping("oregano").build(),
    ]


@pytest.fixture
def non_vegetarian_pizzas():
    return [
        Pizza.Builder("deep pan").with_topping("olive oil").with_topping("tomato sauce").with_topping("pepperoni (meet)").build(),
        Pizza.Builder("crispy").with_topping("olive oil").with_topping("tomato sauce").with_topping("pepperoni (meet)").build(),
    ]


def test_vegetarian_pizzas(vegetarian_pizzas):
    for pizza in vegetarian_pizzas:
        assert pizza.vegetarian


def test_non_vegetarian_pizzas(non_vegetarian_pizzas):
    for pizza in non_vegetarian_pizzas:
        assert not pizza.vegetarian


def test_pizza_base_is_read_only(vegetarian_pizzas):
    assert vegetarian_pizzas[0].base == "deep pan"
    with pytest.raises(AttributeError):
        vegetarian_pizzas[0].base = "crispy"


def test_pizza_toppings_is_read_only(vegetarian_pizzas):
    number_of_toppings = len(vegetarian_pizzas[0].toppings)
    vegetarian_pizzas[0].toppings.clear()
    assert len(vegetarian_pizzas[0].toppings) == number_of_toppings


def test_pizza_must_have_toppings():
    with pytest.raises(ValueError):
        Pizza.Builder("deep pan").build()


def test_pizza_builder_cannot_be_reused():
    with pytest.raises(ValueError):
        builder = Pizza.Builder("crispy").with_topping("olive oil")
        builder.build()
        builder.with_topping("tomato sauce").build()