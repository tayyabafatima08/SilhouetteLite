import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

import pyshark
from attack.features.extract_features import extract_features

LOCAL_IP_HINT = None  # auto-detected from first packet if None

SITES = {
    "site1_example.pcap": "example.com",
    "site2_wikipedia.pcap": "wikipedia.org",
    "site3_github.pcap": "github.com",
    "site4_stackoverflow.pcap": "stackoverflow.com",
    "site5_bbc.pcap": "bbc.com",
}


def pcap_to_trace(pcap_path):
    cap = pyshark.FileCapture(str(pcap_path), display_filter="tcp.port==443")
    trace = []
    local_ip = None

    for pkt in cap:
        try:
            src = pkt.ip.src
            if local_ip is None:
                # first packet's source is assumed local (outgoing)
                local_ip = src
            trace.append(1 if src == local_ip else -1)
        except AttributeError:
            continue

    cap.close()
    return trace


def main():
    here = os.path.dirname(__file__)
    for filename, site_name in SITES.items():
        path = os.path.join(here, filename)
        if not os.path.exists(path):
            print(f"skip {filename}: not found")
            continue

        trace = pcap_to_trace(path)
        if not trace:
            print(f"{site_name}: no packets extracted")
            continue

        feats = extract_features(trace)
        print(f"{site_name}: trace_len={len(trace)}, feature_vector_len={len(feats)}, first_5_features={feats[:5]}")


if __name__ == "__main__":
    main()