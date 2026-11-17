# HTTPS Demo Trace Capture

Captured using tshark (Wireshark CLI) on Windows.

## Command used
& “C:\Program Files\Wireshark\tshark.exe” -i <interface_number> -f “tcp port 443” -w <output_file>.pcap

- Interface found via `tshark -D` (Wi-Fi was interface 2 on capture machine)
- Filter: `tcp port 443` (HTTPS traffic only)
- Process: start capture, visit target site fully in browser, wait ~5s after load, Ctrl+C to stop

## Sites captured
1. example.com
2. wikipedia.org
3. github.com
4. stackoverflow.com
5. bbc.com

Note: these traces are for demonstrating the feature-extraction pipeline on real traffic only. They are NOT used to train or evaluate the classifier.