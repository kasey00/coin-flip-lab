# 🪙 Decision Science Coin-Flip Lab

A Dockerized Flask application that simulates "Random Walk" probability scenarios to demonstrate complex Decision Science concepts like **Volatility Drag**, **Opportunity Cost**, and **Statistical Symmetry**.

It runs thousands of simulations where a coin is flipped until heads and tails reach equilibrium (return to zero).

<img src="https://github.com/user-attachments/assets/b516ec60-570f-4469-ba9e-5e880251644b" width="800" alt="Dashboard Preview">

## 🧠 The Concepts
The app generates massive datasets (1B+ flips) to visualize:
* **The Volatility Trap:** Why correcting a small error takes exponentially longer than making it.
* **Efficiency vs. Churn:** Distinguishing between "lucky" streaks (Skill) and "grinder" streaks (Noise).
* **Statistical Symmetry:** Proving the Law of Large Numbers through Heads/Tails mirroring.

## 🛠️ Tech Stack
* **Backend:** Python 3.11, Flask, SQLAlchemy
* **Database:** PostgreSQL 15 (Docker Volume)
* **Infrastructure:** Docker Compose
* **Frontend:** HTML5, Bootstrap 5, Jinja2

## 🚀 Quick Start

### Prerequisites
* [Docker Desktop](https://www.docker.com/products/docker-desktop/) installed.

### Run the App
1.  **Clone the repository:**
    ```bash
    git clone https://github.com/kasey00/coin-flip-lab.git
cd coin-flip-lab
    ```

2.  **Start the container:**
    ```bash
    docker-compose up -d
    ```

3.  **Access the Dashboard:**
    Open [http://localhost:5000](http://localhost:5000)

4.  **Run Simulations:**
    Click **"+ Run 100"** to generate data.

## 💾 Backup & Restore Strategy
This project includes an automated script to backup the Docker volume to a portable `.tar.gz` file.

### How to Run a Backup
The script is located in `scripts/backup_db.sh`. It automatically detects your project folder, so it works on Linux, Mac, or Windows (via Git Bash).

1.  **Make the script executable** (Linux/Mac only):
    ```bash
    chmod +x scripts/backup_db.sh
    ```

2.  **Run the script:**
    ```bash
    ./scripts/backup_db.sh
    ```
    *Backups are saved to the `/backups` folder in your project root.*

### How to Restore
**Warning:** This overwrites existing data.

1.  Stop the database:
    ```bash
    docker-compose stop
    ```

2.  Run the restore command (Replace `[DATE]` with your specific file):
    ```bash
    # Defines the volume and runs the restore using Alpine
    docker run --rm \
      -v coin_app_postgres_data:/volume \
      -v $(pwd)/backups:/backup \
      alpine tar xzf /backup/db_backup_[DATE].tar.gz -C /volume
    ```

3.  Restart the database:
    ```bash
    docker-compose start
    ```

## 🛡️ License
**MIT License**

Copyright (c) 2026

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED.