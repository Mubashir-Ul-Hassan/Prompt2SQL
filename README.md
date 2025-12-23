# 📊 Prompt2SQL

**Prompt2SQL** is an AI-powered Streamlit application that allows users to upload CSV or Excel files and ask natural language questions to get data-driven insights instantly. The app uses **Google Gemini (Generative AI)** to act as a smart data analyst, summarizing datasets, identifying patterns, and answering analytical questions — all without writing SQL or code.

🚀 **Live Demo (Deployed on Hugging Face Spaces):**
👉 [https://huggingface.co/spaces/MubashirUlHassan/Prompt2SQL](https://huggingface.co/spaces/MubashirUlHassan/Prompt2SQL)

---

## ✨ Features

* 📤 Upload **CSV, XLSX, or XLS** files
* 📊 Automatic data profiling:

  * Dataset shape
  * Column names & data types
  * Descriptive statistics
  * Missing value analysis
* 👀 Interactive data preview (first rows, stats, schema)
* 💬 Chat-based interface to ask questions about your data
* 🤖 AI-powered insights using **Google Gemini**
* 🔐 Secure API key handling via environment variables (Hugging Face Secrets)

---

## 🧠 How It Works

1. Upload a CSV or Excel file
2. The app generates a structured data summary
3. Your question + data context is sent to **Gemini**
4. The AI responds with accurate, data-backed insights

Example questions:

* "Summarize the key statistics"
* "Which columns have the most missing values?"
* "What trends do you see in this dataset?"
* "Give insights based on the data"

---

## 🛠️ Tech Stack

* **Streamlit** – UI & app framework
* **Google Generative AI (Gemini)** – Data analysis reasoning
* **Pandas** – Data processing
* **openpyxl / xlrd** – Excel file support

---

## 📦 Requirements

Create a `requirements.txt` file with the following content:

```txt
streamlit
google-generativeai
pandas
openpyxl
xlrd
```

---

## 🔑 Environment Variables

This app requires a Google Gemini API key.

### For Hugging Face Spaces:

1. Go to **Settings → Secrets**
2. Add:

```
GOOGLE_API_KEY=your_api_key_here
```

The app will automatically read it from the environment.

---

## 🧪 Local Setup (Optional)

If you want to run the app locally:

```bash
git clone https://github.com/your-username/Prompt2SQL.git
cd Prompt2SQL
pip install -r requirements.txt
streamlit run app.py
```

Make sure to set your API key:

```bash
export GOOGLE_API_KEY=your_api_key_here
```

---

## 📁 Project Structure

```
Prompt2SQL/
│── app.py              # Main Streamlit app
│── README.md           # Project documentation
│── requirements.txt    # Dependencies
```

> Note: `streamlit_app.py` is a default Streamlit template and is **not used** in production.

---

## 🌐 Deployment

The application is deployed on **Hugging Face Spaces** using:

* SDK: Streamlit
* App file: `app.py`

Deployment metadata is managed via the Hugging Face README YAML header.

---

## 🙌 Author

**Mubashir Ul Hassan**
AI & Data Applications Developer

---

## 📜 License

This project is open-source and available under the **MIT License**.

---

⭐ If you find this project useful, consider giving it a star on GitHub!
