import re
import PyPDF2
import spacy
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from collections import Counter

# Load English language model for spaCy
nlp = spacy.load("en_core_web_sm")

def extract_text_from_pdf(pdf_path):
    """Extracts text from a PDF file."""
    text = ""
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            text += page.extract_text() or ""
    return text

def extract_email(text):
    """Extracts email using Regex."""
    email = re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', text)
    return email[0] if email else "Not found"

def extract_name(text):
    """Extracts name using spaCy NLP."""
    doc = nlp(text)
    for entity in doc.ents:
        if entity.label_ == "PERSON":
            return entity.text
    return "Not found"

def extract_skills(text):
    """Extracts skills using keyword matching."""
    skills_list = ['python', 'java', 'sql', 'machine learning', 'aws', 'excel']
    found_skills = []
    for skill in skills_list:
        if re.search(rf'\b{skill}\b', text.lower()):
            found_skills.append(skill.title())
    return found_skills if found_skills else ["Not found"]

def generate_wordcloud(skills):
    """Creates a Word Cloud from skills."""
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(' '.join(skills))
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.show()

def main():
    resume_files = ["resume1.pdf", "resume2.pdf", "resume3.pdf"]
    all_skills = []

    for resume in resume_files:
        print(f"\nProcessing: {resume}")
        text = extract_text_from_pdf(resume)
        
        print("=== Extracted Information ===")
        print(f"Name: {extract_name(text)}")
        print(f"Email: {extract_email(text)}")
        
        skills = extract_skills(text)
        print("Skills:", ", ".join(skills))
        
        all_skills.extend(skills)

    if all_skills:
        print("\nGenerating Word Cloud...")
        generate_wordcloud(all_skills)

if __name__ == "__main__":
    main()