

MASS_DICT = {
    'g': 1,
    'lb': 453.592,
    'oz': 28.3495
}

VOL_DICT = {
    'l': 1,
    'ml': 0.001,
    'tbsp': 0.0147868,
    'cup': 0.24,
    'fl. oz': 0.0295735
}

def get_measurements(unit: str, unit_type: int):
    if unit_type == 1:
        return MASS_DICT[unit]
    elif unit_type == 2:
        return VOL_DICT[unit]