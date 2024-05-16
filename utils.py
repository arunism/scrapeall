def deserialize_python(value):
    try:
        return eval(value)
    except Exception:
        return value