## 📄 The Terminal-Style README.md

```markdown
# >_ Life-OS: Wellbeing Dashboard 🧠⚡

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://your-app-url.streamlit.app/)
[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/)
[![Gemini API](https://img.shields.io/badge/AI-Google_Gemini-orange.svg)](https://deepmind.google/technologies/gemini/)

```bash
user@mirai-internship:~$ ./execute_life_os.sh
> Initializing digital detox sequence...
> Loading screen time metrics...
> Establishing neural link with Gemini Life Coach...
> SYSTEM READY.

```

## 📖 Overview

Digital addiction is a modern epidemic. **Life-OS** is a data-driven Streamlit dashboard designed to visualize daily screen time and combat doomscrolling. Rather than just showing data, it integrates the **Google Gemini API** to act as a personalized, brutal-but-fair productivity coach that analyzes your habits and suggests real-world physical replacements for wasted digital time.

## ✨ Core Features

* **📊 The Command Center:** Interactive UI to filter 14 days of synthetic digital footprint data by date.
* **📈 Real-Time KPIs:** Dynamic metrics tracking total hours, top-used apps, and deltas against customizable daily screen time goals.
* **🤖 AI Data Bridge:** Aggregates Pandas dataframe metrics and feeds them into Gemini via a highly engineered system prompt.
* **⚡ Brutal-But-Fair Accountability:** Context-aware AI feedback that dynamically renders warnings based on how severely the user breached their screen time limits.

## 🛠️ Tech Stack

* **Frontend/Backend:** `Streamlit` (Python)
* **Data Processing:** `Pandas`
* **Artificial Intelligence:** `google-genai` (Gemini 2.5 Flash)

## 🚀 Local Installation

1. **Clone the repository:**
```bash
git clone [https://github.com/samudralasreelasya/life-os-dashboard.git](https://github.com/samudralasreelasya/life-os-dashboard.git)
cd life-os-dashboard

```


2. **Install dependencies:**
```bash
pip install -r requirements.txt

```


3. **Set up Environment Variables:**
Create a `.env` file in the root directory and add your Google Gemini API key:
```text
GEMINI_API_KEY="your_api_key_here"

```


4. **Run the Application:**
```bash
streamlit run app.py

```
