# import io
# from PIL import Image
# import streamlit as st
# import PyPDF2
# import nltk
# import spacy
# import spacy
# nlp = spacy.load('en_core_web_sm')
# from spacy.matcher import Matcher
# matcher = Matcher(nlp.vocab)
#
# nlp = spacy.load('en_core_web_sm')
#
# def read_pdf(file):
#     pdf_reader = PyPDF2.PdfReader(io.BytesIO(file.read()))
#     text = ''
#     for page in range(len(pdf_reader.pages)):
#         text +=  pdf_reader.pages[page].extract_text()
#     return text
#
# def preprocess(text):
#     doc = nlp(text)
#     return [token.lemma_ for token in doc if not token.is_stop and not token.is_punct and not token.is_space]
#
# def calculate_similarity(text1, text2):
#     doc1 = nlp(text1)
#     doc2 = nlp(text2)
#     return doc1.similarity(doc2)
#
# def rank_cvs(cvs, job_description):
#     job_description_preprocessed = preprocess(job_description)
#     ranked_cvs = []
#     for cv in cvs:
#         text = read_pdf(cv)
#         text_preprocessed = preprocess(text)
#         similarity = calculate_similarity(' '.join(text_preprocessed), ' '.join(job_description_preprocessed))
#         ranked_cvs.append((cv.name, similarity))
#     ranked_cvs = sorted(ranked_cvs, key=lambda x: x[1], reverse=True)
#     return ranked_cvs
import base64
import io
import streamlit as st
import PyPDF2
import spacy

nlp = spacy.load('en_core_web_sm')
from spacy.matcher import Matcher

matcher = Matcher(nlp.vocab)

nlp = spacy.load('en_core_web_sm')


def read_pdf(file):
    pdf_reader = PyPDF2.PdfReader(io.BytesIO(file.read()))
    text = ''
    for page in range(len(pdf_reader.pages)):
        text += pdf_reader.pages[page].extract_text()
    return text


def preprocess(text):
    doc = nlp(text)
    return [token.lemma_ for token in doc if not token.is_stop and not token.is_punct and not token.is_space]


def calculate_similarity(text1, text2):
    doc1 = nlp(text1)
    doc2 = nlp(text2)
    return doc1.similarity(doc2)


def rank_cvs(cvs, job_description):
    job_description_preprocessed = preprocess(job_description)
    ranked_cvs = []
    for cv in cvs:
        text = read_pdf(cv)
        text_preprocessed = preprocess(text)
        similarity = calculate_similarity(' '.join(text_preprocessed), ' '.join(job_description_preprocessed))
        ranked_cvs.append((cv.name, similarity))
    ranked_cvs = sorted(ranked_cvs, key=lambda x: x[1], reverse=True)
    return ranked_cvs


def similarity():
    st.title('CV Ranker')

    # Upload job description and CVs
    job_description_file = st.file_uploader('Upload the job description (PDF only)', type='pdf')
    cv_files = st.file_uploader('Upload one or more CVs (PDF only)', type='pdf', accept_multiple_files=True)

    # Set number of CVs to show
    num_cvs_to_show = st.number_input('Enter the number of CVs to show', min_value=1, value=10, step=1)

    # Display ranking button
    left_column, middle, right_column = st.columns((10.5, 10,2.5))
    with middle:
        if (st.button('Rank')):
            if job_description_file is not None and cv_files is not None:
                job_description_text = read_pdf(job_description_file)
                st.write('Ranking CVs...')

                # Rank CVs and display results
                ranked_cvs = rank_cvs(cv_files, job_description_text)[:num_cvs_to_show]
                # cv_results = st.empty()
                for i, (cv_name, similarity) in enumerate(ranked_cvs):
                    st.write(f'{i + 1}. {cv_name} (similarity score: {similarity:.2f})')
            else:
                st.error('Please upload the job description and at least one CV.')

    footer()

def similarity2():
    st.title('CV Ranker')
    job_description_file = st.file_uploader('Upload the job description (PDF only)', type='pdf')
    cv_files = st.file_uploader('Upload one or more CVs (PDF only)', type='pdf', accept_multiple_files=True)

    num_cvs_to_show = st.number_input('Enter the number of CVs to show', min_value=1, value=10, step=1)

    if (st.button('Rank')):
        if job_description_file is not None and cv_files is not None:
            job_description_text = read_pdf(job_description_file)
            st.write('Ranking CVs...')
            ranked_cvs = rank_cvs(cv_files, job_description_text)[:num_cvs_to_show]
            for i, (cv_name, similarity) in enumerate(ranked_cvs):
                st.write(f'{i + 1}. {cv_name} (similarity score: {similarity:.2f})')
                st.write("buuuut")
                if st.button(f"Show {cv_name}"):
                    show_pdf(cv_name)
        else:
            st.error('Please upload the job description and at least one CV.')


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

# similarity()