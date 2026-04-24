import streamlit as st
import google.generativeai as genai
from PyPDF2 import PdfReader
import io

st.set_page_config(page_title="IA Analista de PDFs", layout="wide")
st.title("📂 Analisador de 100+ PDFs")

with st.sidebar:
    st.header("Configuração")
    api_key = st.text_input("Google API Key:", type="password")
    st.info("Obtenha sua chave em: aistudio.google.com")
    st.markdown("---")
    # Aqui está a correção dos nomes dos modelos
    model_choice = st.selectbox("Escolha o modelo:", ["models/gemini-1.5-flash", "models/gemini-1.5-pro"])

st.subheader("Passo 1: Suba seus documentos")
files = st.file_uploader("Arraste seus PDFs aqui", type="pdf", accept_multiple_files=True)

if files:
    if not api_key:
        st.warning("⚠️ Insira sua API Key na barra lateral.")
    else:
        try:
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel(model_choice)
            
            with st.status("Lendo arquivos...", expanded=False) as status:
                full_text = ""
                for file in files:
                    reader = PdfReader(io.BytesIO(file.read()))
                    for page in reader.pages:
                        full_text += (page.extract_text() or "") + "\n"
                status.update(label="Leitura concluída!", state="complete")

            st.success(f"{len(files)} PDFs prontos para análise.")
            user_question = st.text_area("O que deseja saber?")

            if st.button("Analisar agora"):
                with st.spinner("Analisando..."):
                    response = model.generate_content(f"Documentos:\n{full_text}\n\nPergunta: {user_question}")
                    st.markdown("### Resposta:")
                    st.write(response.text)
        except Exception as e:
            st.error(f"Erro técnico: {e}")
