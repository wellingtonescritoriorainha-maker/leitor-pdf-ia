import streamlit as st
import google.generativeai as genai
from PyPDF2 import PdfReader
import io

# 1. Configuração da Página (Deve ser a primeira linha de comando Streamlit)
st.set_page_config(page_title="IA Analista de PDFs", layout="wide")

# 2. Título principal
st.title("📂 Analisador de 100+ PDFs")

# 3. Barra Lateral para configurações
with st.sidebar:
    st.header("Configuração")
    api_key = st.text_input("Google API Key:", type="password")
    st.info("Obtenha sua chave em: aistudio.google.com")
    st.markdown("---")
    st.write("Dica: Use o modelo 'Flash' para rapidez ou 'Pro' para análises profundas.")
    model_name = st.selectbox("Escolha o modelo:", ["gemini-1.5-flash", "gemini-1.5-pro"])

# 4. Área de Upload (Fora da barra lateral para destaque)
st.subheader("Passo 1: Suba seus documentos")
files = st.file_uploader("Arraste seus PDFs aqui (até 100+ arquivos)", type="pdf", accept_multiple_files=True)

# 5. Processamento e Chat
if files:
    if not api_key:
        st.warning("⚠️ Por favor, insira sua Google API Key na barra lateral esquerda.")
    else:
        try:
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel(model_name)
            
            with st.status("Lendo PDFs... aguarde", expanded=True) as status:
                full_text = ""
                for file in files:
                    st.write(f"Lendo: {file.name}")
                    reader = PdfReader(io.BytesIO(file.read()))
                    for page in reader.pages:
                        text = page.extract_text()
                        if text:
                            full_text += text + "\n"
                status.update(label="Leitura concluída!", state="complete", expanded=False)

            st.success(f"Pronto! {len(files)} arquivos carregados no contexto da IA.")
            
            st.subheader("Passo 2: Faça sua pergunta")
            user_question = st.text_area("O que você deseja saber sobre esses documentos?", 
                                        placeholder="Ex: Liste os valores totais de todos os contratos.")

            if st.button("Analisar agora"):
                if user_question:
                    with st.spinner("A IA está analisando o conteúdo..."):
                        # O Gemini 1.5 aguenta centenas de PDFs direto no prompt
                        prompt = f"Contexto dos PDFs:\n{full_text}\n\nPergunta do usuário: {user_question}"
                        response = model.generate_content(prompt)
                        
                        st.markdown("### 🤖 Resposta da IA:")
                        st.write(response.text)
                else:
                    st.error("Digite uma pergunta para a IA responder.")
                    
        except Exception as e:
            st.error(f"Ocorreu um erro técnico: {e}")
else:
    st.info("Aguardando o upload dos arquivos para começar...")
