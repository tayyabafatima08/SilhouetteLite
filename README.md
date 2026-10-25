# SilhouetteLite: Website Fingerprinting Attack and Defense on Encrypted Traffic

Term project for **CS3002 Information Security (Fall 2026)**, FAST-NUCES Lahore.
Instructor: Ms. Sarah Abid Khan

**Status:** Proposal stage. Implementation in progress.

## Overview

Encryption (HTTPS, VPN, Tor) hides the content of network traffic but not its shape: the sizes, directions and timing of packets. SilhouetteLite shows that a passive observer can still infer which website a user visited from an encrypted traffic trace, then tests how much a dummy-cell padding defense helps and what it costs in bandwidth.

## The Problem

Many users assume nobody can tell which sites they visit because their traffic is encrypted. But each website loads with a characteristic packet pattern, so someone watching the encrypted stream (same Wi-Fi, ISP, or a Tor entry node) can identify the site without decrypting anything. This attack is called **website fingerprinting**.

## What We Do

1. **Attack:** Train a random forest on extracted traffic-shape features (optional small CNN) using a public Tor dataset, to predict the visited site from a trace.
2. **Web interface:** A small web page where the user picks or uploads a trace and sees the predicted site, confidence, the main leaking feature types, a risk verdict, and before/after defense results.
3. **Defense:** Apply dummy-cell padding, which inserts extra cells to disguise each site's traffic pattern, and re-run the same attack on the defended traces.
4. **Cost:** Measure the defense cost as bandwidth overhead (percentage of dummy cells added), at several padding strengths (light, medium, heavy).
5. **Result:** A privacy-versus-cost analysis, with a short threat model and a discussion of limitations.

## Risk Verdict

The attack's confidence is mapped to a verdict:

| Confidence | Verdict |
|---|---|
| above 70% | HIGH |
| 40% to 70% | MEDIUM |
| below 40% | LOW |

## Evaluation Outputs

- Accuracy compared with the random-guess baseline (1/N)
- Confusion matrix
- Per-site precision and recall
- Accuracy-vs-overhead curve (defense run at several padding strengths)
- Comparison against the dataset's existing defended versions as baselines

## Scope

**In scope**
- Closed-world website fingerprinting on Tor (about 50 to 100 sites)
- Public Deep Fingerprinting dataset [1]: 95 sites, about 1,000 traces each, direction-only (+1 / -1 per cell, no timestamps)
- One defense: dummy-cell padding, applied by cell position rather than by time
- Web interface with one user role, upload validation (type, size, structure) and an action log
- A small set of our own HTTPS captures (about 5 sites), used only to demonstrate that our capture and feature-extraction pipeline works on real traffic. These traces are not used to train a model, evaluate the defense, or passed to the classifier.

**Out of scope**
- Decrypting any traffic
- Live interception of other users' traffic
- Open-world identification
- Real-time / online classification
- Cross-channel comparison (Tor and HTTPS results are reported separately)
- Real timing and delay effects (the dataset has no timestamps)
- Defeating state-of-the-art published defenses
- Per-trace explanations (the interface reports the feature types the model relies on most)
- Multi-role access control, PDF export, production hosting

## Tech Stack (planned)

- Python, scikit-learn (optionally PyTorch for the CNN)
- Selenium, tcpdump / scapy for capturing our own traces
- Lightweight web interface (Streamlit or FastAPI)

## Ethics

This tool is a measuring instrument for privacy risk, not a tool for deanonymizing real users. We analyze only public datasets and traces captured from our own browsing. We never intercept anyone else's traffic.

## Team

| Name | Roll No. |
|---|---|
| Isbah Arif | 23L-3014 |
| Eshal Shahid | 23L-3086 |
| Tayyaba Fatima | 23L-0947 |

## References

[1] P. Sirinam, M. Imani, M. Juarez, and M. Wright, "Deep Fingerprinting: Undermining Website Fingerprinting Defenses with Deep Learning," arXiv:1801.02265, Jan. 2018. https://arxiv.org/abs/1801.02265

[2] V. Rimmer, D. Preuveneers, M. Juarez, T. Van Goethem, and W. Joosen, "Automated Website Fingerprinting through Deep Learning," in Proc. Network and Distributed System Security Symp. (NDSS), 2018. https://doi.org/10.14722/ndss.2018.23105

[3] M. S. Rahman, P. Sirinam, N. Mathews, K. G. Gangadhara, and M. Wright, "Tik-Tok: The Utility of Packet Timing in Website Fingerprinting Attacks," Proc. Privacy Enhancing Technologies, vol. 2020, no. 3, pp. 5-24, July 2020. https://doi.org/10.2478/popets-2020-0043
