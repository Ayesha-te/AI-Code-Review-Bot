import streamlit as st
import os
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
import tiktoken

# Load OpenAI API key from Streamlit secrets
os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]

# Streamlit setup
st.set_page_config(page_title="AI Code Review Bot", page_icon="🤖")
st.title("🤖 AI Code Review Bot")
st.markdown("Paste your code below and get AI-powered suggestions, improvements, explanations, and a quality score.")

# Code input field
code_input = st.text_area("👨‍💻 Paste your code here:", height=300, placeholder="e.g. def add(a, b): return a + b")

# Function to count tokens
def count_tokens(text: str, model: str = "gpt-3.5-turbo"):
    encoding = tiktoken.encoding_for_model(model)
    return len(encoding.encode(text))

# Review button
if st.button("🧠 Review My Code"):
    if not code_input.strip():
        st.warning("Please paste some code first.")
    else:
        # Shorter prompt to reduce total token usage
        prompt_text = """
You are an expert software engineer reviewing the following code.

Please return the following in this exact order:
1. 🔍 Issues Found
2. ✅ Suggestions for Improvement
3. 📘 Explanations
4. 🧠 Code Quality Score (out of 10 with reason)

Code:
```python
{code_input}





