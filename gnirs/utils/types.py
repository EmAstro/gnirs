from astropy import units as u


def _attach_units_pixel(variable_int):
    """Convert an int into a float

    Args:

    """
    if type(variable_int) is int:
        variable_int = float(variable_int)
    if type(variable_int) is u.quantity.Quantity:
        return variable_int
