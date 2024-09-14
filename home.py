import streamlit as st

from Parser import parser
from ParsingCv import ParsingCv
from classifier import classifier
from principale import principale
from similarity import similarity


def acceuil():

    st.set_page_config(page_title="Cv Manipulation", page_icon="chart_with_upwards_trend", layout="wide")
    acceuil = ["Page Acceuil", "Classifier", "Parser cv","Similarity"]
    choice = st.sidebar.selectbox("Menu", acceuil)

    if choice == "Page Acceuil":
        print("acceuil")
        principale()
    elif choice == "Classifier":
        classifier()
    elif choice == "Parser cv":
        ParsingCv()
    elif choice == "Similarity":
        similarity()



acceuil()