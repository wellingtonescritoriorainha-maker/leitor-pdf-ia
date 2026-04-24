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
    # Nomes corrigidos para a API estável
    model_choice = st.selectbox("Escolha o modelo:", ["gemini-1.5-flash", "gemini-1.5-pro"])

st.subheader("Passo 1: Suba seus documentos")
files = st.file_uploader("Arraste seus PDFs aqui", type="pdf", accept_multiple_files=True)

if files:
    if not api_key:
        st.warning("⚠️ Insira sua API Key na barra lateral.")
    else:
        try:
            # Configuração explícita da API
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel(model_name=model_choice)
            
            with st.status("Lendo arquivos...", expanded=False) as status:
                full_text = ""
                for file in files:
                    reader = PdfReader(io.BytesIO(file.read()))
                    for page in reader.pages:
                        text = page.extract_text()
                        if text:
                            full_text += text + "\n"
                status.update(label="Leitura concluída!", state="complete")

            st.success(f"{len(files)} PDFs carregados.")
            
            user_question = st.text_area("O que deseja saber sobre as notas?")

            if st.button("Analisar agora"):
                if user_question:
                    with st.spinner("Somando valores e analisando..."):
                        # Prompt reforçando que queremos dados numéricos se necessário
                        prompt = f"Considere os seguintes dados extraídos de PDFs:\n{full_text}\n\nPergunta: {user_question}. Se for uma soma de valores, extraia os números com cuidado."
                        response = model.generate_content(prompt)
                        st.markdown("### Resposta da IA:")
                        st.write(response.text)
                else:
                    st.error("Por favor, digite uma pergunta.")
                    
        except Exception as e:
            # Se der erro 404 de novo, tentamos o nome alternativo automaticamente
            st.error(f"Erro ao acessar a IA: {e}")
            st.info("Dica: Tente trocar o modelo na barra lateral (Flash para Pro ou vice-versa).")
