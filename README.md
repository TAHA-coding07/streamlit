# 📡 Ad Hoc File Transfer Tracker

A professional, interactive **Streamlit web application** for tracking and managing ad hoc file transfers between devices. Built as a university Python laboratory assignment, this app demonstrates a wide range of Streamlit features including widgets, session state, data persistence, data visualization, and analytics.

---

## 📖 Project Overview

The Ad Hoc File Transfer Tracker helps users log wireless file transfers made between devices over **WiFi Direct, Bluetooth, NFC, or Hotspot** connections. You can add, edit, search, filter, and delete records, visualize transfer statistics with interactive **Plotly** charts, and export the dataset in **CSV or JSON** format. All data is persisted automatically in a CSV file.

---

## ✨ Features

- 🏠 **Home** – Project introduction, objectives, and features.
- 📊 **Dashboard** – Live metric cards (total, completed, pending, failed, file-size stats) and a completion progress bar.
- ➕ **Add Transfer** – Fully validated data-entry form.
- 📋 **View Transfers** – Browse, edit, and delete records with confirmation.
- 🔎 **Search & Filter** – Multi-column keyword search plus connection/status filters.
- 📈 **Analytics** – 5 interactive Plotly charts that update automatically.
- ⬇️ **Download Dataset** – Export as CSV or JSON.
- ℹ️ **About** – Project and developer information.
- 💾 **CSV persistence** & session state for automatic refresh.
- 🎨 Responsive, modern, and colorful UI with emojis.

---

## 🛠️ Installation Steps

1. **Install Python 3.9+** from [python.org](https://python.org).
2. **Clone or download** this repository.
3. **Create and activate a virtual environment** (recommended):

   ```bash
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # macOS / Linux
   source venv/bin/activate
   ```

4. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

---

## ▶️ How to Run

With the virtual environment active, run:

```bash
streamlit run app.py
```

Your browser will open automatically at `http://localhost:8501`.

---

## ☁️ Deployment Steps (Streamlit Community Cloud)

1. Push your project to a **GitHub repository**.
2. Go to [Streamlit Community Cloud](https://streamlit.io/cloud) and sign in with GitHub.
3. Click **"New app"**.
4. Select your repository, branch, and set the **Main file path** to `app.py`.
5. Click **"Deploy"**.

Streamlit will automatically install packages from `requirements.txt` and host your app.

---

## 🖼️ Screenshots Section

> Add screenshots of your running app here. Place image files in the `screenshots/` folder and reference them like:

```markdown
![Home Page](screenshots/home.png)
![Dashboard](screenshots/dashboard.png)
![Analytics](screenshots/analytics.png)
```

---

## 📂 Project Structure

```
AdHocFileTransferTracker/
│
├── app.py              # Main Streamlit application
├── transfers.csv       # Sample dataset (12 records)
├── requirements.txt    # Python dependencies
├── README.md           # This file
├── assets/
│   └── logo.png        # Optional placeholder logo
└── screenshots/        # Optional app screenshots
```

---

## 🚀 GitHub Upload Steps

```bash
git init
git add .
git commit -m "Initial commit: Ad Hoc File Transfer Tracker"
git branch -M main
git remote add origin https://github.com/<your-username>/<your-repo>.git
git push -u origin main
```

---

## 💡 Notes

- The dataset currently contains **12 realistic sample records**.
- All new, edited, or deleted records are saved back to `transfers.csv` automatically.
- The app is self-contained and runs without any configuration changes.

---

© 2024 Ad Hoc File Transfer Tracker · Developed by **Your Name** · University Python Laboratory
