def _validate_integer_params(**params):
    """Validate that the provided parameters are integers.

    Parameters
    ----------
    **params : int
        Named parameters whose values must be integers.

    Raises
    ------
    TypeError
        If any provided parameter is not an integer.
    """
    for name, value in params.items():
        if type(value) is not int:
            display_name = name.replace("_", " ").capitalize()
            raise TypeError(f"{display_name} must be an integer.")
