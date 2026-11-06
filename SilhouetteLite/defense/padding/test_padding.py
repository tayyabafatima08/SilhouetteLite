from apply_padding import apply_padding, padding_overhead

def test_overhead_increases_with_strength():
    trace = [1, -1, 1, 1, -1, -1, 1, -1, 1, 1]
    overheads = {}
    for strength in ["light", "medium", "heavy"]:
        padded = apply_padding(trace, strength)
        overheads[strength] = padding_overhead(trace, padded)
    print(overheads)
    assert overheads["light"] < overheads["heavy"]

if __name__ == "__main__":
    test_overhead_increases_with_strength()