# Attack Results

## Setup
- Dataset: undefended closed-world Tor traces (Wang / Tik-Tok "Undefended"), 95 sites.
  This run used 100 traces per site (9,500 traces total); the full set (~1,000 per
  site) can be used for the final numbers.
- Each trace is reduced to its +1 / -1 direction sequence (the sign of each packet),
  truncated and padded to 5,000 cells.
- Features: 67 traffic-shape features (counts, bursts, first-20 directions,
  20 chunk out-fractions, 20 cumulative samples).
- Model: random forest, 200 trees, stratified 80/20 split, seed 42.

## Headline result
- Accuracy: 0.866
- Random-guess baseline (1/95): 0.011
- The attack beats the baseline by +0.855. It identifies the visited site about
  87% of the time from encrypted traffic shape alone, without decrypting anything.

## What leaks the most
Top random-forest feature importances:

| Feature | Importance |
|---|---|
| out | 0.034 |
| chunk_out_1 | 0.033 |
| chunk_out_19 | 0.033 |
| chunk_out_18 | 0.032 |
| out_ratio | 0.032 |
| in | 0.031 |
| total | 0.030 |
| chunk_out_0 | 0.029 |
| cum_2 | 0.029 |
| cum_1 | 0.028 |

The outgoing/incoming balance and the cumulative shape of the page load are the
strongest signals; burst structure contributes but direction distribution dominates
on this dataset.

## Detailed metrics
- Confusion matrix: `attack/results/confusion_matrix.csv`
- Per-site precision / recall / F1 and the full metrics: `attack/results/metrics.json`

## Notes and limitations
- These numbers use the 100-trace-per-site subset for a fast run; the full set should
  give similar or slightly higher accuracy.
- This is the undefended baseline. The defense track measures how much dummy-cell
  padding lowers this accuracy and what it costs in bandwidth — that is the
  privacy-versus-cost result.