def string_to_boolean(bool_string):
    """
    Returns True or False depending on the lowercased string.

    True strings:
        true, t, 1, yes, y
    False strings:
        false, f, 0, no, n

    Returns None if not an expected string.
    """
    true_strings = ['true', 't', '1', 'yes', 'y']
    false_strings = ['false', 'f', '0', 'no', 'n']
    if str(bool_string).lower() in true_strings:
        return True
    elif str(bool_string).lower() in false_strings:
        return False
    else:
        raise ValueError('%s not a recognized boolean string' % bool_string)
