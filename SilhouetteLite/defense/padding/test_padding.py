from apply_padding import apply_padding, padding_overhead

def test_overhead_increases_with_strength():
    trace = [1, -1, 1, 1, -1, -1, 1, -1, 1, 1]
    overheads = {}
    for strength in ["light", "medium", "heavy"]:
        padded = apply_padding(trace, strength)
        overheads[strength] = padding_overhead(trace, padded)
    print(overheads)
    assert overheads["light"] < overheads["heavy"]


def test_overhead_across_multiple_traces():
    traces = [
        [1, -1, 1, 1, -1, -1, 1, -1, 1, 1],
        [1, 1, -1, -1, -1, 1, 1, -1],
        [-1, -1, 1, 1, 1, -1, 1, -1, -1, 1, 1, -1],
    ]

    print(f"{'trace_len':<10} {'strength':<10} {'overhead %':<10}")
    for trace in traces:
        for strength in ["light", "medium", "heavy"]:
            padded = apply_padding(trace, strength)
            overhead = padding_overhead(trace, padded)
            print(f"{len(trace):<10} {strength:<10} {overhead:<10.1f}")


if __name__ == "__main__":
    test_overhead_increases_with_strength()
    test_overhead_across_multiple_traces()