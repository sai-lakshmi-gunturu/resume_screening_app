from csv import reader
from email import message
from unicodedata import category

from flask import Flask, request, render_template
import pickle
from PyPDF2 import PdfReader
import re

app= Flask(__name__)


#load models..........
rf_classifier_categorization=pickle.load(open('models/rf_classifier_categorization.pkl','rb'))
tfidf_vectorizer_categorization=pickle.load(open('models/tfidf_vectorizer_categorization.pkl','rb'))


rf_classifier_job_recommendation=pickle.load(open('models/rf_classifier_job_recommendation.pkl','rb'))
tfidf_vectorizer_job_recommendation=pickle.load(open('models/tfidf_vectorizer_job_recommendation.pkl','rb'))


#  CLEANING FUNCTION ------------------

def cleanResume(txt):
    txt = re.sub(r'http\S+', ' ', txt)
    txt = re.sub(r'RT|cc', ' ', txt)
    txt = re.sub(r'#\S+', '', txt)
    txt = re.sub(r'@\S+', ' ', txt)
    txt = re.sub(r'[^\w\s]', ' ', txt)
    txt = re.sub(r'\s+', ' ', txt)
    return txt.strip()

# - PDF TO TEXT ------------------

def pdf_to_txt(file):
    reader = PdfReader(file)
    text = ""
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text
    return text

# - CATEGORY → JOB MAPPING ------------------

CATEGORY_TO_JOB = {
    "accountant": "Senior Accountant",
    "banking": "Banking Officer",
    "finance": "Financial Analyst",
    "hr": "HR Executive",
    "it": "Software Developer",
    "data science": "Data Scientist",
    "sales": "Sales Executive",
    "admin": "Admin Executive",
    "customer service": "Customer Support Associate",
    "bpo": "Customer Support Associate",
    "teacher": "Teacher",
}




# CATEGORY PREDICTION.......
def predict_category(resume_text):
    resume_text = cleanResume(resume_text)
    resume_tfidf = tfidf_vectorizer_categorization.transform([resume_text])
    predicted_category = rf_classifier_categorization.predict(resume_tfidf)[0]
    return predicted_category






# JOB RECOMMENDATION......
def recommended_job(resume_text):
    resume_text = cleanResume(resume_text)
    resume_tfidf = tfidf_vectorizer_job_recommendation.transform([resume_text])
    predicted_category= rf_classifier_job_recommendation.predict(resume_tfidf)[0]
    # map category → job
    recommended_job = CATEGORY_TO_JOB.get(predicted_category.lower(), "Job Not Mapped")

    return recommended_job





# Resume parsing.........
def extract_name(text):
    lines = text.split("\n")
    return lines[0].strip() if lines else None


def extract_email(text):
    pattern = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
    match = re.search(pattern, text)
    return match.group() if match else None


def extract_phone(text):
    pattern = r"\b(?:(?:\+?\d{1,3}[-.\s]?)?(?:\(?\d{3}\)?[-.\s]?)?\d{3}[-.\s]?\d{4})\b"
    match = re.search(pattern, text)
    return match.group() if match else None

def extract_skills(text):
    skills_list = [
        "python", "java", "c++", "sql", "machine learning", "data analysis",
        "excel", "communication", "teamwork", "leadership", "django",
        "html", "css", "javascript", "react", "node", "pandas", "numpy"
    ]
    text_lower = text.lower()
    return [skill for skill in skills_list if skill in text_lower]


def extract_education(text):
    keywords = [
        "bachelor", "master", "phd", "b.sc", "m.sc", "btech", "mtech",
        "b.tech", "m.tech", "mba", "university", "college"
    ]
    text_lower = text.lower()
    return [edu for edu in keywords if edu in text_lower]


def extract_experience(text):
    pattern = r"[A-Za-z ]+ at [A-Za-z0-9 .,&]+ \(\d{4}[-–]\d{4}\)"
    return re.findall(pattern, text)


def extract_address(text):
    pattern = r"Address:\s*(.*)"
    match = re.search(pattern, text)
    return match.group(1).strip() if match else None





#routes path..............
@app.route("/")
def resume():
    return render_template("resume.html")

@app.route("/predict",methods=["POST"])
def predict():
    if 'resume' in request.files:
        file=request.files['resume']
        filename=file.filename

        if filename.endswith('.pdf'):
            text=pdf_to_txt(file)
        elif filename.endswith('.txt'):
            text=file.read().decode('utf-8')
        else:
            return render_template('resume.html',message="Invalid file format, Please upload a PDF or TXT file..")
        
        category = predict_category(text)
        job = recommended_job(text)

        # INFORMATION EXTRACTION

        phone = extract_phone(text)
        email = extract_email(text)
        name = extract_name(text)
        address = extract_address(text)
        extracted_skills = extract_skills(text)
        extracted_education = extract_education(text)
        extracted_experience = extract_experience(text)

        return render_template('resume.html',predicted_category= category,
                               recommended_job=job,
                                phone=phone,
                                name=name,
                                email=email,
                                address=address,
                                extracted_skills=extracted_skills,
                                extracted_education=extracted_education,
                                extracted_experience=extracted_experience)

    else:
        return render_template('resume.html',message='No resume file uploaded.')
        



#python main
if __name__=="__main__":
    app.run(debug=True)