# 📄 Resume Screening & Job Recommendation App

A machine‑learning powered web application built with **Flask** that analyzes resumes, extracts key information, predicts the candidate’s job category, and recommends the most suitable job role.

This project supports **PDF and TXT** resumes and uses **NLP + ML models** to classify resumes into categories such as IT, HR, Finance, Data Science, Sales, etc.

---

## 🚀 Features

### ✔ Resume Upload  
- Supports **PDF** and **TXT** files  
- Extracts raw text from uploaded resumes  

### ✔ Information Extraction  
Automatically extracts:
- Name  
- Email  
- Phone Number  
- Address  
- Skills  
- Education  
- Experience  

### ✔ Machine Learning Predictions  
- Predicts **resume category** using a trained Random Forest model  
- Recommends a **job role** based on the predicted category  

### ✔ Clean User Interface  
- Simple and user‑friendly HTML interface  
- Displays extracted information and predictions clearly  

---

## 🧠 Machine Learning Models Used

### 1️⃣ Resume Categorization  
- **Model:** Random Forest Classifier  
- **Vectorizer:** TF‑IDF  
- **Output:** Category (e.g., IT, HR, Finance, Data Science)

### 2️⃣ Job Recommendation  
- **Model:** Random Forest Classifier  
- **Vectorizer:** TF‑IDF  
- **Output:** Recommended job title  

---


---

## 🛠 Installation & Setup

### 1️⃣ Clone the repository
```bash
git clone https://github.com/sai-lakshmi-gunturu/resume_screening_app.git
cd resume_screening_app

2️⃣ Create a virtual environment
python -m venv .venv

3️⃣ Activate the environment
Windows:

bash
.venv\Scripts\activate

4️⃣ Install dependencies
bash
pip install -r requirements.txt

5️⃣ Run the Flask app
bash
python app.py


6️⃣ Open in browser
Code
http://127.0.0.1:5000/


📌 How It Works
User uploads a resume

App extracts text using PyPDF2

Text is cleaned and vectorized

ML model predicts the resume category

Another ML model recommends a job role

Extracted information + predictions are displayed on the UI

📷 Screenshots

Code
![Upload Page](screenshots/upload.png)
![Results Page](screenshots/results.png)


🧑‍💻 Technologies Used
Python

Flask

Scikit‑learn

PyPDF2

Regex

HTML / CSS

Jinja2 Templates

⭐ Future Enhancements
Add support for DOCX resumes

Deploy on Render / Railway

Add charts for skill visualization

Add login system for recruiters

👩‍💻 Author
Sai Lakshmi Gunturu  
GitHub: https://github.com/sai-lakshmi-gunturu (github.com in Bing)

❤️ Support
If you like this project, please ⭐ the repository!