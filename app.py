import streamlit as st
from googletrans import Translator
import json
import PyPDF2
from docx import Document
import pandas as pd
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import io

# Configuración de Alto Contraste
st.set_page_config(page_title="Traductor Pro", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #FFFFFF; }
    h1, h2, h3, p, span, label, .stMarkdown { 
        color: #000000 !important; 
        font-weight: 900 !important; 
    }
    .stButton>button {
        background-color: #28a745 !important;
        color: white !important;
        font-weight: bold !important;
        width: 100%;
        height: 3.5em;
        border: 2px solid #000;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🚀 TRADUCTOR UNIVERSAL: MODO PRÁCTICO")
st.write("**Traducción instantánea a Español para PDF, Word, Excel, JSON y TXT.**")

translator = Translator()

def crear_pdf(texto):
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter
    text_obj = c.beginText(40, height - 40)
    text_obj.setFont("Helvetica", 10)
    
    # Simple control de líneas para el PDF
    for line in texto.split('\n'):
        text_obj.textLine(line[:100]) # Cortar líneas muy largas
    
    c.drawText(text_obj)
    c.showPage()
    c.save()
    buffer.seek(0)
    return buffer

archivo = st.file_uploader("📂 Sube tu documento aquí", type=['pdf', 'json', 'txt', 'docx', 'xlsx'])

if archivo:
    tipo = archivo.name.split('.')[-1].lower()
    texto_puro = ""

    try:
        with st.spinner("**Traduciendo... por favor ten paciencia.**"):
            if tipo == 'txt':
                texto_puro = archivo.read().decode('utf-8')
            elif tipo == 'json':
                texto_puro = json.dumps(json.load(archivo), indent=2)
            elif tipo == 'pdf':
                reader = PyPDF2.PdfReader(archivo)
                texto_puro = "\n".join([p.extract_text() for p in reader.pages])
            elif tipo == 'docx':
                doc = Document(archivo)
                texto_puro = "\n".join([para.text for para in doc.paragraphs])
            elif tipo == 'xlsx':
                df = pd.read_excel(archivo)
                texto_puro = df.to_string()

            if texto_puro:
                # Traducción (limitada a bloques para evitar errores)
                traduccion = translator.translate(texto_puro[:3000], dest='es').text
                
                st.subheader("**📝 RESULTADO EN ESPAÑOL:**")
                st.text_area("", traduccion, height=250)

                col1, col2 = st.columns(2)
                with col1:
                    st.download_button("📥 DESCARGAR EN TXT", traduccion, f"traducido_{archivo.name}.txt")
                with col2:
                    pdf_file = crear_pdf(traduccion)
                    st.download_button("📥 DESCARGAR EN PDF", pdf_file, f"traducido_{archivo.name}.pdf", "application/pdf")
    except Exception as e:
        st.error(f"**Vaya, hubo un problema: {e}**")
else:
    st.info("**Elige un archivo de tu dispositivo para comenzar.**")