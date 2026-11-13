from attack.model.predict import predict as _predict
from defense.padding.apply_padding import apply_padding as _apply_padding


def predict(trace):
    """
    trace: list[int]  (sequence of +1/-1 values, Tor cell direction)
    returns: {"site": str, "confidence": float}
    """
    return _predict(trace)


def apply_padding(trace, strength):
    """
    trace: list[int]
    strength: "light" | "medium" | "heavy"
    returns: list[int]  (padded trace)
    """
    return _apply_padding(trace, strength)