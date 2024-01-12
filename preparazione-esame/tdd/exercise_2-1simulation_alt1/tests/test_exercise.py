import pytest

from exercise_2_1simulation_alt1.exercise import Salad


def test_salad_init_is_reserved():
    with pytest.raises(TypeError):
        Salad("lettuce", ["tomato"], True)


def test_salad_base_can_be_lettuce_or_spinach():
    for base in ("lettuce", "spinach"):
        assert Salad.Builder(base).with_ingredient("tomato").build().base == base


def test_salad_base_cannot_be_cabbage_or_kale():
    for base in ("cabbage", "kale"):
        with pytest.raises(ValueError):
            Salad.Builder(base).with_ingredient("tomato").build()


def test_salad_ingredient_must_be_between_4_and_50_letters_and_spaces_starting_with_letter_and_possibly_terminated_by_gluten():
    valid_ingredients = ("carrot", "Carrot", "a" * 50, "abc def")
    invalid_ingredients = ("abc", "Abc0", "a" * 51)
    for ingredient in valid_ingredients:
        assert Salad.Builder("lettuce").with_ingredient(ingredient).build().ingredients[0] == ingredient
        assert Salad.Builder("lettuce").with_ingredient(f"{ingredient} (gluten)").build().ingredients[
                   0] == f"{ingredient} (gluten)"
    for ingredient in invalid_ingredients:
        with pytest.raises(ValueError):
            Salad.Builder("lettuce").with_ingredient(ingredient).build()
        with pytest.raises(ValueError):
            Salad.Builder("lettuce").with_ingredient(f"{ingredient} (gluten)").build()


def test_salad_ingredient_extra_spaces_are_sanified():
    for ingredient in ("abc  def", "abc def ", " abc def"):
        assert Salad.Builder("lettuce").with_ingredient(ingredient).build().ingredients[0] == "abc def"
        for gluten in ("gluten ", " gluten", " gluten ", "    gluten   "):
            assert Salad.Builder("lettuce").with_ingredient(f"{ingredient} ({gluten})").build().ingredients[
                       0] == "abc def (gluten)"
            assert Salad.Builder("lettuce").with_ingredient(f"{ingredient}   ({gluten})").build().ingredients[
                       0] == "abc def (gluten)"
    assert Salad.Builder("lettuce").with_ingredient("a  b   c     d     e").build().ingredients[0] == "a b c d e"


def test_extra_spaces_in_salad_ingredient_are_stripped():
    for ingredient in (" abcdef", "abcdef ", " abcdef "):
        assert Salad.Builder("lettuce").with_ingredient(ingredient).build().ingredients[0] == ingredient.strip()
    for ingredient in (
    "abcdef  (gluten)", "abcdef(gluten)", "abcdef ( gluten)", "abcdef (gluten )", "abcdef ( gluten )"):
        assert Salad.Builder("lettuce").with_ingredient(ingredient).build().ingredients[0] == "abcdef (gluten)"


def test_salad_builder_does_not_leak_instance():
    with pytest.raises(AttributeError):
        _ = Salad.Builder("lettuce").instance


def test_lettuce_salad_can_have_5_ingredients():
    builder = Salad.Builder("lettuce")
    for index in range(5):
        builder.with_ingredient("ingredient " + chr((ord('a') + index)))
    assert builder.build().number_of_ingredients == 5


def test_lettuce_salad_cannot_have_more_than_5_ingredients():
    with pytest.raises(ValueError):
        builder = Salad.Builder("lettuce")
        for index in range(6):
            builder.with_ingredient("ingredient " + chr((ord('a') + index)))
        builder.build()


def test_spinach_salad_can_have_4_ingredients():
    builder = Salad.Builder("spinach")
    for index in range(4):
        builder.with_ingredient("ingredient " + chr((ord('a') + index)))
    assert builder.build().number_of_ingredients == 4


def test_spinach_salad_cannot_have_more_than_4_ingredients():
    with pytest.raises(ValueError):
        builder = Salad.Builder("spinach")
        for index in range(5):
            builder.with_ingredient("ingredient " + chr((ord('a') + index)))
        builder.build()


@pytest.fixture
def gluten_free_salads():
    return [
        Salad.Builder("lettuce").with_ingredient("tomato").build(),
        Salad.Builder("lettuce").with_ingredient("tomato").with_ingredient("cucumber").build(),
        Salad.Builder("lettuce").with_ingredient("tomato").with_ingredient("carrot").build(),
        Salad.Builder("spinach").with_ingredient("tomato").build(),
        Salad.Builder("spinach").with_ingredient("tomato").with_ingredient("cucumber").build(),
        Salad.Builder("spinach").with_ingredient("tomato").with_ingredient("carrot").build(),
    ]


@pytest.fixture
def non_gluten_free_salads():
    return [
        Salad.Builder("lettuce").with_ingredient("tomato").with_ingredient("couscous (gluten)").build(),
        Salad.Builder("spinach").with_ingredient("tomato").with_ingredient("couscous (gluten)").build(),
    ]


def test_gluten_free_salads(gluten_free_salads):
    for salad in gluten_free_salads:
        assert salad.gluten_free


def test_non_gluten_free_salads(non_gluten_free_salads):
    for salad in non_gluten_free_salads:
        assert not salad.gluten_free


def test_salad_base_is_read_only(gluten_free_salads):
    assert gluten_free_salads[0].base == "lettuce"
    with pytest.raises(AttributeError):
        gluten_free_salads[0].base = "spinach"


def test_salad_ingredients_is_read_only(gluten_free_salads):
    number_of_ingredients = len(gluten_free_salads[0].ingredients)
    gluten_free_salads[0].ingredients.clear()
    assert len(gluten_free_salads[0].ingredients) == number_of_ingredients


def test_salad_must_have_ingredients():
    with pytest.raises(ValueError):
        Salad.Builder("lettuce").build()


def test_salad_builder_cannot_be_reused():
    with pytest.raises(ValueError):
        builder = Salad.Builder("spinach").with_ingredient("tomato")
        builder.build()
        builder.with_ingredient("cucumber").build()
