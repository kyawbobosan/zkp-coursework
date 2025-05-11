# ZKP Challenge Assistant (Coursework Submission)

This repository contains the final implementation of a Zero-Knowledge Proof (ZKP) challenge-response assistant developed for the MSc Cybersecurity Applied Cryptography module.

## 🔐 Features

- Implements Schnorr-based ZKP challenge-response
- Accepts user-supplied or randomly generated secrets
- Verifies knowledge without revealing the secret
- Generates:
  - ✅ Verification results
  - 📝 Logs in `.txt`, `.csv`, `.json`
  - 📊 Summary chart (via matplotlib)
  - 📦 Archived ZIP logs (optional)
- Supports `--headless` mode (skip chart for automation)

## 📁 Folder Structure

```
📁 core/
│   └── zkp_challenge.py
📁 logs/
│   ├── zkp_log.txt
│   ├── zkp_log.csv
│   └── zkp_log.json
📄 Zero_Knowledge_Proofs-Coursework.docx
📄 README.md
```

## ▶️ How to Run

1. Install required packages:
   ```
   pip install matplotlib pandas
   ```

2. Run the script:
   ```
   python core/zkp_challenge.py
   ```

3. To run without showing the chart (headless mode):
   ```
   python core/zkp_challenge.py --headless
   ```

## 📦 Output Files

- `zkp_log.txt` – Plain text audit trail
- `zkp_log.csv` – Structured CSV log
- `zkp_log.json` – Machine-readable JSON
- `logs/` – All logs stored and optionally zipped

## 📄 Submission

All coursework material, code, and logs are included in this repository.

---

🎓 *Developed by Kyaw San for MSc Cybersecurity (Napier University), 2025.*
