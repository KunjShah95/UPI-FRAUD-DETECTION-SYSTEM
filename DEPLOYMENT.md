# Deployment Guide - UPI Fraud Detection System

This app is a Streamlit project (`main.py`) with a local model artifact:

- `UPI Fraud Detection updated.pkl`

## Handling the `.pkl` file in deployment (important)

Your app needs the model file at runtime. You have 3 safe patterns:

### Pattern A — Commit `.pkl` in repo (fastest, current setup)

Use this when:

- Model file is reasonably small.
- Repository is private, or model is not sensitive/proprietary.

What to do:

- Keep `UPI Fraud Detection updated.pkl` in project root.
- Keep current path fallback in `main.py` (already implemented).
- Ensure pinned compatible dependency:
  - `scikit-learn==1.6.1` in `requirements.txt`

Pros:

- Easiest deployment.
- No extra storage service required.

Cons:

- Increases repo size.
- Model is distributed with source code.

---

### Pattern B — Store `.pkl` in object storage (recommended for production)

Use this when:

- Model is large or sensitive.
- You want cleaner repo and model version control outside code.

Storage examples:

- Azure Blob Storage
- AWS S3
- GCP Cloud Storage

What to do:

1. Upload `.pkl` to private bucket/container.
2. Add secure access via environment variables (URL, token/SAS, key).
3. Download model at app startup to local temp path, then `pickle.load`.

Pros:

- Better security and scalability.
- No large binaries in git.

Cons:

- Requires cloud storage setup and credentials.

---

### Pattern C — Re-train and build model during CI/CD

Use this when:

- Training is deterministic and fast enough.
- You want fully reproducible pipelines.

Pros:

- No binary artifact committed.

Cons:

- Slower deploys.
- More moving parts in pipeline.

---

## Recommended choice for your current project

For now: **Pattern A** is okay and simplest.

When you move to production/team use: switch to **Pattern B**.

## `.pkl` do/don't checklist

- ✅ Do keep sklearn version aligned with training version.
- ✅ Do validate model load in startup checks.
- ✅ Do keep model path configurable for cloud.
- ❌ Don’t commit sensitive models to public repos.
- ❌ Don’t rely on ad-hoc local paths only.

## Best deployment options

1. **Streamlit Community Cloud** (easiest for Streamlit apps)
2. **Render** (good free starter web service)
3. **Railway** (quick containerized deploy)
4. **Azure App Service** (production-ready cloud option)

---

## 1) Deploy on Streamlit Community Cloud (recommended)

### Steps

1. Push your project to a GitHub repository.
2. Ensure these files exist in root:
   - `main.py`
   - `requirements.txt`
   - `UPI Fraud Detection updated.pkl`
3. Go to Streamlit Community Cloud and sign in with GitHub.
4. Click **New app**.
5. Select repository + branch.
6. Set **Main file path** to `main.py`.
7. Click **Deploy**.

### Notes

- If app crashes with package issues, verify `requirements.txt` is committed.
- Keep model file in repo root or adapt path logic to secrets/cloud storage.
- For private/prod deployments, prefer object storage for `.pkl` over committing binary in git.

---

## 2) Deploy on Render

### Setup

- Create a new **Web Service** from your GitHub repo.
- Runtime: Python

### Build command

`pip install -r requirements.txt`

### Start command

`streamlit run main.py --server.port $PORT --server.address 0.0.0.0`

### Environment

- No secrets required currently (unless you add APIs later).

---

## 3) Deploy on Railway

### Steps

1. Create new project from GitHub repo.
2. Add service and select your repo.
3. Set Start Command:
   `streamlit run main.py --server.port $PORT --server.address 0.0.0.0`
4. Railway auto-builds Python dependencies from `requirements.txt`.
5. Deploy and open generated URL.

---

## 4) Deploy on Azure App Service

### Steps

1. Create an Azure App Service (Linux, Python runtime).
2. Connect your GitHub repo to Deployment Center.
3. Set startup command:
   `streamlit run main.py --server.port 8000 --server.address 0.0.0.0`
4. Set App Setting `WEBSITES_PORT=8000`.
5. Save and restart app.

### Optional

- Move model file to Azure Blob Storage if repo size becomes large.
- Configure app settings for model URL / access token if loading model from Blob.

---

## Pre-deploy checklist

- [ ] `main.py` runs locally with `streamlit run main.py`
- [ ] `requirements.txt` is up to date
- [ ] `UPI Fraud Detection updated.pkl` is present and readable
- [ ] `main.py` uses robust model path lookup (already implemented)
- [ ] CSV upload works with your sample dataset

---

## Quick local smoke test before deploying

```powershell
.\.venv\Scripts\python.exe -m py_compile main.py
streamlit run main.py
```

If local works, cloud deployment usually works with minimal changes.
