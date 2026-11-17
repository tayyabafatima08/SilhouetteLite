# Defense Track — Results (SilhouetteLite)

## Overview
This document summarizes the dummy-cell padding defense results: how much it reduces
classifier accuracy, at what bandwidth cost, tested on 200 synthetic-data samples
across 20 sites (real-dataset results pending).

## 1. Padding Overhead (Task 1-2)
`apply_padding()` inserts dummy cells at three strengths:

| Strength | Target rate | Observed avg overhead |
|----------|------------|------------------------|
| Light    | 10%        | ~10.0%                 |
| Medium   | 30%        | ~29.9%                 |
| Heavy    | 60%        | ~60.0%                 |

Overhead scales predictably with strength, confirmed across traces of varying length
(tested at lengths 8, 10, and 12 cells, see `defense/padding/test_padding.py`).

## 2. Attack Accuracy Under Padding (Task 3-4)
Classifier accuracy on 200 samples, 20 sites (random baseline = 5%):

| Strength | Accuracy | Avg Overhead |
|----------|----------|---------------|
| None     | 0.820    | 0.0%          |
| Light    | 0.165    | 10.0%         |
| Medium   | 0.105    | 29.9%         |
| Heavy    | 0.065    | 60.0%         |

See plot: `defense/results/accuracy_vs_overhead.png`

## 3. Key Finding
Even light padding (10% bandwidth overhead) is enough to collapse classifier accuracy
from 82% to 16.5% — a disproportionately large drop relative to the overhead cost.
This happens because several extracted features (chunk-based direction ratios,
cumulative-sum samples at fixed positions) are sensitive to the exact trace length.
Padding shifts these feature values even with a small number of inserted cells,
which is enough to flip the classifier's prediction in most cases.

Diminishing returns are visible past light padding: medium and heavy padding reduce
accuracy further, but at a steeper bandwidth cost for a smaller additional accuracy
drop (light→medium: -6.0pp accuracy for +19.9pp overhead; medium→heavy: -4.0pp
accuracy for +30.4pp overhead). This suggests light padding may already capture most
of the practical defensive benefit on this feature set.

## 4. Limitations
- Results above use synthetic traffic data; real DF Tor dataset results pending
  integration from the Attack track.
- Baseline comparison against the dataset's own pre-defended trace versions is not
  yet complete (depends on real dataset + defended-version files being added).
- A known bug in `attack/load_dataset.py`'s `_label()` function (empty except block)
  will need fixing before real-data labels can be processed.

## 5. HTTPS Demo (Task 5)
Feature extraction was verified end-to-end on 5 real HTTPS traffic captures
(example.com, wikipedia.org, github.com, stackoverflow.com, bbc.com), confirming the
pipeline works on real traffic shapes, not just synthetic data. These traces were
used only for this demonstration and were not passed to the classifier for training
or evaluation. See `defense/https_demo_traces/`.