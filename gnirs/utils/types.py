from astropy import units as u
import numpy as np

def attach_units_pixel(variable_int):
    """Convert an int into a float

    If the input is an `integer` it first is converted into a `float`. Then the units of `pix` ara attached to make
    it an :obj:`astropy.Quantity`.

    Args:
        variable_int (int): variable of type int to be converted into an :obj:'astropy.quantity'

    Returns
        :obj:`astropy.Quantity`:

    """
    if variable_int is None:
        return variable_int
    if type(variable_int) is int:
        variable_int = float(variable_int)
    if type(variable_int) is not u.quantity.Quantity:
        variable_int = variable_int * u.pixel
    if variable_int.unit is not u.pixel:
        raise ValueError('The units should be pixel')
    return variable_int

def int_to_float(variable_int):
    """Convert an int into a float

    If the input is an `integer` it first is converted into a `float`. Then the units of `pix` ara attached to make
    it an :obj:`astropy.Quantity`.

    Args:
        variable_int (int): variable of type int to be converted into an :obj:'astropy.quantity'

    Returns
        float

    """
    if variable_int is None:
        return variable_int
    elif (type(variable_int) is int) | (type(variable_int) is np.int_):
        return float(variable_int)
    elif (type(variable_int) is float) | (type(variable_int) is np.float_):
        return variable_int
    elif type(variable_int) is np.ndarray:
        if len(variable_int) == 1:
            variable_int_first_element = variable_int[0]
            if (type(variable_int_first_element) is int) | (type(variable_int_first_element) is np.int_):
                return float(variable_int_first_element)
            elif (type(variable_int_first_element) is float) | (type(variable_int_first_element) is np.float_):
                return variable_int_first_element
            else:
                raise TypeError('Variable should be a int or a float')
        else:
            raise TypeError('Variable should be of size 1')
    else:
        raise TypeError('Variable should be a int or a float')
