import os
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import PyPDF2
from io import StringIO
import re
import json
import logging
from docx import Document
from bs4 import BeautifulSoup
import google.generativeai as genai

# Setup
logging.basicConfig(level=logging.INFO)
st.set_page_config(page_title="📊 File Insight Bot", layout="wide")
st.title("📂 File Insight Bot (Multi-format Chat + Charts)")

# Gemini setup
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    st.error("⚠️ Gemini API Key not found in environment variables.")
    st.stop()

try:
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel("gemini-1.5-flash")
except Exception as e:
    st.error(f"⚠️ Gemini configuration error: {e}")
    st.stop()

# File extractor functions
def extract_text_from_pdf(file):
    reader = PyPDF2.PdfReader(file)
    return "\n".join(page.extract_text() or "" for page in reader.pages)

def extract_text_from_docx(file):
    doc = Document(file)
    return "\n".join([para.text for para in doc.paragraphs])

def extract_text_from_html(file):
    soup = BeautifulSoup(file.read(), "html.parser")
    return soup.get_text()

# File uploader
uploaded_file = st.file_uploader("📁 Upload a file", type=["csv", "xlsx", "txt", "pdf", "docx", "json", "html"])

if uploaded_file:
    file_type = uploaded_file.name.split(".")[-1].lower()
    df = None
    raw_text = ""

    try:
        if file_type == "csv":
            df = pd.read_csv(uploaded_file)
            raw_text = df.head(15).to_string(index=False)
            st.subheader("📊 Data Preview")
            st.dataframe(df)

        elif file_type == "xlsx":
            df = pd.read_excel(uploaded_file)
            raw_text = df.head(15).to_string(index=False)
            st.subheader("📊 Data Preview")
            st.dataframe(df)

        elif file_type == "txt":
            raw_text = StringIO(uploaded_file.getvalue().decode("utf-8")).read()
            st.subheader("📝 Text Preview")
            st.text(raw_text[:1000])

        elif file_type == "pdf":
            raw_text = extract_text_from_pdf(uploaded_file)
            st.subheader("📄 PDF Text Preview")
            st.text(raw_text[:1000])

        elif file_type == "docx":
            raw_text = extract_text_from_docx(uploaded_file)
            st.subheader("📄 DOCX Text Preview")
            st.text(raw_text[:1000])

        elif file_type == "json":
            data = json.load(uploaded_file)
            raw_text = json.dumps(data, indent=2)
            st.subheader("🧾 JSON Preview")
            st.json(data)

        elif file_type == "html":
            raw_text = extract_text_from_html(uploaded_file)
            st.subheader("🌐 HTML Text Preview")
            st.text(raw_text[:1000])

        else:
            st.warning("❗ Unsupported file type.")
            st.stop()

    except Exception as e:
        st.error(f"❌ Error processing file: {e}")
        st.stop()

    # Overview from Gemini
    st.divider()
    st.subheader("🧠 Gemini's Overview")
    with st.spinner("Generating summary..."):
        overview_prompt = f"""You are a business analyst. Give a high-level overview of the following content.
- Summarize key points or data columns.
- If it looks like structured data, mention patterns and numeric summaries.
- Otherwise, summarize the topic and structure.
        
Content:
{raw_text[:3000]}
"""
        response = model.generate_content(overview_prompt)
        st.markdown(response.text)

    # Chatbot input
    st.divider()
    st.subheader("💬 Ask Anything About the File (Charts Included!)")
    user_prompt = st.text_input("Ask a question or request a chart:")

    if user_prompt:
        # Prepare chatbot prompt
        base_prompt = f"""
You are a data and content analyst. The user uploaded the following content:

{raw_text[:3000]}

Their question is: "{user_prompt}"

Reply in 2 parts:
1. Brief explanation in natural language.
2. A Python code block (in triple backticks) using matplotlib and pandas to generate a chart, if applicable.

Return only ONE code block.
"""
        with st.spinner("Thinking..."):
            try:
                response = model.generate_content(base_prompt)
                output = response.text
                st.markdown(output)

                # Extract and run code
                match = re.search(r"```(?:python)?\s+(.*?)```", output, re.DOTALL)
                if match:
                    code = match.group(1)
                    with st.expander("🧪 Generated Code"):
                        st.code(code, language="python")
                    try:
                        local_vars = {"df": df if df is not None else pd.DataFrame(), "st": st, "plt": plt, "pd": pd}
                        exec(code, local_vars)
                        st.pyplot()
                    except Exception as e:
                        st.error(f"⚠️ Error executing chart code: {e}")
            except Exception as e:
                st.error("🚫 Gemini failed to respond. Try again.")
