import pytest
from tools.function_tools.math_utils import compound_interest, convert_units


def test_compound_interest_known_value():
    result = compound_interest(100000, 0.05, 1, n=12)
    assert result["final_amount"] == 105116.19
    assert result["principal"] == 100000
    assert result["rate_percent"] == 5.0
    assert result["total_interest"] == 5116.19


def test_compound_interest_zero_rate():
    result = compound_interest(10000, 0.0, 5)
    assert result["final_amount"] == 10000.0
    assert result["total_interest"] == 0.0


def test_convert_length_km_to_m():
    result = convert_units(1.0, "km", "m")
    assert result["converted_value"] == 1000.0
    assert result["from_unit"] == "km"
    assert result["to_unit"] == "m"


def test_convert_weight_kg_to_lb():
    result = convert_units(1.0, "kg", "lb")
    assert abs(result["converted_value"] - 2.204624) < 0.0001


def test_convert_temperature_celsius_to_fahrenheit():
    result = convert_units(0.0, "celsius", "fahrenheit")
    assert result["converted_value"] == 32.0


def test_convert_temperature_celsius_to_kelvin():
    result = convert_units(0.0, "celsius", "kelvin")
    assert result["converted_value"] == 273.15


def test_convert_temperature_fahrenheit_to_celsius():
    result = convert_units(212.0, "fahrenheit", "celsius")
    assert abs(result["converted_value"] - 100.0) < 0.0001


def test_convert_units_incompatible_categories_raises():
    with pytest.raises(ValueError, match="Cannot convert"):
        convert_units(1.0, "km", "kg")


def test_convert_units_unknown_from_unit_raises():
    with pytest.raises(ValueError, match="Unknown unit"):
        convert_units(1.0, "parsec", "m")


def test_convert_units_unknown_to_unit_raises():
    with pytest.raises(ValueError, match="Unknown unit"):
        convert_units(1.0, "m", "furlongs")
