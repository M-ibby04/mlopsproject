# 🛠 Phase 1 – Preprocessing (MUST BE DONE BEFORE TRAINING)

Before running any training, each teammate **must generate the processed datasets locally**.  
These processed files are used by the Federated Learning clients in Phase 2.

Raw data is **not included** in the repository.  
You MUST place raw files in the correct folders, then run the preprocessing scripts.

---

## 1. Preprocess City Data (Air Quality)

### Step 1 — Place Raw Files
Download all air-quality CSV/XLSX files (e.g., Islamabad, Lahore, Karachi…).

Place them here:
data/raw/city/

EXAMPLE:
data/raw/city/islamabad_complete_data.xlsx
data/raw/city/karachi_complete_data.xlsx

### Step 2 — Run Preprocessing

From the repo root:

```bash
python src/preprocessing/clean_city.py

OUTPUT:
Processed files are generated here:
data/processed/city/

Example output file:

client_city_islamabad.csv

These CSVs contain:
Timestamp, HeartRate, Temp, PM25, NO2, CO_Level, Label

Health features = zero padded, pollution features = normalized.

2. Preprocess Hospital Data (WESAD)
Step 1 — Place Raw WESAD Folders

Download WESAD dataset and place subject folders (S2, S3, S4…) here:

data/raw/hospitals/


Example:

data/raw/hospitals/S2/S2.pkl
data/raw/hospitals/S3/S3.pkl

Step 2 — Run Preprocessing
python src/preprocessing/clean_wesad.py

Output

Processed files appear here:

data/processed/hospital/


Example:

client_hospital_S2.csv

These CSVs contain:
Timestamp, HeartRate, Temp, PM25, NO2, CO_Level, Label


Pollution features = zero padded, health features = normalized.

PREPROCESSING MUST BE RUN BEFORE TRAINING

Phase 2 Federated Learning scripts depend on these files:

data/processed/city/*.csv
data/processed/hospital/*.csv


If preprocessing is not run, training will fail because the model cannot find node data.

Make sure each you have:

Correct raw data in data/raw/

Correct processed data in data/processed/

Ran both preprocessing scripts successfully

Once preprocessing is complete, proceed to:

src/federated/client.py
src/federated/server.py

for Phase 2 (training + federated averaging).