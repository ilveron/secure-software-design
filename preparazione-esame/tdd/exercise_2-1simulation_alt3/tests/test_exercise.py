import pytest

from exercise_2_1simulation_alt3.exercise import CarConfiguration


@pytest.fixture(scope="module")
def features_fixture():
    return ["chassis", "tint windows", "alloy wheels", "led headlights", "air conditioning", "android infotainment"]


def test_car_configuration_init_is_reserved():
    with pytest.raises(TypeError):
        CarConfiguration("ModelX", "electric", [], False)


def test_car_model_name_length():
    with pytest.raises(ValueError):
        CarConfiguration.Builder("AAAs", "diesel").build()
    with pytest.raises(ValueError):
        CarConfiguration.Builder("A" * 51, "electric").build()


def test_car_model_regex():
    with pytest.raises(ValueError):
        CarConfiguration.Builder("@@@@not ok", "diesel")
    with pytest.raises(ValueError):
        CarConfiguration.Builder("!not ok", "diesel")

    car = CarConfiguration.Builder("1this is ok", "diesel").with_feature("one").with_feature("two").with_feature("chassis").build()
    assert car.model_name == "1this is ok"


def test_car_model_extra_spaces_are_sanified():
    car = CarConfiguration.Builder("        why  these          spaces  ", "diesel").with_feature("one").with_feature("two").with_feature("chassis").build()
    assert car.model_name == "why these spaces"


def test_car_engine_type():
    for engine_type in ("electric", "hybrid", "gasoline", "diesel"):
        assert (CarConfiguration.Builder("ModelX", engine_type)
                .with_feature("one")
                .with_feature("two")
                .with_feature("chassis")
                .build()
                .engine_type == engine_type)


def test_car_features(features_fixture):
    builder = CarConfiguration.Builder("Focus", "gasoline")
    for f in features_fixture:
        builder.with_feature(f)
    built_car = builder.build()
    for f in features_fixture:
        assert f in built_car.features


def test_car_has_no_sunroof_property(features_fixture):
    builder = CarConfiguration.Builder("ModelX", "electric")
    builder.with_feature(features_fixture[0]).with_feature(features_fixture[1]).with_feature(features_fixture[2])
    assert not builder.build().has_sunroof


def test_car_has_sunroof_property(features_fixture):
    builder = CarConfiguration.Builder("ModelX", "electric")
    builder.with_feature(features_fixture[0]).with_feature(features_fixture[1]).with_feature("sunroof")
    assert builder.build().has_sunroof  # Feature added


def test_car_with_no_chassis_cant_be_built(features_fixture):
    builder = CarConfiguration.Builder("California", "gasoline")
    for f in features_fixture[1:]:
        builder.with_feature(f)
    with pytest.raises(ValueError):
        builder.build()
    builder.with_feature("chassis")
    assert builder.build().engine_type == "gasoline"  # it eventually gets built


def test_car_feature_length():
    builder = CarConfiguration.Builder("911 RS", "gasoline")
    builder.with_feature("one").with_feature("two").with_feature("three")
    with pytest.raises(ValueError):
        builder.with_feature("A" * 51)
    with pytest.raises(ValueError):
        builder.with_feature("A")


def test_car_feature_regex():
    builder = CarConfiguration.Builder("Uno Turbo", "gasoline")
    builder.with_feature("it is okay").with_feature("lets go")
    with pytest.raises(ValueError):
        builder.with_feature("this is not okay because of this !")


def test_car_feature_extra_spaces_are_sanified():
    builder = CarConfiguration.Builder("Turbo Daily", "diesel")
    builder.with_feature("carbon dioxide").with_feature("black fog").with_feature("chassis")
    car = builder.with_feature("     what   am i  doing   ").build()
    assert "what am i doing" in car.features


def test_car_builder_does_not_leak_instance():
    with pytest.raises(AttributeError):
        _ = CarConfiguration.Builder("ModelX", "electric").instance


def test_car_configuration_is_read_only(features_fixture):
    builder = CarConfiguration.Builder("Focus", "gasoline")
    for f in features_fixture:
        builder.with_feature(f)
    built_car = builder.build()
    number_of_features = len(built_car.features)
    built_car.features.clear()
    assert len(built_car.features) == number_of_features


