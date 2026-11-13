import json
from pathlib import Path

import numpy as np
from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    precision_recall_fscore_support,
)


def baseline_accuracy(labels):
    return 1 / len(set(labels))


def evaluate(y_true, y_pred):
    sites = sorted(set(y_true))
    acc = accuracy_score(y_true, y_pred)
    prec, rec, f1, support = precision_recall_fscore_support(
        y_true, y_pred, labels=sites, zero_division=0
    )

    per_site = {}
    for site, p, r, f, s in zip(sites, prec, rec, f1, support):
        per_site[site] = {
            "precision": float(p),
            "recall": float(r),
            "f1": float(f),
            "support": int(s),
        }

    return {
        "accuracy": float(acc),
        "baseline": baseline_accuracy(y_true),
        "n_sites": len(sites),
        "per_site": per_site,
    }


def confusion(y_true, y_pred):
    sites = sorted(set(y_true))
    return sites, confusion_matrix(y_true, y_pred, labels=sites)


def save_results(metrics, out_dir, y_true=None, y_pred=None):
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "metrics.json").write_text(json.dumps(metrics, indent=2))

    if y_true is not None and y_pred is not None:
        sites, cm = confusion(y_true, y_pred)
        np.savetxt(
            out_dir / "confusion_matrix.csv", cm,
            fmt="%d", delimiter=",", header=",".join(sites), comments="",
        )
    return out_dir


def print_summary(metrics):
    acc, base = metrics["accuracy"], metrics["baseline"]
    print(f"accuracy: {acc:.3f}  (baseline 1/N = {base:.3f}, {metrics['n_sites']} sites)")
    print(f"beats baseline by {acc - base:+.3f}")


if __name__ == "__main__":
    y_true = ["a", "a", "b", "b", "c", "c"]
    y_pred = ["a", "b", "b", "b", "c", "c"]
    m = evaluate(y_true, y_pred)
    print_summary(m)
    for site, s in m["per_site"].items():
        print(f"  {site}: precision={s['precision']:.2f} recall={s['recall']:.2f}")