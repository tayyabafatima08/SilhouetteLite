from pathlib import Path

import numpy as np
from sklearn.model_selection import train_test_split

from attack.config import DATA_DIR, SEED


def _clean(trace):
    return [int(c) for c in trace if c == 1 or c == -1]


def load_real(data_dir=DATA_DIR):
    data_dir = Path(data_dir)
    x_npy, y_npy = data_dir / "X.npy", data_dir / "y.npy"

    if x_npy.exists() and y_npy.exists():
        X = np.load(x_npy, allow_pickle=True)
        y = np.load(y_npy, allow_pickle=True)
    else:
        npz_files = list(data_dir.glob("*.npz"))
        if not npz_files:
            return None
        bundle = np.load(npz_files[0], allow_pickle=True)
        if "X" not in bundle or "y" not in bundle:
            return None
        X, y = bundle["X"], bundle["y"]

    traces = [_clean(row) for row in X]
    labels = [str(label) for label in y]
    return traces, labels


def make_synthetic(n_sites=20, per_site=60, length=600, seed=SEED):
    rng = np.random.default_rng(seed)
    traces, labels = [], []

    for site in range(n_sites):
        out_bias = rng.uniform(0.3, 0.7)
        avg_run = rng.integers(2, 8)

        for _ in range(per_site):
            trace = []
            while len(trace) < length:
                direction = 1 if rng.random() < out_bias else -1
                run = max(1, int(rng.poisson(avg_run)))
                trace.extend([direction] * run)
            traces.append(trace[:length])
            labels.append(f"site_{site:02d}")

    return traces, labels


def load_dataset(data_dir=DATA_DIR, **synthetic_kwargs):
    real = load_real(data_dir)
    if real is not None:
        traces, labels = real
        return traces, labels, True

    traces, labels = make_synthetic(**synthetic_kwargs)
    return traces, labels, False


def split(traces, labels, test_size=0.2, seed=SEED):
    return train_test_split(
        traces, labels,
        test_size=test_size,
        random_state=seed,
        stratify=labels,
    )


if __name__ == "__main__":
    traces, labels, using_real = load_dataset()
    source = "real dataset" if using_real else "synthetic data"
    sites = sorted(set(labels))
    print(f"Loaded {len(traces)} traces from {source}")
    print(f"{len(sites)} sites, e.g. {sites[:3]}")
    print(f"first trace length: {len(traces[0])}, starts with {traces[0][:10]}")