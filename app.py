import streamlit as st
import pandas as pd
import requests
import plotly.express as px
import re
import os

HF_TOKEN = os.environ.get("HF_TOKEN")
headers = {"Authorization": f"Bearer {HF_TOKEN}"}
model = "mistralai/Mistral-7B-Instruct-v0.1"
api_url = f"https://api-inference.huggingface.co/models/{model}"

st.set_page_config(page_title="📊 Business Analytics Chatbot", layout="wide")
st.title("📈 Business Analytics Chatbot (Free LLM + Charts)")

uploaded_file = st.file_uploader("Upload CSV or Excel file", type=["csv", "xlsx"])

if uploaded_file:
    file_type = uploaded_file.name.split(".")[-1]
    if file_type == "csv":
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    st.subheader("📄 Preview of Your Data")
    st.dataframe(df.head())

    st.divider()
    prompt = st.text_input("💬 Ask a question or request a chart (e.g. 'Show sales by region'): ")

    if prompt:
        sample_data = df.head(15).to_string(index=False)
        full_prompt = f"""You are a data analyst. Analyze the following data:\n\n{sample_data}\n\nQuestion: {prompt}

Answer the question in two parts:
1. A short natural language explanation.
2. A Python code block (using Plotly Express and the 'df' variable) to generate a chart.

Return only one code block inside triple backticks."""
        
        with st.spinner("Thinking..."):
            response = requests.post(api_url, headers=headers, json={"inputs": full_prompt})
        
        try:
            result = response.json()
            output = result[0]["generated_text"]
            st.markdown(output)

            # Extract and run the code
            match = re.search(r"```(?:python)?\s+(.*?)```", output, re.DOTALL)
            if match:
                code = match.group(1)
                with st.expander("🔍 Generated Code"):
                    st.code(code, language="python")
                try:
                    exec(code, {"df": df, "px": px, "st": st, "pd": pd})
                except Exception as e:
                    st.error(f"⚠️ Error running chart code: {e}")
        except Exception as e:
            st.error("🚫 LLM response failed. Try again or check your HF token.")
