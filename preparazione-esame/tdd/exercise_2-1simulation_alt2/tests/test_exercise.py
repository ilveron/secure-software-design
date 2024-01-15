import pytest
from exercise_2_1simulation_alt2.exercise import CoffeeOrder


def test_coffee_order_init_is_reserved():
    with pytest.raises(TypeError):
        CoffeeOrder("espresso", ["milk"], True)


def test_coffee_base_can_be_espresso_or_latte():
    for base in ("espresso", "latte"):
        assert CoffeeOrder.Builder(base).with_ingredient("milk").build().base == base


def test_coffee_base_cannot_be_cappuccino_or_american():
    for base in ("cappuccino", "american"):
        with pytest.raises(ValueError):
            CoffeeOrder.Builder(base).with_ingredient("milk").build()


def test_coffee_ingredient_must_be_between_3_and_40_letters_and_spaces_starting_with_letter_and_possibly_terminated_by_organic():
    valid_ingredients = ("sugar", "Sugar", "a" * 40, "abc def")
    invalid_ingredients = ("ab", "Abc0", "a" * 41)
    for ingredient in valid_ingredients:
        assert CoffeeOrder.Builder("espresso").with_ingredient(ingredient).build().ingredients[0] == ingredient
        assert CoffeeOrder.Builder("espresso").with_ingredient(f"{ingredient} (organic)").build().ingredients[
                   0] == f"{ingredient} (organic)"
    for ingredient in invalid_ingredients:
        with pytest.raises(ValueError):
            CoffeeOrder.Builder("espresso").with_ingredient(ingredient).build()
        with pytest.raises(ValueError):
            CoffeeOrder.Builder("espresso").with_ingredient(f"{ingredient} (organic)").build()


def test_coffee_ingredient_extra_spaces_are_sanitized():
    for ingredient in ("abc  def", "abc def ", " abc def"):
        assert CoffeeOrder.Builder("espresso").with_ingredient(ingredient).build().ingredients[0] == "abc def"
        for organic in ("organic ", " organic", " organic ", "    organic   "):
            assert CoffeeOrder.Builder("espresso").with_ingredient(f"{ingredient} ({organic})").build().ingredients[
                       0] == "abc def (organic)"
            assert CoffeeOrder.Builder("espresso").with_ingredient(f"{ingredient}   ({organic})").build().ingredients[
                       0] == "abc def (organic)"
    assert CoffeeOrder.Builder("espresso").with_ingredient("a  b   c     d     e").build().ingredients[0] == "a b c d e"


def test_extra_spaces_in_coffee_ingredient_are_stripped():
    for ingredient in (" abcdef", "abcdef ", " abcdef "):
        assert CoffeeOrder.Builder("espresso").with_ingredient(ingredient).build().ingredients[0] == ingredient.strip()
    for ingredient in (
    "abcdef  (organic)", "abcdef(organic)", "abcdef ( organic)", "abcdef (organic )", "abcdef ( organic )"):
        assert CoffeeOrder.Builder("espresso").with_ingredient(ingredient).build().ingredients[0] == "abcdef (organic)"


def test_coffee_builder_does_not_leak_instance():
    with pytest.raises(AttributeError):
        _ = CoffeeOrder.Builder("espresso").instance


def test_espresso_coffee_can_have_3_ingredients():
    builder = CoffeeOrder.Builder("espresso")
    for index in range(3):
        builder.with_ingredient("ingredient " + chr((ord('a') + index)))
    assert builder.build().number_of_ingredients == 3


def test_espresso_coffee_cannot_have_more_than_3_ingredients():
    with pytest.raises(ValueError):
        builder = CoffeeOrder.Builder("espresso")
        for index in range(4):
            builder.with_ingredient("ingredient " + chr((ord('a') + index)))
        builder.build()


def test_latte_coffee_can_have_4_ingredients():
    builder = CoffeeOrder.Builder("latte")
    for index in range(4):
        builder.with_ingredient("ingredient " + chr((ord('a') + index)))
    assert builder.build().number_of_ingredients == 4


def test_latte_coffee_cannot_have_more_than_4_ingredients():
    with pytest.raises(ValueError):
        builder = CoffeeOrder.Builder("latte")
        for index in range(5):
            builder.with_ingredient("ingredient " + chr((ord('a') + index)))
        builder.build()


@pytest.fixture
def organic_coffee_orders():
    return [
        CoffeeOrder.Builder("espresso").with_ingredient("milk (organic)").build(),
        CoffeeOrder.Builder("espresso").with_ingredient("milk").with_ingredient("sugar (organic)").build(),
        CoffeeOrder.Builder("latte").with_ingredient("milk (organic)").build(),
        CoffeeOrder.Builder("latte").with_ingredient("milk").with_ingredient("sugar (organic)").build()
    ]


@pytest.fixture
def non_organic_coffee_orders():
    return [
        CoffeeOrder.Builder("espresso").with_ingredient("milk").with_ingredient("barley").build(),
        CoffeeOrder.Builder("latte").with_ingredient("milk").with_ingredient("chocolate").build(),
    ]


def test_organic_coffee_orders(organic_coffee_orders):
    for order in organic_coffee_orders:
        assert order.organic


def test_non_organic_coffee_orders(non_organic_coffee_orders):
    for order in non_organic_coffee_orders:
        assert not order.organic


def test_coffee_base_is_read_only(organic_coffee_orders):
    assert organic_coffee_orders[0].base == "espresso"
    with pytest.raises(AttributeError):
        organic_coffee_orders[0].base = "latte"


def test_coffee_ingredients_is_read_only(organic_coffee_orders):
    number_of_ingredients = len(organic_coffee_orders[0].ingredients)
    organic_coffee_orders[0].ingredients.clear()
    assert len(organic_coffee_orders[0].ingredients) == number_of_ingredients


def test_coffee_order_must_have_ingredients():
    with pytest.raises(ValueError):
        CoffeeOrder.Builder("espresso").build()


def test_coffee_builder_cannot_be_reused():
    with pytest.raises(ValueError):
        builder = CoffeeOrder.Builder("latte").with_ingredient("milk")
        builder.build()
        builder.with_ingredient("sugar").build()
