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
        llm = OpenAI(temperature=0)

        # Improved prompt template with clearer instructions
        prompt_text = (
            "You are a senior software engineer. Review the following code for:\n\n"
            "1. Bugs or potential issues\n"
            "2. Bad programming practices\n"
            "3. Suggestions for cleaner or more efficient code\n"
            "4. Explanation of any complex logic\n\n"
            "Code:\n"
            "```python\n{code_input}\n```\n\n"
            "Return your review in markdown with the following sections:\n\n"
            "### 🔍 Issues Found:\n[List of issues and why they are problematic.]\n\n"
            "### ✅ Suggestions for Improvement:\n[Concrete suggestions for improving the code.]\n\n"
            "### 📘 Explanations:\n[Detailed explanations for the issues and suggestions, including what to avoid.]\n\n"
            "### 🧠 Code Quality Score (out of 10):\n[Score and detailed justification based on readability, efficiency, and maintainability.]"
        )

        # Create the prompt with the code input
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


