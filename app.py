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

        # Enhanced prompt that forces all sections
        prompt_text = (
            "You are a senior software engineer tasked with reviewing the following code. "
            "Please provide a detailed review with the following sections, in **exact order**, with clear explanations and no omissions:\n\n"
            
            "### 🔍 Issues Found:\n"
            "1. List all bugs, potential issues, or bad practices in the code. Include explanations for why each issue is a problem.\n\n"
            
            "### ✅ Suggestions for Improvement:\n"
            "2. Provide specific suggestions for fixing each issue and improving the code's quality. "
            "If something is correct, explain why it's good.\n\n"
            
            "### 📘 Explanations:\n"
            "3. For each issue and suggestion, provide a detailed explanation, including best practices or alternative approaches.\n\n"
            
            "### 🧠 Code Quality Score (out of 10):\n"
            "4. Give the code a quality score based on readability, efficiency, maintainability, and structure. "
            "Justify the score with detailed reasoning.\n\n"
            
            "### Important Instructions:\n"
            "- Do **not** skip any of these sections. All sections are mandatory.\n"
            "- Follow the **exact** order of sections as specified.\n\n"
            
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


