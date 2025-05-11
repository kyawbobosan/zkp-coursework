# core/zkp_challenge.py
import random
import hashlib

# Public parameters (shared between prover and verifier)
p = 208351617316091241234326746312124448251235562226470491514186331217050270460481
g = 2

# === Key Generation ===
def generate_keypair():
    x = random.randint(1, p - 2)  # private key
    y = pow(g, x, p)              # public key
    return x, y

# === Issue Challenge ===
def issue_challenge():
    r = random.randint(1, p - 2)
    t = pow(g, r, p)
    return r, t

# === Calculate Challenge Hash ===
def compute_challenge(t, y):
    h = hashlib.sha256(f"{t}{y}".encode()).hexdigest()
    c = int(h, 16) % p
    return c

# === Generate Proof ===
def generate_proof(x, r, c):
    s = (r + c * x) % (p - 1)
    return s

# === Verify Proof ===
def verify_proof(y, t, c, s):
    left = pow(g, s, p)
    right = (t * pow(y, c, p)) % p
    return left == right

# === Full Challenge-Response ===
import csv

import matplotlib.pyplot as plt
import pandas as pd
import json

import sys
import zipfile
import os

if __name__ == "__main__":
    print("=== ZKP Challenge-Response Demo ===")
    headless = "--headless" in sys.argv
    x_input = input("Enter your own secret x (leave blank for random): ").strip()
    if x_input.isdigit():
        x = int(x_input)
    else:
        x, _ = generate_keypair()
    y = pow(g, x, p)
    print("(1) Secret x:", x)
    print("(2) Public y:", y)

    r, t = issue_challenge()
    print("(3) Commitment t:", t)

    c = compute_challenge(t, y)
    print("(4) Challenge c:", c)

    s = generate_proof(x, r, c)
    print("(5) Response s:", s)

    result = verify_proof(y, t, c, s)
    print("(6) Verification Result:", "✅ Success" if result else "❌ Failed")

    # Optional: Save result to zkp_log.txt
    try:
        with open("zkp_log.txt", "a", encoding="utf-8") as log_file:
            from datetime import datetime
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            log_file.write(f"[{timestamp}] ZKP Challenge | x={x} | y={y} | t={t} | c={c} | s={s} | Result: {'✅ Success' if result else '❌ Failed'}\n")


        # Also export to CSV
        csv_file = "zkp_log.csv"
        file_exists = False
        try:
            with open(csv_file, "r", encoding="utf-8") as check:
                file_exists = True
        except FileNotFoundError:
            pass

        with open(csv_file, "a", newline='', encoding="utf-8") as csvfile:
            fieldnames = ["timestamp", "x", "y", "t", "c", "s", "result"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            if not file_exists:
                writer.writeheader()
            writer.writerow({
                "timestamp": timestamp,
                "x": x,
                "y": y,
                "t": t,
                "c": c,
                "s": s,
                "result": "success" if result else "fail"
            })
            # Also export to JSON
        json_file = "zkp_log.json"
        json_entry = {
            "timestamp": timestamp,
            "x": x,
            "y": y,
            "t": t,
            "c": c,
            "s": s,
            "result": "success" if result else "fail"
        }
        try:
            with open(json_file, "r", encoding="utf-8") as jf:
                data = json.load(jf)
        except (FileNotFoundError, json.JSONDecodeError):
            data = []
        data.append(json_entry)
        with open(json_file, "w", encoding="utf-8") as jf:
            json.dump(data, jf, indent=4)

        # Optional: Display live summary chart
        try:
            df = pd.read_csv(csv_file)
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            df['date'] = df['timestamp'].dt.date
            summary = df.groupby(['date', 'result']).size().unstack(fill_value=0)
            summary.plot(kind='bar', stacked=True, color=['green', 'red'])
            plt.title("ZKP Challenge Results Over Time")
            plt.ylabel("Attempts")
            plt.xlabel("Date")
            plt.tight_layout()
            plt.grid(axis='y')
            if not headless:
                plt.show()
        except Exception as e:
            print("⚠️ Could not render chart:", e)

        # Optional: Create ZIP archive of logs
        try:
            log_dir = "logs"
            os.makedirs(log_dir, exist_ok=True)
            zip_name = os.path.join(log_dir, f"zkp_logs_{timestamp.replace(':', '-').replace(' ', '_')}.zip")
            with zipfile.ZipFile(zip_name, 'w') as zipf:
                for fname in ["zkp_log.txt", "zkp_log.csv", "zkp_log.json"]:
                    if os.path.exists(fname):
                        zipf.write(fname, arcname=os.path.basename(fname))
            print(f"📦 ZKP logs archived as {zip_name}")

            # Email export removed for coursework simplicity

            # Cleanup: keep only the 5 most recent ZIPs
            zip_files = sorted([
                f for f in os.listdir(log_dir) if f.startswith("zkp_logs_") and f.endswith(".zip")
            ], reverse=True)
            for old_zip in zip_files[5:]:
                try:
                    os.remove(os.path.join(log_dir, old_zip))
                    print(f"🗑️ Removed old log: {old_zip}")
                except Exception as cleanup_err:
                    print(f"⚠️ Could not delete {old_zip}: {cleanup_err}")
        except Exception as e:
            print("⚠️ Could not create ZIP archive:", e)
        except Exception as e:
            print("⚠️ Could not render chart:", e)

    except Exception as e:
        print("⚠️ Could not write log:", e)
