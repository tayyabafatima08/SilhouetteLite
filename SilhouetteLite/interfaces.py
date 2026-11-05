def predict(trace):
    """
    trace: list[int]  (sequence of +1/-1 values, Tor cell direction)
    returns: {"site": str, "confidence": float}
    STUB — Person 1 implements this in attack/model/predict.py
    """
    raise NotImplementedError

def apply_padding(trace, strength):
    """
    trace: list[int]
    strength: "light" | "medium" | "heavy"
    returns: list[int]  (padded trace)
    """
    raise NotImplementedError