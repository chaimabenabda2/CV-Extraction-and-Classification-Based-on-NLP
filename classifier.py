import base64
import io
from sklearn.feature_extraction.text import TfidfVectorizer
import re
import pickle
import pandas as pd
import streamlit as st
import PyPDF2
import nltk
from sklearn.preprocessing import LabelEncoder
nltk.download("stopwords")
from nltk.stem import WordNetLemmatizer
nltk.download('punkt')
nltk.download('wordnet')


# Define a function to read the text from a PDF file
def read_pdf(file):
    pdf_reader = PyPDF2.PdfReader(io.BytesIO(file.read()))
    text = ''
    for page in range(len(pdf_reader.pages)):
        text +=  pdf_reader.pages[page].extract_text()
    return text

def preprocess(txt):
    # convert all characters in the string to lower case
    txt = txt.lower()
    import string
    txt = txt.replace('city', '')
    txt = txt.replace('state', '')
    txt = txt.replace('company', '')
    # removing punctuation
    punct = string.punctuation
    for p in punct:
        txt = txt.replace(p, '')
    # remove non-english characters, punctuation and numbers
    txt = re.sub('[^a-zA-Z]', ' ', txt)
    txt = re.sub('http\S+\s*', ' ', txt)  # remove URLs
    txt = re.sub('RT|cc', ' ', txt)  # remove RT and cc
    txt = re.sub('#\S+', '', txt)  # remove hashtags
    txt = re.sub('@\S+', '  ', txt)  # remove mentions
    txt = re.sub('\s+', ' ', txt)  # remove extra whitespace
    # tokenize word
    txt = nltk.tokenize.word_tokenize(txt)
    from nltk.stem.porter import PorterStemmer
    # stemmer = PorterStemmer()
    # txt=[stemmer.stem(word) for word in txt]
    lemmatizer = WordNetLemmatizer()
    txt = [lemmatizer.lemmatize(token) for token in txt]
    # remove stop words
    txt = [w for w in txt if not w in nltk.corpus.stopwords.words('english')]
    return ' '.join(txt)


def preprocess2(txt):
    # convert all characters in the string to lower case
    txt = txt.lower()
    # remove non-english characters, punctuation and numbers
    txt = re.sub('[^a-zA-Z]', ' ', txt)
    txt = re.sub('http\S+\s*', ' ', txt)  # remove URLs
    txt = re.sub('RT|cc', ' ', txt)  # remove RT and cc
    txt = re.sub('#\S+', '', txt)  # remove hashtags
    txt = re.sub('@\S+', '  ', txt)  # remove mentions
    txt = re.sub('\s+', ' ', txt)  # remove extra whitespace
    # tokenize word
    txt = nltk.tokenize.word_tokenize(txt)
    # remove stop words
    txt = [w for w in txt if not w in nltk.corpus.stopwords.words('english')]

    return ' '.join(txt)

# Define a function to classify the CV
def classify_cv(text):
    # text2 = preprocess2(text)
    text2 = [text]

    # Create a TF-IDF model
    tfidf_model = TfidfVectorizer(max_features=100)

    path_file = 'Data/my_dataNew.csv'
    df = pd.read_csv(path_file)
    # category = df.iloc[:, -1]
    category = df.Category

    label_encoder = LabelEncoder()
    label_encoder.fit_transform(category)

    # Load the saved model from the file
    with open('Models/modelNew.pkl', 'rb') as f:
        model = pickle.load(f)

    # Apply the TF-IDF model to the preprocessed text data
    text = tfidf_model.fit_transform(text2).toarray()
    pred = model.predict(text)

    # use inverse_transform to decode the predicted label
    y_pred_label = label_encoder.inverse_transform(pred)
    print("this resume is classified to " , y_pred_label)
    st.write(f'The CV is classified as: {y_pred_label}')
    return pred


def show_pdf(file):
    # Read the contents of the file
    pdf_bytes = file.read()

    # Encode the PDF content as a base64 string
    base64_pdf = base64.b64encode(pdf_bytes).decode('utf-8')

    # Generate the HTML code to display the PDF
    pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="700" height="1000" type="application/pdf"></iframe>'

    # Display the PDF in the app
    st.markdown(pdf_display, unsafe_allow_html=True)


def classifier():
    # Set up the Streamlit app
    st.title('CV Classifier')
    # Allow the user to upload a file
    cv_file = st.file_uploader('Upload your CV (PDF only)', type='pdf')
    # Once the user has uploaded a file and clicks the "Classify" button, read the text and classify it
    if cv_file is not None:

        if st.button('Classify'):
            text = read_pdf(cv_file)
            st.write('Classifying...')
            classify_cv(text)
        else:
            st.write('')

        if st.button('Show Cv'):
            st.write('Showing candidate''s cv...')
            show_pdf(cv_file)
        else:
            st.write('')
    footer()

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

# classifier()