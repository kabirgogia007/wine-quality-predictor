# 🍷 VinoVeritas - Wine Quality Prediction System

A full-stack machine learning application predicting wine quality with a premium, wine-themed interface.
Transformed from a simple script to a robust React + FastAPI architecture.

## Project Structure

```
Wine Quality Prediction/
├── backend/                 # FastAPI Server & ML Logic
│   ├── server.py            # API Endpoints (/predict, /eda, /report)
│   ├── train_model.py       # Model training script
│   ├── eda_plots.py         # Visualization generator
│   ├── generate_report.py   # Report generator
│   └── ...artifacts         # (.joblib, .json, .png)
│
└── frontend/                # React + Vite Application
    ├── src/
    │   ├── components/      # UI Components (Layout, etc.)
    │   ├── pages/           # Pages (Landing, Predict, Dashboard, Report)
    │   └── ...
    └── ...
```

## Setup & Installation

### 1. Backend Setup
Navigate to the backend directory and install Python dependencies.
```bash
cd backend
pip install -r requirements.txt
```
**Run the Server:**
```bash
uvicorn server:app --reload
```
The API will run at `http://localhost:8000`.

### 2. Frontend Setup
Navigate to the frontend directory and install Node dependencies.
```bash
cd frontend
npm install
```
**Run the Client:**
```bash
npm run dev
```
The App will run at `http://localhost:5173`.

## Usage Flow
1. **Train Model**: If not done, run `python train_model.py` in `backend/`.
2. **Generate Plots**: Run `python eda_plots.py` in `backend/`.
3. **Start App**: Launch both server and client.
4. **Predict**: Use the form to get real-time quality assessments.
5. **Analyze**: View EDA plots in the Dashboard.
6. **Report**: Check the generated markdown report in the App.

## Tech Stack
- **Frontend**: React, Vite, TailwindCSS, Framer Motion, Axios.
- **Backend**: FastAPI, Scikit-Learn, Pandas, Joblib.
- **Design**: "Burgundy & Gold" premium aesthetic.


