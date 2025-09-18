from flask import Flask, render_template, request
import spacy
import PyPDF2
import re

app = Flask(__name__)

# Load spacy model
nlp = spacy.load("en_core_web_sm")

@app.route("/", methods=["GET", "POST"])
def index():
    name, email, phone, skills = None, None, None, []

    if request.method == "POST":
        file = request.files["file"]

        if file:
            # Extract text from PDF
            reader = PyPDF2.PdfReader(file)
            text = ""
            for page in reader.pages:
                text += page.extract_text() or ""

            # Extract Name (NER example)
            doc = nlp(text)
            for ent in doc.ents:
                if ent.label_ == "PERSON":
                    name = ent.text
                    break

            # Extract Email
            email_match = re.search(r"[\w\.-]+@[\w\.-]+", text)
            if email_match:
                email = email_match.group(0)

            # Extract Phone
            phone_match = re.search(r"\+?\d[\d\s-]{8,}\d", text)
            if phone_match:
                phone = phone_match.group(0)

            # Extract Skills only under "Skills" section
            skills_section = re.search(r"skills(.*)", text, re.IGNORECASE | re.DOTALL)
            if skills_section:
                skills_text = skills_section.group(1)
                keywords = ["Python", "Java", "C++", "HTML", "CSS", "JavaScript", "SQL", "Machine Learning"]
                skills = [kw for kw in keywords if kw.lower() in skills_text.lower()]

    return render_template("index.html", name=name, email=email, phone=phone, skills=skills)

if __name__ == "__main__":
    app.run(debug=True)
