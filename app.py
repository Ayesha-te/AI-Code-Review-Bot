import streamlit as st
import os
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
import tiktoken  # To check token usage

# Load OpenAI API key from Streamlit secrets
os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]

# Streamlit setup
st.set_page_config(page_title="AI Code Review Bot", page_icon="🤖")
st.title("🤖 AI Code Review Bot")
st.markdown("Paste your Python code below and get AI-powered suggestions, improvements, and explanations.")

# Function to count tokens in a text using tiktoken
def count_tokens(text: str) -> int:
    enc = tiktoken.get_encoding("gpt-3.5-turbo")  # Adjust according to the model
    return len(enc.encode(text))

# Code input field
code_input = st.text_area(
    "👨‍💻 Paste your code here:",
    height=300,
    placeholder="e.g. def add(a, b): return a + b"
)

# Review button
if st.button("🧠 Review My Code"):
    if not code_input.strip():
        st.warning("Please paste some code to review.")
    else:
        # Check token count
        token_count = count_tokens(code_input)
        max_tokens = 3500  # Set your token limit here (consider both input and output tokens)
        
        if token_count > max_tokens:
            st.warning(f"Your code exceeds the maximum token limit of {max_tokens}. Trimming the input.")
            # Truncate the input to fit within the token limit
            truncated_input = code_input[:max_tokens]
        else:
            truncated_input = code_input

        # LangChain LLM setup
        llm = OpenAI(temperature=0.7)

        # Enhanced prompt with more specific instructions
        prompt_text = (
            "You are a senior software engineer tasked with reviewing the following code. "
            "Please provide a comprehensive and detailed review with the following sections in **exact order**, "
            "including explanations, suggestions, and a quality score. Do not skip any sections.\n\n"
            
            "### 🔍 Issues Found:\n"
            "1. Identify all bugs, potential issues, or bad practices in the code. "
            "For each issue, explain why it is a problem.\n\n"
            
            "### ✅ Suggestions for Improvement:\n"
            "2. Provide **specific** suggestions for fixing each issue and improving the quality of the code. "
            "If the code is correct in some parts, explain why it is correct.\n\n"
            
            "### 📘 Explanations:\n"
            "3. For each issue and suggestion, provide **detailed explanations**, including best practices, alternative approaches, or clarifications.\n\n"
            
            "### 🧠 Code Quality Score (out of 10):\n"
            "4. Evaluate the quality of the code based on readability, efficiency, maintainability, and structure. "
            "Give the code a score out of 10 and provide a detailed justification for the score.\n\n"
            
            "### Important Instructions:\n"
            "- Do **not** skip any of these sections. All sections are mandatory.\n"
            "- Be sure to follow the **exact** order of sections as specified.\n\n"
            
            "Code to review:\n"
            "```python\n{truncated_input}\n```"
        )

        # Create prompt template with code input
        prompt = PromptTemplate(
            input_variables=["truncated_input"],
            template=prompt_text
        )

        # Create the LLM chain
        chain = LLMChain(llm=llm, prompt=prompt)

        with st.spinner("Analyzing your code..."):
            # Run the chain to generate the response
            result = chain.run(truncated_input)

        # Display the formatted review
        st.markdown("---")
        st.subheader("📋 Code Review Summary")
        st.markdown(result)

        # Debugging: Output raw result if needed
        st.write("### Raw Response from AI:")
        st.code(result)




