import streamlit as st
import os
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

# Load OpenAI API key from Streamlit secrets
os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]

# Streamlit page setup
st.set_page_config(page_title="AI Code Review Bot", page_icon="🤖")

# App title and description
st.title("🤖 AI Code Review Bot")
st.markdown("Paste your code below and get AI-powered suggestions, improvements, and explanations.")

# Code input field
code_input = st.text_area(
    label="👨‍💻 Paste your code here:",
    height=300,
    placeholder="Enter your Python, JavaScript, or other code..."
)

# Review button
if st.button("🧠 Review My Code"):
    if not code_input.strip():
        st.warning("Please paste some code before clicking review.")
    else:
        # LangChain LLM setup
        llm = OpenAI(temperature=0)

        # Prompt template (FIXED triple quotes)
        prompt = PromptTemplate(
            input_variables=["code_input"],
            template="""
You are a senior software engineer. Please review the following code for:

1. Bugs or potential issues  
2. Bad programming practices  
3. Suggestions for cleaner or more efficient code  
4. Explanation of any complex logic  

Code:
```python
{code_input}

