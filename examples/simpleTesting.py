def strToType(s: str) -> type:
    """Deduces the data type of a string

    Args:
        s: string to be deducted

    Returns:
        Estimated string type
    """
    from ast import literal_eval
    try:
        return type(literal_eval(s))
    except Exception:
        return type(s)


print(strToType('4654564.655'))
