import streamlit as st
import os
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

# Load OpenAI API key from Streamlit secrets
os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]

# Streamlit setup
st.set_page_config(page_title="AI Code Review Bot", page_icon="🤖")
st.title("🤖 AI Code Review Bot")
st.markdown("Paste your code below and get AI-powered suggestions and improvements.")

# Code input
code_input = st.text_area(
    "👨‍💻 Paste your code here:",
    height=300,
    placeholder="e.g. def add(a, b): return a + b"
)

# Trigger
if st.button("🧠 Review My Code"):
    if not code_input.strip():
        st.warning("Please paste some code first.")
    else:
        # LLM setup
        llm = OpenAI(temperature=0)

        # Safe prompt (defined as a regular string to avoid syntax errors)
        prompt_text = (
            "You are a senior software engineer. Review the following code for:\n\n"
            "1. Bugs or potential issues\n"
            "2. Bad programming practices\n"
            "3. Suggestions for cleaner or more efficient code\n"
            "4. Explanation of any complex logic\n\n"
            "Code:\n"
            "```python\n{code_input}\n```\n\n"
            "Return your review in markdown with the following sections:\n\n"
            "### 🔍 Issues Found:\n[List of issues]\n\n"
            "### ✅ Suggestions for Improvement:\n[Suggestions]\n\n"
            "### 📘 Explanations:\n[Explanation of complex code]\n\n"
            "### 🧠 Code Quality Score (out of 10):\n[Score and justification]"
        )

        prompt = PromptTemplate(
            input_variables=["code_input"],
            template=prompt_text
        )

        chain = LLMChain(llm=llm, prompt=prompt)

        with st.spinner("Analyzing your code..."):
            result = chain.run(code_input)

        st.markdown("---")
        st.subheader("📋 Code Review Summary")
        st.markdown(result)

