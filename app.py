import streamlit as st
import os
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

# Load API key from Streamlit secrets
os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]

# Streamlit UI setup
st.set_page_config(page_title="AI Code Review Bot", page_icon="🤖")
st.title("🤖 AI Code Review Bot")
st.markdown("Paste your code below and get **AI-powered** review with improvements, explanations, and a quality score!")

# Input box
code_input = st.text_area(
    "🧾 Enter your Python code:",
    height=300,
    placeholder="e.g. def add(a, b): return a + b"
)

# Truncate code input if it's too long
max_code_length = 800  # adjust to fit within token budget
if len(code_input) > max_code_length:
    code_input = code_input[:max_code_length]
    st.warning("⚠️ Your code was too long and has been truncated to fit token limits.")

# Submit button
if st.button("🚀 Review My Code"):
    if not code_input.strip():
        st.error("Please enter some code first.")
    else:
        with st.spinner("Analyzing code with AI..."):
            # Prompt for LangChain
            prompt_text = """
You are a senior Python developer. Review the following code and return a detailed response in the exact sections below:

### 🔍 Issues Found:
- List any bugs, bad practices, or concerns.
- Explain why each issue matters.

### ✅ Suggestions for Improvement:
- Suggest fixes or enhancements.
- Mention good practices if found.

### 📘 Explanations:
- Provide detailed reasoning for your review.

### 🧠 Code Quality Score (out of 10):
- Score based on readability, efficiency, and structure.
- Include a short justification.

Only respond in this format. Code:
```python
{code_input}
