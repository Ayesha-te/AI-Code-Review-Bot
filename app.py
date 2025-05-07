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
st.markdown("Paste your code below and get AI-powered suggestions, improvements, and explanations.")

# Code input field
code_input = st.text_area(
    "👨‍💻 Paste your code here:",
    height=300,
    placeholder="e.g. def add(a, b): return a + b"
)

# Review button
if st.button("🧠 Review My Code"):
    if not code_input.strip():
        st.warning("Please paste some code first.")
    else:
        # LangChain LLM setup
        llm = OpenAI(temperature=0.7)

        # Refined prompt with more explicit instructions and sample output
        prompt_text = (
            "You are a senior software engineer tasked with reviewing the following code. "
            "Please provide a detailed review in markdown format with the following sections:\n\n"
            
            "### 🔍 Issues Found:\n"
            "List all bugs, potential issues, or bad practices in the code. Include explanations for why each issue is a problem.\n\n"
            
            "### ✅ Suggestions for Improvement:\n"
            "Provide specific suggestions for fixing each issue and improving the code's quality. If something is good, explain why it's correct.\n\n"
            
            "### 📘 Explanations:\n"
            "For each issue and suggestion, provide a detailed explanation, including best practices or alternative approaches.\n\n"
            
            "### 🧠 Code Quality Score (out of 10):\n"
            "Give the code a quality score based on readability, efficiency, maintainability, and structure. Justify the score with detailed reasoning.\n\n"
            
            "### Example Format:\n"
            "### 🔍 Issues Found:\n"
            "- Issue 1: The variable `x` is not initialized before use. This could cause a runtime error.\n"
            "- Issue 2: Using a list for key-value storage instead of a dictionary can lead to inefficient lookups.\n\n"
            "### ✅ Suggestions for Improvement:\n"
            "- Suggestion 1: Initialize `x` before using it, and consider defaulting it to `0`.\n"
            "- Suggestion 2: Replace the list with a dictionary for better performance.\n\n"
            "### 📘 Explanations:\n"
            "- Explanation 1: Initializing variables before use prevents runtime errors and improves code reliability.\n"
            "- Explanation 2: Using dictionaries for key-value lookups is much faster than using lists.\n\n"
            "### 🧠 Code Quality Score (out of 10):\n"
            "7/10: The code is readable and functional, but the performance could be optimized by using a dictionary instead of a list for lookups.\n\n"
            
            "Code to review:\n"
            "```python\n{code_input}\n```"
        )

        # Create prompt template with code input
        prompt = PromptTemplate(
            input_variables=["code_input"],
            template=prompt_text
        )

        # Create the LLM chain
        chain = LLMChain(llm=llm, prompt=prompt)

        with st.spinner("Analyzing your code..."):
            # Run the chain to generate the response
            result = chain.run(code_input)

        # Debugging: Output raw result
        st.write("### Raw Response from AI:")
        st.code(result)

        # Display the formatted review
        st.markdown("---")
        st.subheader("📋 Code Review Summary")
        st.markdown(result)

