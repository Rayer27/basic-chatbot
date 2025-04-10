# 📊 Business Analytics Chatbot (Free & Open Source)

A Streamlit-based chatbot that analyzes your business data (CSV or Excel) using a **free LLM hosted on Hugging Face** — no OpenAI API or paid cloud required!

It supports:
- ✅ Conversational Q&A about your data
- 📈 Automatic **chart generation** (bar, line, pie, etc.)
- 💡 Insightful summaries powered by **Mistral 7B**
- 🚀 Deployable on **Streamlit Cloud** for free

---

## 🔧 How It Works

1. Upload your spreadsheet
2. Ask a question like:
   - *"Show total sales by product"*
   - *"Which region performs best?"*
   - *"Give me a pie chart of revenue by country"*
3. The LLM responds with:
   - 💬 Text answer
   - 🧠 Python code (auto-executed) to generate a chart

---

## 🧠 Powered By

- 🤖 [Mistral-7B-Instruct](https://huggingface.co/mistralai/Mistral-7B-Instruct-v0.1) via Hugging Face API
- 🎈 [Streamlit](https://streamlit.io/)
- 📦 pandas, plotly, requests

---

## 🚀 Get Started

### 1. Clone This Repo

```bash
git clone https://github.com/your-username/business-analytics-chatbot.git
cd business-analytics-chatbot


