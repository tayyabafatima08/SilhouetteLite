import numpy as np

FIRST_N = 20
N_CHUNKS = 20
N_CUM = 20


def _runs(trace):
    runs = []
    count = 1
    for i in range(1, len(trace)):
        if trace[i] == trace[i - 1]:
            count += 1
        else:
            runs.append(count)
            count = 1
    runs.append(count)
    return runs


def extract_features(trace):
    trace = [c for c in trace if c == 1 or c == -1]
    total = len(trace)
    if total == 0:
        return [0.0] * len(FEATURE_NAMES)

    out = sum(1 for c in trace if c == 1)
    inc = total - out
    runs = _runs(trace)

    feats = [
        total,
        out,
        inc,
        out / total,
        len(runs),
        float(np.mean(runs)),
        float(np.max(runs)),
    ]

    first = trace[:FIRST_N] + [0] * max(0, FIRST_N - total)
    feats.extend(first)

    chunks = np.array_split(np.array(trace), N_CHUNKS)
    for chunk in chunks:
        feats.append(float(np.mean(chunk == 1)) if len(chunk) else 0.0)

    cumulative = np.cumsum(trace)
    idx = np.linspace(0, total - 1, N_CUM).astype(int)
    feats.extend(cumulative[idx].tolist())

    return [float(x) for x in feats]


def _make_names():
    names = ["total", "out", "in", "out_ratio", "num_runs", "mean_run", "max_run"]
    names += [f"first_{i}" for i in range(FIRST_N)]
    names += [f"chunk_out_{i}" for i in range(N_CHUNKS)]
    names += [f"cum_{i}" for i in range(N_CUM)]
    return names


FEATURE_NAMES = _make_names()


def extract_batch(traces):
    return np.array([extract_features(t) for t in traces])


if __name__ == "__main__":
    from attack.load_dataset import load_dataset

    traces, labels, _ = load_dataset()
    X = extract_batch(traces)
    print(f"{len(traces)} traces -> feature matrix {X.shape}")
    print(f"{len(FEATURE_NAMES)} features, e.g. {FEATURE_NAMES[:8]}")
    print(f"first row (first 8 values): {X[0][:8]}")