# Deployment Guide for Wine Quality Advisor

This guide will walk you through deploying the Backend to **Render** and the Frontend to **Vercel**.

## Prerequisites
- A GitHub account.
- This project pushed to a GitHub repository.

## 1. Deploy Backend to Render

1.  Log in to [Render](https://render.com/).
2.  Click **New +** -> **Web Service**.
3.  Connect your GitHub repository.
4.  Configure the service:
    *   **Name**: `wine-quality-backend` (or similar)
    *   **Root Directory**: `backend`
    *   **Runtime**: `Python 3`
    *   **Build Command**: `pip install -r requirements.txt`
    *   **Start Command**: `uvicorn server:app --host 0.0.0.0 --port $PORT`
5.  Click **Create Web Service**.
6.  Wait for deployment to finish. Copy the **Service URL** (e.g., `https://wine-backend.onrender.com`).

**Note**: Ensure `best_model_wine_quality.joblib` and `feature_names.json` are committed to your repo!

## 2. Deploy Frontend to Vercel

1.  Log in to [Vercel](https://vercel.com/).
2.  Click **Add New...** -> **Project**.
3.  Import your GitHub repository.
4.  Configure the project:
    *   **Framework Preset**: Vite
    *   **Root Directory**: `frontend`
    *   **Environment Variables**:
        *   Key: `VITE_API_URL`
        *   Value: The Render URL from Step 1 (e.g., `https://wine-backend.onrender.com`) - **IMPORTANT**: No trailing slash!
5.  Click **Deploy**.

## 3. Verify Deployment

1.  Open the Vercel deployment URL.
2.  Click **Assess Quality**.
3.  Fill out the form and submit.
4.  If it works, you have successfully deployed the Wine Quality Advisor!
