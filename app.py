import os
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import re
import google.generativeai as genai

# Get Gemini API key from environment variable
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
if GEMINI_API_KEY is None:
    st.error("⚠️ Gemini API Key not found in environment variables.")
else:
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel("gemini-1.5-flash")

    st.set_page_config(page_title="📊 Business Analytics Chatbot", layout="wide")
    st.title("📈 Business Analytics Chatbot (Gemini + Charts)")

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

Answer in two parts:
1. A brief explanation in natural language.
2. A Python code block (using matplotlib and the 'df' variable) to generate a chart.

Return only one code block inside triple backticks."""

            with st.spinner("Thinking..."):
                try:
                    response = model.generate_content(full_prompt)
                    output = response.text
                    st.markdown(output)

                    # Extract and run code block
                    match = re.search(r"```(?:python)?\s+(.*?)```", output, re.DOTALL)
                    if match:
                        code = match.group(1)
                        with st.expander("🔍 Generated Code"):
                            st.code(code, language="python")
                        try:
                            # Execute code to generate graph using matplotlib
                            exec(code, {"df": df, "st": st, "plt": plt, "pd": pd})

                            # Show the generated plot
                            st.pyplot()
                        except Exception as e:
                            st.error(f"⚠️ Error running chart code: {e}")
                except Exception as e:
                    st.error("🚫 Gemini response failed. Check your API key or try again.")
