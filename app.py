import streamlit as st
import google.generativeai as genai
from PyPDF2 import PdfReader
import io

st.set_page_config(page_title="IA Analista de PDFs", layout="wide")
st.title("📂 Analisador de 100+ PDFs")
