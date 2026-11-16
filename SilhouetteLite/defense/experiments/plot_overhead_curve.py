import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

import matplotlib.pyplot as plt
from defense.experiments.run_defense_eval import evaluate_defense


def plot_curve(results):
    strengths = ["none", "light", "medium", "heavy"]
    accuracies = []
    overheads = []

    for s in strengths:
        r = results[s]
        accuracies.append(r["correct"] / r["total"])
        overheads.append(r["overhead"] / r["total"] if r["total"] else 0)

    plt.figure(figsize=(7, 5))
    plt.plot(overheads, accuracies, marker="o")
    for s, x, y in zip(strengths, overheads, accuracies):
        plt.annotate(s, (x, y), textcoords="offset points", xytext=(5, 5))

    plt.xlabel("Bandwidth Overhead (%)")
    plt.ylabel("Classifier Accuracy")
    plt.title("Accuracy vs Padding Overhead")
    plt.grid(True)

    out_path = os.path.join(os.path.dirname(__file__), "..", "results", "accuracy_vs_overhead.png")
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    plt.savefig(out_path)
    print(f"saved plot -> {out_path}")


if __name__ == "__main__":
    results = evaluate_defense(num_samples=200)
    plot_curve(results)