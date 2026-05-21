from fastmcp import FastMCP

_LENGTH = {"km": 1000.0, "m": 1.0, "cm": 0.01, "mi": 1609.344, "ft": 0.3048, "in": 0.0254}
_WEIGHT = {"kg": 1000.0, "g": 1.0, "lb": 453.59237, "oz": 28.349523}
_TEMP = {"celsius", "fahrenheit", "kelvin"}
_CATEGORIES = {"length": _LENGTH, "weight": _WEIGHT, "temperature": _TEMP}


def _unit_category(unit: str) -> str | None:
    for cat, units in _CATEGORIES.items():
        if unit in units:
            return cat
    return None


def _convert_temperature(value: float, from_unit: str, to_unit: str) -> float:
    if from_unit == "celsius":
        celsius = value
    elif from_unit == "fahrenheit":
        celsius = (value - 32) * 5 / 9
    else:
        celsius = value - 273.15

    if to_unit == "celsius":
        return celsius
    elif to_unit == "fahrenheit":
        return celsius * 9 / 5 + 32
    else:
        return celsius + 273.15


def compound_interest(principal: float, rate: float, years: int, n: int = 12) -> dict:
    """Calculate compound interest and return final amount breakdown.

    Args:
        principal: Initial principal amount
        rate: Annual interest rate as decimal (e.g. 0.05 = 5%)
        years: Number of years
        n: Compounding periods per year (default 12 = monthly)
    """
    if n <= 0:
        raise ValueError("n must be at least 1")
    amount = principal * (1 + rate / n) ** (n * years)
    return {
        "principal": principal,
        "final_amount": round(amount, 2),
        "total_interest": round(amount - principal, 2),
        "rate_percent": round(rate * 100, 4),
        "years": years,
        "n": n,
    }


def convert_units(value: float, from_unit: str, to_unit: str) -> dict:
    """Convert a value between units of length, weight, or temperature.

    Args:
        value: Numeric value to convert
        from_unit: Source unit — km, m, cm, mi, ft, in, kg, g, lb, oz, celsius, fahrenheit, kelvin
        to_unit: Target unit — same options as from_unit
    """
    from_unit = from_unit.lower()
    to_unit = to_unit.lower()

    from_cat = _unit_category(from_unit)
    to_cat = _unit_category(to_unit)

    if from_cat is None:
        raise ValueError(f"Unknown unit: {from_unit}")
    if to_cat is None:
        raise ValueError(f"Unknown unit: {to_unit}")
    if from_cat != to_cat:
        raise ValueError(f"Cannot convert {from_unit} ({from_cat}) to {to_unit} ({to_cat})")

    if from_cat == "temperature":
        converted = _convert_temperature(value, from_unit, to_unit)
    else:
        base = value * _CATEGORIES[from_cat][from_unit]
        converted = base / _CATEGORIES[to_cat][to_unit]

    return {
        "original_value": value,
        "from_unit": from_unit,
        "converted_value": round(converted, 6),
        "to_unit": to_unit,
    }


def register(mcp: FastMCP) -> None:
    mcp.tool()(compound_interest)
    mcp.tool()(convert_units)
