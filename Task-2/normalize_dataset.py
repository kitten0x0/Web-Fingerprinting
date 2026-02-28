import os
import glob
import json
import concurrent.futures
from scapy.all import rdpcap, IP
import pandas as pd
import socket
import time

# --- Configuration ---
RAW_DIR = "../research_dataset"
PROCESSED_BASE = "../processed_dataset"
MASTER_CSV = "../research_dataset_final.csv"
TARGET_PACKETS = 5000
MIN_PACKETS = 250 # Match collector's MIN_PACKETS

def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('8.8.8.8', 1))
        local_ip = s.getsockname()[0]
    except:
        local_ip = '127.0.0.1'
    finally:
        s.close()
    return local_ip

def normalize_trace(pcap_path, site_name, local_ip):
    """
    Extracts [timestamp, size, direction], filters, and pads/truncates to 5000 packets.
    """
    try:
        packets = rdpcap(pcap_path)
    except Exception as e:
        return None

    if len(packets) < 5: # Critical safety check
        return None

    data = []
    start_time = float(packets[0].time)
    
    for pkt in packets:
        if IP in pkt:
            timestamp = float(pkt.time) - start_time
            size = len(pkt)
            
            if pkt[IP].src == local_ip:
                direction = 1
            else:
                direction = -1
                
            data.append(timestamp)
            data.append(size)
            data.append(direction)

    # Truncate
    if len(data) > TARGET_PACKETS * 3:
        data = data[:TARGET_PACKETS * 3]
    
    # Pad
    while len(data) < TARGET_PACKETS * 3:
        data.extend([0.0, 0, 0]) 

    return [site_name] + data

def main():
    local_ip = get_local_ip()
    print(f"Using local IP: {local_ip}")
    
    all_pcaps = []
    sites = sorted([d for d in os.listdir(RAW_DIR) if os.path.isdir(os.path.join(RAW_DIR, d))])
    for site in sites:
        pcaps = glob.glob(os.path.join(RAW_DIR, site, "*.pcap"))
        for p in pcaps:
            all_pcaps.append((p, site))
    
    # Balanced Concurrency: Use half of available cores to avoid overloading
    max_workers = max(1, os.cpu_count() // 2)
    print(f"Processing {len(all_pcaps)} traces in BALANCED-TURBO (Workers: {max_workers})...")
    
    headers = ["label"]
    for i in range(1, TARGET_PACKETS + 1):
        headers.extend([f"t_{i}", f"s_{i}", f"d_{i}"])
    
    # Write headers first
    with open(MASTER_CSV, 'w') as f:
        f.write(",".join(headers) + "\n")
    
    count = 0
    with concurrent.futures.ProcessPoolExecutor(max_workers=max_workers) as executor:
        # Submit all tasks
        futures = {executor.submit(normalize_trace, p, s, local_ip): (p, s) for p, s in all_pcaps}
        
        # Process results as they complete
        for future in concurrent.futures.as_completed(futures):
            res = future.result()
            if res:
                # Append directly to file to keep memory footprint tiny
                with open(MASTER_CSV, 'a') as f:
                    line = ",".join(map(str, res))
                    f.write(line + "\n")
            
            count += 1
            if count % 100 == 0:
                print(f"Progress: {count}/{len(all_pcaps)} (Balanced-Turbo Active)")

    print(f"Done! Final dataset saved to {MASTER_CSV}")

if __name__ == "__main__":
    main()
