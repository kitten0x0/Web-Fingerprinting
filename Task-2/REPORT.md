# Task 2: Real-World Website Fingerprinting Dataset Collection


## 1. Collection Methodology

I engineered a data collection pipeline capable of capturing high-fidelity network traffic. To ensure realistic web behavior and bypass anti-bot mechanisms, a sequence of practical evasion techniques was utilized to orchestrate the downloads.

**Technical Pipeline:**
1.  **Multi-Browser Simulation**: `wget --page-requisites` simulates a full browser load, fetching the root HTML, Javascript, CSS, and media assets.
2.  **Stealth Execution**: 
    - Full HTTP headers injected (e.g., rotating User-Agents, `Accept-Language`, `DNT=1`).
    - Stateful authentication cookies were actively managed and piped directly into `wget` to maintain persistence and avoid stateless bot detection.
3.  **Network Resilience**: Dynamic IP backoff (15-30 seconds) and target URL diversification (e.g., `/tags` vs `/`) were implemented to defeat aggressive 429 Rate Limiting from sites like Adobe and StackOverflow.
4.  **Packet Capture**: `tcpdump` was operated via `sudo` on wireless interface `wlp1s0` to explicitly capture raw `.pcap` files during the entire HTTP request lifecycle.

## 2. Dataset Specifications

The final dataset is a robust, perfectly balanced array of live internet traffic.

| Specification | Value |
| :--- | :--- |
| **Total Classes (Websites)** | 20 (Google, Adobe, StackOverflow, GitHub, Reddit, etc.) |
| **Traces per Class** | 120 |
| **Total Global Traces** | 2,400 Validated Sessions |
| **Total Dataset Size** | ~40 GB |
| **Capture Interface** | `wlp1s0` |
| **Hardware Used** | AMD Ryzen 5 7430U, 8GB RAM |

## 3. Data Processing & Normalization

Processing 40GB of raw PCAP data into an ML-ready format required an "Eco-Mode" conversion script (`normalize_dataset.py`) using serial execution to prevent RAM starvation.

**Feature Extraction Matrix:**
- **Rows**: 2,401 (Header + 2,400 traces)
- **Columns**: 15,001 (1 Label + 5,000 packets × 3 features)
- **Extracted Vectors**: `[Relative Timestamp, Packet Byte Size, Directionality (-1/1)]`

## 4. Directory Structure

All Task 2 artifacts, data, and code are strictly organized within the `Task_2/` directory:

- `scripts/normalize_dataset.py`: The parsing tool for converting PCAPs to CSV.
- `research_dataset/`: The raw 40GB directory containing 2,400 PCAPs and associated JSON metadata.
- `research_dataset_final.csv`: The final 293MB normalized feature matrix ready for scikit-learn.

## 5. Verification Check

Before concluding Task 2, the following quality assurance checks were enforced globally:
- [x] Every trace verified to return HTTP Status: 200 OK.
- [x] Every trace verified to contain `> 250` packets (assuring a complete page load).
- [x] Missing or corrupted traces automatically discarded and re-collected.
- [x] Directory exact balance check complete: 120 traces × 20 folders.

---
**Status**: TASK 2 DATA COLLECTION 100% COMPLETE. Dataset ready for ML model training.
