import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from attack.load_dataset import load_dataset
from attack.model.predict import predict
from defense.padding.apply_padding import apply_padding, padding_overhead


def evaluate_defense(num_samples=50):
    traces, labels, _ = load_dataset()

    results = {"none": {"correct": 0, "total": 0, "overhead": 0.0}}
    for strength in ["light", "medium", "heavy"]:
        results[strength] = {"correct": 0, "total": 0, "overhead": 0.0}

    for i in range(min(num_samples, len(traces))):
        trace = traces[i]
        true_label = labels[i]

        # baseline: no padding
        out = predict(trace)
        results["none"]["total"] += 1
        if out["site"] == true_label:
            results["none"]["correct"] += 1

        # padded versions
        for strength in ["light", "medium", "heavy"]:
            padded = apply_padding(trace, strength)
            overhead = padding_overhead(trace, padded)
            out = predict(padded)

            results[strength]["total"] += 1
            results[strength]["overhead"] += overhead
            if out["site"] == true_label:
                results[strength]["correct"] += 1

    print(f"{'strength':<10} {'accuracy':<10} {'avg overhead %':<15}")
    for strength, r in results.items():
        acc = r["correct"] / r["total"]
        avg_overhead = r["overhead"] / r["total"] if r["total"] else 0
        print(f"{strength:<10} {acc:<10.3f} {avg_overhead:<15.1f}")

    return results


if __name__ == "__main__":
    evaluate_defense()