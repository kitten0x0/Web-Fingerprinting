import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

# --- Configuration ---
DATASET_CSV = "../../Task_2/research_dataset_final.csv"
REPORT_DIR = "../reports"

def main():
    if not os.path.exists(DATASET_CSV):
        print(f"Error: Dataset not found at {DATASET_CSV}")
        return

    print("Loading dataset for analysis...")
    df = pd.read_csv(DATASET_CSV)
    
    # 1. Label Distribution
    label_counts = df['label'].value_counts()
    print("\n--- Class Distribution ---")
    print(label_counts)
    
    # 2. Packet Count Analysis
    # Every 3rd feature starting from column 3 is direction. 
    # Direction is 0 if it's padding.
    # We can detect real packet count by looking at direction columns.
    direction_cols = [col for col in df.columns if col.startswith('d_')]
    pkt_counts = (df[direction_cols] != 0).sum(axis=1)
    
    print("\n--- Packet Count Statistics ---")
    print(pkt_counts.describe())
    
    # 3. Simple Feature Analysis (First 10 packets)
    first_sizes = [col for col in df.columns if col.startswith('s_')][:10]
    print("\n--- Average Size of First 10 Packets ---")
    print(df[first_sizes].mean())

    # 4. Save summary stats to a file
    summary_file = os.path.join(REPORT_DIR, "dataset_summary.txt")
    with open(summary_file, 'w') as f:
        f.write("RESEARCH-GRADE DATASET SUMMARY\n")
        f.write("=============================\n")
        f.write(f"Total Traces: {len(df)}\n")
        f.write(f"Unique Sites: {len(label_counts)}\n\n")
        f.write("Traces per site:\n")
        f.write(label_counts.to_string())
        f.write("\n\nPacket Count Stats:\n")
        f.write(pkt_counts.describe().to_string())
    
    print(f"\nAnalysis complete. Summary saved to {summary_file}")

if __name__ == "__main__":
    os.makedirs(REPORT_DIR, exist_ok=True)
    main()
