from PIL import Image
import streamlit as st

def principale():
    st.title("Welcome Back")
    st.subheader("This application is designed to help with three tasks related to job applications:")
    espace()
    firstPart()
    espace()
    secondPart()
    espace()
    thirdPart()
    espace()
    about()
    espace()
    display_form()
    espace()
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

def espace():
    st.write("\n")
    st.write("\n")
    st.write("\n")
    st.write("\n")
    st.write("\n")
    st.write("\n")
    st.write("------------------------------------------------------------")

def about():
    # Add an "About" section to provide more information about the application
    st.header("About")
    st.write(
        "This application was developed to help streamline the job application process for both candidates and recruiters. By using advanced NLP and machine learning techniques, it can help identify the best candidates for a given position, saving recruiters time and effort. The application is designed to be user-friendly and easy to use, even for those with limited technical expertise.")

    st.write(
        "The developers of this application are committed to continuous improvement and welcome feedback from users. If you have any suggestions or ideas for how to improve the application, please don't hesitate to contact us.")

    # Add a call to action to encourage users to get started
    st.write("To get started, simply upload a resume and select which part of the application you'd like to use.")

def display_contact_section():
    st.header("Contact Us")
    st.write("If you have any questions or feedback about this application, please feel free to contact us at:")
    st.write("- Email: yassinegunidi99@email.com")
    st.write("- Phone: +216 22 344 203")

def display_form():

    # ---- CONTACT ----
    with st.container():
        # st.write("---")
        contact_form = """
                <style>
                    input[type=text], input[type=email], textarea {
                        width: 100%;
                        padding: 12px;
                        border: 1px solid #ccc;
                        border-radius: 4px;
                        resize: vertical;
                    }
                    label {
                        display: block;
                        font-weight: bold;
                    }
                    button[type=submit] {
                        background-color: #4CAF50;
                        color: white;
                        padding: 12px 20px;
                        border: none;
                        border-radius: 4px;
                        cursor: pointer;
                    }
                    button[type=submit]:hover {
                        background-color: #45a049;
                    }
                    .container {
                        border-radius: 5px;
                        background-color: #f2f2f2;
                        padding: 20px;
                    }
                </style>
                <div class="container">
                    <form action="https://formsubmit.co/yassineguenidi99@gmail.com" 
                          method="POST" autocomplete="off">
                        <input type="hidden" name="_captcha" value="false">
                        <label for="name">Nom:</label>
                        <input type="text" name="name" placeholder="Your name" required>
                        <label for="email">Email:</label>
                        <input type="email" name="email" placeholder="Your email" required>
                        <label for="message">Message:</label>
                        <textarea name="message" placeholder="Your message" required></textarea>
                        <button type="submit">Submit</button>
                    </form>
                </div>
                """
        left_column,right_column = st.columns((3.5, 0.5))
        with left_column:
            st.header("Do you have any question ?")
            st.markdown(contact_form, unsafe_allow_html=True)

def firstPart():
    with st.container():
        image_column, text_column = st.columns((1, 2))
        with image_column:
            image = Image.open(r'images\1584386507363.jpeg')
            centered_container = st.container()
            with centered_container:
                st.write("##")
                st.image(image, width=300, use_column_width=True)

        with text_column:
            st.subheader("Resume Parser")
            st.write("1. Resume Parser: Extracting important information from a candidate's resume")
            st.write(
                """
                 The Resume Parser uses natural language processing (NLP) techniques to extract key information 
                 from a candidate's resume, 
                 such as their name, 
                 contact information, 
                 work experience, 
                 and education.
                 """
            )

def secondPart():
    with st.container():
        image_column, text_column = st.columns((1, 2))

        with image_column:
            image = Image.open(r'images\36762097_M.jpg')
            centered_container = st.container()
            with centered_container:
                st.write("##")
                st.image(image, width=300, use_column_width=True)

        with text_column:
            st.subheader("Resume Classification")
            st.write("1. Resume Classification:: Categorizing resumes into different job roles or industries")
            st.write(
                """
                The Resume Classification module uses machine learning algorithms 
                to categorize resumes based on the job role or industry. 
                This can help recruiters quickly sort through large numbers of resumes 
                and identify the most relevant candidates for a given position.
                 """
            )

def thirdPart():
    with st.container():
        image_column, text_column = st.columns((1, 2))
        with image_column:
            image = Image.open(r'images\choice.jpg')
            centered_container = st.container()
            with centered_container:
                st.write("")
                st.image(image, width=300, use_column_width=True)

        with text_column:
            st.subheader("Similarity Analysis")
            st.write("3. Similarity Analysis: Comparing job requirements with a candidate's resume to determine the best fit")
            st.write(
                """
                 The Similarity Analysis module compares job requirements with a candidate's resume 
                 to determine how well they match. 
                 This can help recruiters and hiring managers quickly identify candidates who are the best fit 
                 for a particular position.")
                 """
            )

# principale()