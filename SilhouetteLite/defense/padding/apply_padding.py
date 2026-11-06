import random

PADDING_RATES = {
    "light": 0.10,
    "medium": 0.30,
    "heavy": 0.60,
}

def apply_padding(trace, strength):
    """
    trace: list[int] — sequence of +1/-1 values (Tor cell direction)
    strength: "light" | "medium" | "heavy"
    returns: list[int] — padded trace
    """
    if strength not in PADDING_RATES:
        raise ValueError(f"strength must be one of {list(PADDING_RATES)}")

    rate = PADDING_RATES[strength]
    padded = []
    for cell in trace:
        padded.append(cell)
        if random.random() < rate:
            dummy = random.choice([1, -1])
            padded.append(dummy)
    return padded


def padding_overhead(original_trace, padded_trace):
    """
    returns: float — percentage of dummy cells added
    """
    added = len(padded_trace) - len(original_trace)
    return (added / len(original_trace)) * 100


if __name__ == "__main__":
    sample_trace = [1, -1, 1, 1, -1, -1, 1, -1, 1, 1]
    for strength in ["light", "medium", "heavy"]:
        padded = apply_padding(sample_trace, strength)
        overhead = padding_overhead(sample_trace, padded)
        print(f"{strength}: original={len(sample_trace)}, padded={len(padded)}, overhead={overhead:.1f}%")