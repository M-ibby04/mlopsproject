# 🏥 MLOps Health Risk Assessment System

A production-grade **Federated Learning** system for real-time health risk assessment combining vital signs and environmental exposure data. This project implements distributed machine learning with data drift detection, conditional retraining, and dual dashboard interfaces for citizens and health authorities.

---

## 🎯 Project Overview

This MLOps project addresses health risk assessment across multiple cities in Pakistan by:

- **Federated Learning**: Training models across distributed clients (hospitals and city centers) without centralizing sensitive health data
- **Real-time Predictions**: AI-powered health risk classification from vital signs and air quality metrics
- **Data Drift Detection**: Automated monitoring for concept drift with conditional model retraining
- **Dual Dashboards**: Citizen portal for personalized health insights and authority command center for population-level monitoring
- **Production API**: FastAPI deployment for real-time predictions with comprehensive logging

### Key Features

✅ **Federated Averaging (FedAvg)**: Manual implementation for distributed model training  
✅ **Data Preprocessing**: Unified pipeline for air quality and WESAD (wearable) data  
✅ **Multi-Client Architecture**: Support for 5 hospital clients + 5 city centers  
✅ **Drift Detection**: Statistical monitoring with automated retraining triggers  
✅ **Interactive Dashboards**: Streamlit-based citizen and admin portals  
✅ **REST API**: FastAPI backend for model serving with prediction logging  
✅ **Containerization**: Docker support for seamless deployment  

---

## 📊 Data Sources

The system integrates two primary data streams:

### 1. **City Air Quality Data** 🌍
- **Source**: Environmental monitoring stations across Pakistani cities
- **Metrics**: PM2.5, NO₂, CO levels, temperature
- **Cities**: Islamabad, Lahore, Karachi, Peshawar, Quetta
- **Processing**: Normalization across features

### 2. **Hospital Vital Signs (WESAD Dataset)** 🏥
- **Source**: Wearable sensors from hospital patients
- **Metrics**: Heart rate, body temperature, stress levels
- **Subjects**: 5 hospital clients (S2-S9)
- **Processing**: Zero-padding for missing environmental data

### 3. **Output Labels**: 8-class health risk classification (0-7)
- Class imbalance addressed with weighted loss functions

---

## 🏗️ Project Architecture

```
mlopsproject/
├── src/
│   ├── preprocessing/          # Data cleaning & normalization
│   │   ├── clean_city.py
│   │   ├── clean_wesad.py
│   │   └── align_hospital_timestamps.py
│   │
│   ├── federated/              # Federated learning core
│   │   ├── model.py            # Neural network architecture
│   │   ├── client.py           # Client-side training
│   │   ├── manual_fedavg.py    # FedAvg implementation
│   │   └── eval_global_model.py
│   │
│   ├── evaluation/             # Model evaluation & monitoring
│   │   ├── central_baseline.py
│   │   ├── data_drift.py
│   │   └── eval_federated_on_merged.py
│   │
│   ├── training/               # Retraining pipelines
│   │   └── retrain_if_drift.py
│   │
│   ├── dashboard/              # Streamlit interfaces
│   │   ├── main_dashboard.py   # Authentication & routing
│   │   ├── citizen_dashboard.py
│   │   └── admin_dashboard.py
│   │
│   ├── deployment/             # Production APIs
│   │   └── api.py              # FastAPI prediction server
│   │
│   └── utilis/                 # Utilities
│       ├── experiment_tracker.py
│       └── dummy_data.py
│
├── data/
│   ├── raw/                    # Raw data (not in repo)
│   │   ├── city/
│   │   └── hospitals/
│   │
│   ├── processed/              # Preprocessed datasets
│   │   ├── city/
│   │   ├── hospital/
│   │   ├── merged_hospitals/
│   │   ├── test/
│   │   └── eval/
│   │
│   └── real_backup/            # Data backups
│
├── models_tff/                 # Trained models (Keras format)
│   ├── baseline_central_model.keras
│   └── manual_fedavg_global_model.keras
│
├── notebooks/                  # Analysis & experimentation
│   ├── eda_air_quality.ipynb
│   ├── eda_wesad.ipynb
│   ├── data_drift.ipynb
│   ├── evaluation.ipynb
│   └── manual_fedavg_eval.ipynb
│
├── logs/                       # Runtime logs
│   ├── api_predictions.jsonl
│   └── experiments.csv
│
├── Dockerfile                  # Container configuration
├── requirements.txt            # Python dependencies
├── run_pipeline.sh             # Automated pipeline script
└── README.md                   # This file
```

---

## 🚀 Quick Start

### Prerequisites

- **Python 3.9+**
- **Docker** (optional, for containerization)
- **Git** (for version control)
- Raw data files (see Data Preparation section)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/M-ibby04/mlopsproject.git
   cd mlopsproject
   ```

2. **Set up Python environment**
   ```bash
   # Create virtual environment
   python -m venv venv
   
   # Activate (Windows)
   venv\Scripts\activate
   
   # Activate (macOS/Linux)
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Prepare data** (see next section)

---

## 📥 Data Preparation

### Phase 1: Preprocessing

**IMPORTANT**: Raw data must be prepared before training.

#### Step 1: Place Raw Files

Download and organize data:

```
data/raw/city/
├── islamabad_complete_data.csv
├── lahore_complete_data.csv
├── karachi_complete_data.csv
├── peshawar_complete_data.csv
└── quetta_complete_data.csv

data/raw/hospitals/
├── S2/
│   └── S2.pkl
├── S3/
│   └── S3.pkl
├── S4/, S5/, S9/
...
```

#### Step 2: Run Preprocessing Scripts

**City Data** (Air Quality)
```bash
python src/preprocessing/clean_city.py
```
- **Output**: `data/processed/city/client_city_*.csv`
- **Features**: Timestamp, HeartRate, Temp, PM25, NO2, CO_Level, Label
- **Processing**: Pollution normalized, health features zero-padded

**Hospital Data** (WESAD)
```bash
python src/preprocessing/clean_wesad.py
```
- **Output**: `data/processed/hospital/client_hospital_*.csv`
- **Features**: Same as city data
- **Processing**: Health features normalized, pollution features zero-padded

**Merge Hospital Data** (optional, for centralized baseline)
```bash
python src/preprocessing/merge_city_hospital.py
```
- **Output**: `data/processed/merged_hospitals/client_merged_*.csv`

---

## 🤖 Training & Evaluation

### Option 1: Run Full Pipeline

Execute the complete ML pipeline automatically:

```bash
bash run_pipeline.sh
```

This runs:
1. Preprocessing (city data)
2. Central baseline training
3. Federated learning (manual FedAvg)
4. Global model evaluation
5. Data drift detection
6. Conditional retraining

### Option 2: Run Individual Steps

**Train Baseline Model**
```bash
python src/evaluation/central_baseline.py
```
- Trains on merged/centralized data
- Establishes performance benchmark

**Train Federated Model**
```bash
python src/federated/manual_fedavg.py
```
- Implements manual FedAvg across clients
- 10 communication rounds by default
- Each client trains locally, then shares weights

**Evaluate Models**
```bash
python src/federated/eval_global_model.py
python src/evaluation/eval_federated_on_merged.py
```
- Compares federated vs. centralized performance
- Generates evaluation metrics and confusion matrices

**Detect Data Drift**
```bash
python src/evaluation/data_drift.py
```
- Statistical tests (KS, Wasserstein)
- Triggers retraining if drift is HIGH

**Conditional Retraining**
```bash
python src/training/retrain_if_drift.py
```
- Automatically retrains if drift detected

---

## 📱 Dashboards

### Citizen Portal 🚀

Interactive health risk assessment interface for citizens.

**Launch**:
```bash
streamlit run src/dashboard/main_dashboard.py
```

**Features**:
- 👤 Patient information input
- 💓 Vital signs entry (interactive sliders or manual)
- 🌍 Environmental exposure data
- 🎯 Real-time health risk classification
- 📊 Personalized health advice based on risk level
- 🏥 Emergency contacts and health resources
- 📈 Historical trend analysis

**Risk Levels**:
- **Low Risk** (Class 0): Safe, continue normal activities
- **Moderate Risk** (Class 1-3): Monitor symptoms, take precautions
- **High Risk** (Class 4-7): Seek medical attention

### Authority Portal 👨‍💼

Command center for health authorities to monitor population health.

**Launch**:
```bash
streamlit run src/dashboard/main_dashboard.py
```
(Select "Access Authority Portal" after login)

**Features**:
- 🏙️ Multi-city comparative analysis
- 📊 Real-time population health metrics
- 🗺️ Geographic risk distribution map
- ⏰ Environmental trends over time
- 📈 Statistical summaries (mean, peak, std dev)
- 📥 CSV/JSON export for reporting
- 🔄 Data refresh controls

**Dashboard Sections**:
1. System Status Dashboard (5 KPIs)
2. Inter-City Comparative Analysis
3. Detailed City-Level Monitoring
4. Geographic Risk Distribution Map
5. Command Center Controls

---

## 🔌 API Deployment

### Start Prediction Server

```bash
python -m uvicorn src.deployment.api:app --host 0.0.0.0 --port 8000
```

**API Documentation**: http://localhost:8000/docs

### API Endpoints

#### POST `/predict`

Make predictions on new data.

**Request**:
```json
{
  "HeartRate": 75,
  "Temp": 36.5,
  "PM25": 50.0,
  "NO2": 25.0,
  "CO_Level": 1.5
}
```

**Response**:
```json
{
  "prediction": 2,
  "raw_output": [0.05, 0.12, 0.35, 0.28, 0.15, 0.03, 0.02, 0.00]
}
```

#### GET `/health`

Health check endpoint.

**Response**:
```json
{
  "status": "healthy"
}
```

### Prediction Logging

All predictions are logged to `logs/api_predictions.jsonl` with:
- Timestamp
- Input parameters
- Classification output
- Raw prediction probabilities

---

## 🐳 Docker Deployment

### Build Docker Image

```bash
docker build -t mlops_fl:latest .
```

### Run Services

**API Server**:
```bash
docker run --rm -p 8000:8000 \
  -v $(pwd):/app -w /app \
  mlops_fl \
  uvicorn src.deployment.api:app --host 0.0.0.0 --port 8000
```

**Streamlit Dashboard**:
```bash
docker run --rm -p 8501:8501 \
  -v $(pwd):/app -w /app \
  mlops_fl \
  python -m streamlit run src/dashboard/main_dashboard.py \
  --server.port 8501 --server.address 0.0.0.0
```

---

## 🔐 Authentication

### Dashboard Login

**Admin Access**:
- **Username**: admin
- **Password**: `admin123` (or set `ADMIN_PASSWORD` env var)

**Citizen Access**:
- No credentials required
- Direct access via "Access Citizen Portal" button

---

## 📊 Experiment Tracking

### Log Experiments

Utilities are provided for tracking ML experiments:

```python
from src.utilis.experiment_tracker import ExperimentTracker

tracker = ExperimentTracker()
tracker.log_experiment(
    name="FedAvg_Round_1",
    metrics={"accuracy": 0.85, "loss": 0.32},
    model_path="models_tff/manual_fedavg_global_model.keras"
)
```

**Output**: `logs/experiments.csv`

---

## 📚 Model Architecture

### Neural Network

```
Input Layer: 5 features
    ↓
Batch Normalization
    ↓
Dense(256, ReLU) + Dropout(0.3)
    ↓
Dense(128, ReLU) + Dropout(0.3)
    ↓
Dense(64, ReLU) + Dropout(0.3)
    ↓
Dense(8, Softmax) → 8 health risk classes
```

### Features (Normalized)

| Feature     | Source | Range | Unit |
|-------------|--------|-------|------|
| HeartRate   | Wearable | 50-150 | BPM |
| Temperature | Wearable | 35-42 | °C |
| PM2.5       | Air Quality | 0-500 | µg/m³ |
| NO₂         | Air Quality | 0-200 | ppb |
| CO_Level    | Air Quality | 0-50 | ppm |

### Loss Function

**Weighted Sparse Categorical Crossentropy**
```
Addresses class imbalance with per-class weights:
[1.0, 3.0, 3.0, 4.0, 4.0, 6.0, 6.0, 6.0]
```

---

## 🔍 Data Drift Detection

### Methodology

Monitors distributions across multiple clients using:

1. **Kolmogorov-Smirnov (KS) Test**
   - Detects distribution shifts in individual features
   - Threshold: p-value < 0.05

2. **Wasserstein Distance**
   - Measures Earth Mover's Distance between distributions
   - Threshold: distance > 0.3

3. **Population-Level Aggregation**
   - Drift severity: NONE, LOW, MEDIUM, HIGH
   - Triggers retraining if HIGH

### Triggers

```python
if drift_level == "HIGH":
    trigger_retraining()
```

---

## 📈 Performance Metrics

### Classification Metrics

- **Accuracy**: Overall correct predictions
- **Precision/Recall**: Per-class performance
- **F1-Score**: Weighted harmonic mean
- **Confusion Matrix**: Class-level misclassifications

### Federated Learning Metrics

- **Communication Rounds**: Number of FL iterations
- **Local Epochs**: Training epochs per client per round
- **Model Convergence**: Loss trajectory across rounds
- **Communication Cost**: Bandwidth consumed for weight exchange

---

## 🛠️ Troubleshooting

### Common Issues

**Issue**: `FileNotFoundError: data/processed/city/*.csv`
```
Solution: Run preprocessing scripts first
python src/preprocessing/clean_city.py
```

**Issue**: Port 8501 already in use
```
Solution: Use different port
streamlit run src/dashboard/main_dashboard.py --server.port 8502
```

**Issue**: Model not found error
```
Solution: Train model first
python src/federated/manual_fedavg.py
```

**Issue**: Out of memory during training
```
Solution: Reduce batch size or use smaller dataset
Edit hyperparameters in respective training scripts
```

---

## 🔗 Dependencies

### Core ML Libraries
- `tensorflow==2.13.1` - Deep learning framework
- `scikit-learn` - Machine learning utilities
- `numpy` - Numerical computing
- `pandas` - Data manipulation

### Web & API
- `fastapi` - REST API framework
- `uvicorn` - ASGI server
- `streamlit` - Dashboard framework
- `plotly` - Interactive visualizations

### Data Processing
- `openpyxl` - Excel file handling
- `jupyter` - Interactive notebooks

---

## 📖 Notebooks

### Exploratory Data Analysis

- **`eda_air_quality.ipynb`**: City air quality data exploration
- **`eda_wesad.ipynb`**: Hospital vital signs analysis

### Model Evaluation

- **`evaluation.ipynb`**: Comprehensive model performance analysis
- **`manual_fedavg_eval.ipynb`**: Federated learning results
- **`data_drift.ipynb`**: Drift detection case studies

---

## 🤝 Contributing

1. Create a feature branch
   ```bash
   git checkout -b feature/your-feature
   ```

2. Make changes and commit
   ```bash
   git commit -m "Add your feature"
   ```

3. Push and create pull request
   ```bash
   git push origin feature/your-feature
   ```

---

## 📝 License

This project is part of an MLOps research initiative. Please contact the maintainers for licensing details.

---

## 📞 Contact & Support

**Project Members**: Muhammad Ibrahim 22i0586, Reha Yamin 22i0573, Abdullah Sipra 22i1392  
**Repository**: https://github.com/M-ibby04/mlopsproject

For issues, questions, or suggestions:
1. Open an issue on GitHub
2. Review troubleshooting section above
3. Check existing documentation

---


