import streamlit as st
import base64
import tempfile
import numpy
import cv2
from pdf2image.pdf2image import convert_from_path
import re
import pandas as pd
import pytesseract
import spacy
nlp = spacy.load('en_core_web_sm')
from spacy.matcher import Matcher
matcher = Matcher(nlp.vocab)

def ParsingCv():
    st.title("PDF Resume Parser")

    # Upload PDF file
    uploaded_file = st.file_uploader("Choose a CV (PDF only)", type="pdf")
    if uploaded_file is not None:
        if st.button('Show Cv'):
            st.write('Showing candidate''s cv...')
            show_pdf(uploaded_file)

        if st.button('Parser'):
            with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
                tmp_file.write(uploaded_file.read())
                pdf_path = tmp_file.name
                # Convert PDF to image
                images = convert_from_path(pdf_path)
                cv2_images = [cv2.cvtColor(numpy.array(image), cv2.COLOR_RGB2BGR) for image in images]
                # Parse content
                text = extract_text(cv2_images)
                parsed_content = parse_content(text)

                st.subheader("Parsed Content")
                df = pd.DataFrame(parsed_content.items(), columns=["Category", "Content"])
                st.dataframe(df)
                # Add button to save DataFrame to JSON file
                if st.button("SAVE"):
                    with open('Data/data.json', 'a') as f:
                        df.to_json(f, orient='records')
                        st.success("Data saved to JSON file")
        else:
            st.error('')
    footer()

def extract_text(cv2_images):
    import os
    os.environ['PATH'] += ':/usr/bin:/usr/local/bin:/usr/local/poppler/bin'

    # OCR the images to extract text
    text = ""
    for image in cv2_images:
        text += pytesseract.image_to_string(image)
    return text


def parse_content(text):

    # Extract name
    name = extract_name(text)
    parsed_content = {"Name": name}

    # Extract email
    email = get_email_addresses(text)
    parsed_content["Email"] = email

    # Extract github
    github = extract_github_links(text)
    parsed_content["GitHub"] = github

    # Extract LinkedIn
    linkedIn= extract_linkedin_links(text)
    parsed_content["LinkedIn"] = linkedIn

    # Extract phone number
    phone_number = extract_phone_numbers(text)
    if len(phone_number) <= 12:
        parsed_content["Phone Number"] = phone_number

    text= modif(text)

    Keywords = ["education",
                "summary",
                "accomplishments",
                "executive profile",
                "professional profile",
                "personal profile",
                "work background",
                "academic profile",
                "other activities",
                "qualifications",
                "Experience",
                "interests",
                "skills",
                "achievements",
                "publications",
                "publication",
                "certifications",
                "workshops",
                "projects",
                "internships",
                "trainings",
                "hobbies",
                "overview",
                "objective",
                "position of responsibility",
                "jobs"
                ]

    # Extract content by category
    content = {}
    indices = []
    keys = []
    for key in Keywords:
        try:
            content[key] = text[text.index(key) + len(key):]
            indices.append(text.index(key))
            keys.append(key)
        except:
            pass
    # Sorting the indices
    zipped_lists = zip(indices, keys)
    sorted_pairs = sorted(zipped_lists)
    tuples = zip(*sorted_pairs)
    print(tuples)
    indices, keys = [list(tuple) for tuple in tuples]

    # Keeping the required content and removing the redundant part
    content = []
    for idx in range(len(indices)):
        if idx != len(indices) - 1:
            content.append(text[indices[idx]: indices[idx + 1]])
        else:
            content.append(text[indices[idx]:])

    for i in range(len(indices)):
        parsed_content[keys[i]] = content[i]

    return parsed_content


def extract_name(text):
    nlp_text = nlp(text)
    # First name and Last name are always Proper Nouns
    pattern = [{'POS': 'PROPN'}, {'POS': 'PROPN'}]
    matcher.add('NAME', [pattern], on_match=None)
    matches = matcher(nlp_text)
    for match_id, start, end in matches:
        span = nlp_text[start:end]
        return span.text


def get_email_addresses(string):
    r = re.compile(r'[\w\.-]+@[\w\.-]+')
    return r.findall(string)

def extract_github_links(text):
    # Regular expression to match GitHub links
    github_regex = r'github\.com/[^\s/]+/[^\s/]+'
    # Find all matches of the regex in the text
    matches = re.findall(github_regex, text)
    # Return the matches
    return matches


def extract_linkedin_links(text):
    # Regular expression to match LinkedIn profile links
    linkedin_regex = r'linkedin\.com/[^\s/]+'
    # Find all matches of the regex in the text
    matches = re.findall(linkedin_regex, text)
    # Return the matches
    return matches


def extract_phone_numbers(text):
    # Regular expression to match phone numbers
    phone_regex = r'\d{2}\s?\d{2}\s?\d{2}\s?\d{2}\s?(\d{3}\s?\d{3}|\d{4}\s?\d{3})'
    # Find all matches of the regex in the text
    matches = re.findall(phone_regex, text)
    # Return the matches
    return matches

    # r = re.compile(r'(\d{3}[-\.\s]??\d{4}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4})')
    # return r.findall(string)

def modif(text):
    text = text.replace("\n", " ")
    text = text.replace("[^a-zA-Z0-9]", " ");
    re.sub('\W+', '', text)
    text = text.lower()
    return text


def show_pdf(file):
    # Read the contents of the file
    pdf_bytes = file.read()

    # Encode the PDF content as a base64 string
    base64_pdf = base64.b64encode(pdf_bytes).decode('utf-8')

    # Generate the HTML code to display the PDF
    pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="700" height="1000" type="application/pdf"></iframe>'

    # Display the PDF in the app
    st.markdown(pdf_display, unsafe_allow_html=True)

def footer():
    # Add page footer
    footer = """
        <style>
            .footer {
                font-size: 0.7em;
                text-align: center;
                padding: 1em;
            }
        </style>
        <div class="footer">
            <p>Made by Yassine GUENIDI & Chaima BEN ABDALLAH</p>
        </div>
    """
    st.write("___")
    st.markdown(footer, unsafe_allow_html=True)

# ParsingCv()