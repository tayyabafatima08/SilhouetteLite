# Attack Results

## Setup
- Dataset: undefended closed-world Tor traces (Wang / Tik-Tok "Undefended"), 95 sites,
  all ~105,000 traces (about 1,100 per site).
- Each trace is reduced to its +1 / -1 direction sequence (the sign of each packet),
  truncated and padded to 5,000 cells.
- Features: 67 traffic-shape features (counts, bursts, first-20 directions,
  20 chunk out-fractions, 20 cumulative samples).
- Model: random forest, 200 trees, stratified 80/20 split, seed 42.

## Headline result
- Accuracy: 0.935
- Random-guess baseline (1/95): 0.011
- The attack beats the baseline by +0.925. It identifies the visited site about
  93.5% of the time from encrypted traffic shape alone, without decrypting anything.

## Per-site performance
Results are even across sites, not driven by a few easy ones:

| Metric (macro-averaged over 95 sites) | Value |
|---|---|
| Precision | 0.936 |
| Recall | 0.935 |
| F1 | 0.935 |

Hardest sites (lowest F1):

| Site | Precision | Recall | F1 |
|---|---|---|---|
| site_13 | 0.82 | 0.82 | 0.82 |
| site_58 | 0.86 | 0.79 | 0.82 |
| site_62 | 0.85 | 0.81 | 0.83 |
| site_76 | 0.87 | 0.82 | 0.84 |
| site_35 | 0.79 | 0.92 | 0.85 |

Easiest sites (highest F1):

| Site | Precision | Recall | F1 |
|---|---|---|---|
| site_52 | 1.00 | 1.00 | 1.00 |
| site_69 | 1.00 | 0.99 | 0.99 |
| site_07 | 0.99 | 0.99 | 0.99 |
| site_43 | 0.99 | 0.98 | 0.99 |
| site_75 | 0.98 | 0.99 | 0.98 |

The full per-site table is in `attack/results/metrics.json`; the confusion matrix is
in `attack/results/confusion_matrix.csv`.

## What leaks the most
Top random-forest feature importances:

| Feature | Importance |
|---|---|
| out | 0.040 |
| out_ratio | 0.038 |
| chunk_out_1 | 0.036 |
| chunk_out_19 | 0.036 |
| chunk_out_18 | 0.033 |
| in | 0.032 |
| cum_2 | 0.031 |
| chunk_out_0 | 0.031 |
| total | 0.030 |
| cum_1 | 0.029 |

The outgoing/incoming balance (`out`, `out_ratio`, `in`, `total`), how the outgoing
share is spread across the load (`chunk_out_*`), and the cumulative shape (`cum_*`)
are the strongest signals. Direction distribution dominates on this dataset.

## Notes and limitations
- This is the undefended baseline. The defense track measures how much dummy-cell
  padding lowers this accuracy and what it costs in bandwidth — that is the
  privacy-versus-cost result.
- A random forest on summary features is deliberately simple; deep models in the
  literature reach higher accuracy but are out of scope here.