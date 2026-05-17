# 🎓 NRIIT Semester Result CLI Scraper

A lightweight, high-performance, stateless CLI scraper that fetches semester result links for **NRIIT Autonomous** students. 

By leveraging parallel multithreaded requests directly via standard Python HTTP protocols (no heavy browser automation or Selenium required), the scraper retrieves direct, clickable exam-cell result links in seconds!

---

## ✨ Features

- **Stateless & Zero Database**: Completely standalone and independent of databases. Identifies student names dynamically on-the-fly from active records.
- **Ultra-Fast Parallel execution**: Uses a Python `ThreadPoolExecutor` to check multiple semester result sheets concurrently.
- **Double-Mode CLI**:
  - **Interactive Mode**: Fallback prompts guide you step-by-step.
  - **Argument-Driven Mode**: Pass credentials directly as command-line arguments to bypass prompts.
- **Example/Demo Flag**: Run with `--example` to instantly query results using pre-configured test credentials.
- **Self-Cleaning Docker Wrapper (`run-cli.sh`)**: Builds, runs, and completely wipes all Docker containers, images, and builder caches on completion, leaving **zero footprint** on your machine.

---

## 🛠️ Folder Structure

All core scraper components are standalone at the root surface level of the repository:

```plaintext
cgpa-calculator-web-scraping/
├── scrapper.py        # Standalone, stateless Python CLI scraper
├── requirements.txt   # Minimal pinned dependencies (requests, bs4)
├── Dockerfile             # Lightweight python-slim runner
├── run-cli.sh             # Self-cleaning script (Build, Run, Clean Image/Cache)
├── LICENSE                # MIT License
└── README.md              # Project Documentation
```

---

## 🚀 Execution Guide

### Option A: Docker (Self-Cleaning / Zero Footprint)
This is the recommended method. The script automatically handles building, interactive running, and completely destroys the Docker container, image, and build caches upon exit (even if interrupted via `Ctrl+C`).

#### 1. Example Mode (Instant Test run)
Query real semester records instantly using pre-configured example credentials (`NRIA20`, `2022`, `2026`, `22KN1A05D8`):
```bash
./run-cli.sh --example
```

#### 2. Argument-Driven Mode
Bypass prompts by passing arguments directly:
```bash
./run-cli.sh --roll 22KN1A05D8 --reg NRIA20 --start 2022 --end 2026
```

*Arguments list:*
- `--roll`: Hall Ticket / Roll Number (e.g. `22KN1A05D8`)
- `--reg`: Regulation (e.g. `NRIA20`)
- `--start`: Starting academic year (e.g. `2022`)
- `--end`: Ending academic year (e.g. `2026`)
- `--example`: Runs with predefined demo details (bypasses other inputs)

#### 3. Interactive Mode
Run the self-cleaning script and follow the prompts:
```bash
./run-cli.sh
```

---

### Option B: Local Python Setup (Native)
If you prefer running natively in your terminal outside of Docker:

#### 1. Initialize a clean virtual environment
```bash
# Create the virtual environment
python3 -m venv venv

# Activate it
source venv/bin/activate
```

#### 2. Install minimal dependencies
We have stripped the package requirements list down to the absolute bare minimum:
```bash
pip install -r requirements.txt
```

#### 3. Run the Scraper

**Example Mode (Instant Test):**
```bash
python scrapper.py --example
```

**Argument-Driven Mode:**
```bash
python scrapper.py --roll 22KN1A05D8 --reg NRIA20 --start 2022 --end 2026
```

**Interactive Mode:**
```bash
python scrapper.py
```

---

## 📊 Sample Output (Example Mode Run)

```plaintext
=======================================================
🎓 NRIIT AUTONOMOUS SEMESTER RESULT CLI SCRAPER
=======================================================
💡 Running in Example Mode with default credentials...

🌐 Fetching announcement list from https://www.nriitexamcell.com/autonomous/results.php...

🔎 Found 57 result sheets matching NRIA20 in years 2022-2026.

⚡ Scraping 57 pages in parallel using 57 threads...
🎉 FOUND RECORDS in: III B.Tech I Sem (NRIA20), Reg/Supple, October-2024
👤 Student identified: PATSA NAGA SIVA SAI TEJA
🎉 FOUND RECORDS in: I B.Tech II Sem (NRIA20) Regular/Supple, June-2023
...

🎉 Parallel scraping finished in 0.34 seconds!

=======================================================
📖 DIRECT SEMESTER LINKS FOR 22KN1A05D8 (PATSA NAGA SIVA SAI TEJA)
=======================================================
1. 🏫 I B.Tech I Sem (NRIA20) Reg/Supple, Feb-2023
   🔗 Direct Link: https://www.nriitexamcell.com/autonomous/results/1-1-NRIA20-FEB-2023.php
2. 🏫 I B.Tech II Sem (NRIA20) Regular/Supple, June-2023
   🔗 Direct Link: https://www.nriitexamcell.com/autonomous/results/1-2-NRIA20-JUNE-2023.php
...
=======================================================

💡 Tip: Cmd+Click (on Mac) or Ctrl+Click (on Windows/Linux) the links above to open them directly in your web browser!
```

---

## 📝 License
This project is licensed under the **MIT License**. See [LICENSE](./LICENSE) for details.
