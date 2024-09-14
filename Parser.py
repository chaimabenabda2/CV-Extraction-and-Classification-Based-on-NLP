import os
import re
import PyPDF2
from PIL import Image
import streamlit as st
from pyresparser import ResumeParser
import spacy
from spacy.matcher import Matcher
nlp = spacy.load('en_core_web_sm')

def convert_to_txt(path):
    pdf_file = open(path, 'rb')
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    text = ''
    for page_num in range(len(pdf_reader.pages)):
        # page = pdf_reader.getPage(page_num)
        page = pdf_reader.pages[page_num]
        text += page.extract_text()

    pdf_file.close()

    # print(text)
    return text

def extract_phone_number(text):
    #phone_pattern = r'\b\d{2}[-.\s]?\d{3}[-.\s]?\d{3}\b'
    phone_pattern =r"\+\d{3}\s\d{2}\s\d{2}\s\d{2}\s\d{2}"# Pattern to match phone numbers
    phone_number = re.search(phone_pattern, text)
    if phone_number:
        return phone_number.group(0)
    else:
        return None

def find_github_link(text):
    # Define a regular expression pattern to match GitHub URLs
    # Regular expression pattern to match GitHub links
    github_pattern = r"https?://(?:www\.)?github\.com/\w+"

    # Search for GitHub links in CV text
    github_links = re.findall(github_pattern, text)
    return github_links

# Define a function to extract name, email, skills and experience from the resume
def extract_information(file):
    data = ResumeParser(file).get_extracted_data()
    name = data.get('name')
    email = data.get('email')
    degree = ', '.join(data.get('degree', []))
    skills = ', '.join(data.get('skills', []))
    # designation = ', '.join(list(data.get('designation', [])))

    experience = ', '.join(data.get('experience', []))
        # '\n\n'.join([f"{job['title']} at {job['company']} ({job['date_range']})\n{job['description']}" for job in data.get('experience', [])])
    return name, email, degree ,skills, experience


# Define a function to highlight entities in the text
def highlight_entities(text, entities):
    matcher = Matcher(nlp.vocab)
    for entity in entities:
        matcher.add(entity['label'], None, [{'LOWER': ent.lower()} for ent in entity['text'].split()])
    doc = nlp(text)
    matches = matcher(doc)
    spans = []
    for match_id, start, end in matches:
        spans.append(doc[start:end])
    return spacy.displacy.render(spans, style='ent', jupyter=False)

def save_uploadedfile(uploadedfile):

    newpath = r'UploadedFIles\\'
    if not os.path.exists(newpath):
        os.makedirs(newpath)
    with open(os.path.join(newpath, uploadedfile.name), "wb") as f:
        f.write(uploadedfile.getbuffer())
        return newpath + uploadedfile.name

def parser():
    st.title('Resume Parser')

    # Allow the user to upload a resume
    resume_file = st.file_uploader('Upload a resume (PDF or DOCX)', type=['pdf', 'docx'])

    if(st.button('Parse')):
        if resume_file is not None:
            path = save_uploadedfile(resume_file)

            # Read the file contents into a bytes buffer
            cv_text = convert_to_txt(path)
            # print("dddddddddddddddddddddddddddddddddddddd\n\n\n",cv_text)

            phone_number = ""
            github = find_github_link(cv_text)
            phone_number = extract_phone_number(cv_text)
            # print("git link" , github)

            name, email, degree, skills, experience = extract_information(resume_file)
            st.write(f'Name: {name}')
            st.write(f'Email: {email}')
            if github is not None:
                st.write(f"GitHub link: {github}")
            if phone_number is not None:
                st.write(f"Phone Number: {phone_number}")
            st.write(f'Degree\n: \n{degree}')
            st.write(f'Skills: {skills}')
            # if designation is not None:
            #     st.write(f'Designation \n: \n{designation}')
            st.write(f'Experience:\n{experience}')
            entities = [
                {'text': name, 'label': 'PERSON'},
                {'text': email, 'label': 'EMAIL'},
                {'text': phone_number, 'label': 'PHONE NUMBER'},
                {'text': github, 'label': 'GITHUB'},
                {'text': degree, 'label': 'DEGREE'},
                # {'text': designation, 'label': 'DESIGNATION'},
                {'text': skills, 'label': 'SKILLS'},
                {'text': experience, 'label': 'EXPERIENCE'}
            ]
            # st.markdown(highlight_entities(resume_file.read().decode('ISO-8859-1'), entities), unsafe_allow_html=True)


# parser()

