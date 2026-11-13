import sys
from pathlib import Path

import numpy as np

from attack.config import DATA_DIR

MAX_LEN = 5000


def _row(path):
    dirs = []
    with open(path) as f:
        for line in f:
            parts = line.split()
            if len(parts) < 2:
                continue
            try:
                value = float(parts[1])
            except ValueError:
                continue
            dirs.append(1 if value > 0 else -1)
            if len(dirs) >= MAX_LEN:
                break
    if not dirs:
        return None
    row = np.zeros(MAX_LEN, dtype=np.int8)
    row[: len(dirs)] = dirs
    return row


def prepare(raw_dir, per_site=None, out_dir=DATA_DIR):
    raw_dir = Path(raw_dir)
    files = sorted(p for p in raw_dir.iterdir() if p.is_file() and "-" in p.name)

    X, y, counts = [], [], {}
    for i, path in enumerate(files):
        if i and i % 5000 == 0:
            print(f"  read {i}/{len(files)} files...")

        site = path.name.split("-")[0]
        if not site.isdigit():
            continue
        if per_site is not None and counts.get(site, 0) >= per_site:
            continue

        row = _row(path)
        if row is None:
            continue

        X.append(row)
        y.append(int(site))
        counts[site] = counts.get(site, 0) + 1

    X = np.stack(X)
    y = np.array(y, dtype=np.int16)

    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    np.save(out_dir / "X.npy", X)
    np.save(out_dir / "y.npy", y)
    print(f"saved {len(X)} traces from {len(set(y))} sites -> {out_dir}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("usage: python -m attack.prepare_dataset <raw_folder> [per_site_cap]")
        raise SystemExit(1)

    raw = sys.argv[1]
    cap = int(sys.argv[2]) if len(sys.argv) > 2 else None
    prepare(raw, per_site=cap)