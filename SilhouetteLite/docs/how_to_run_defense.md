# How to Run — Defense Track (SilhouetteLite)

## Prerequisites
- Python 3.11
- Install dependencies:

py -m pip install -r requirements.txt
py -m pip install matplotlib pyshark

- Wireshark (with tshark + Npcap) installed, only needed for re-capturing HTTPS demo traces

## 1. Train the attack model (needed before running defense experiments)

py -m attack.model.train_classifier

Uses synthetic data automatically if the real dataset isn't present in `data/`.

## 2. Test the padding module standalone

py defense/padding/apply_padding.py
py defense/padding/test_padding.py


## 3. Run the defense evaluation (padding vs classifier accuracy)

py -m defense.experiments.run_defense_eval

Prints accuracy and average bandwidth overhead for none/light/medium/heavy padding.

## 4. Generate the accuracy-vs-overhead plot

py -m defense.experiments.plot_overhead_curve

Saves to `defense/results/accuracy_vs_overhead.png`.

## 5. Run the HTTPS feature-extraction demo
Pre-captured `.pcap` files are already included in `defense/https_demo_traces/`. To re-run feature extraction on them:

py defense/https_demo_traces/extract_demo.py

To capture new traces yourself, see `defense/https_demo_traces/capture.md`.

## Notes
- HTTPS demo traces are for pipeline demonstration only and are never passed to the classifier for training or evaluation.
- Defense results use synthetic data until the real DF Tor dataset is added to `data/` by the Attack track.