import streamlit as st
from openai import AuthenticationError, OpenAI


def get_openai_api_key() -> str:
    if "OPENAI_API_KEY" in st.secrets:
        return st.secrets["OPENAI_API_KEY"]
    if "openai_api_key" in st.secrets:
        return st.secrets["openai_api_key"]
    if "openai" in st.secrets:
        openai_section = st.secrets["openai"]
        if "apikey" in openai_section:
            return openai_section["apikey"]
        if "api_key" in openai_section:
            return openai_section["api_key"]

    st.error(
        "Missing OpenAI API key in Streamlit secrets. Add one of: "
        "`OPENAI_API_KEY`, `openai_api_key`, or `[openai] apikey`."
    )
    st.stop()


def get_client() -> OpenAI:
    return OpenAI(api_key=get_openai_api_key())


def review_code(client: OpenAI, code_input: str) -> str:
    prompt = (
        "You are a senior Python developer. Review the following code and return a detailed response "
        "in the exact sections below:\n\n"
        "### Issues Found:\n"
        "- List any bugs, bad practices, or concerns.\n"
        "- Explain why each issue matters.\n\n"
        "### Suggestions for Improvement:\n"
        "- Suggest fixes or enhancements.\n"
        "- Mention good practices if found.\n\n"
        "### Explanations:\n"
        "- Provide detailed reasoning for your review.\n\n"
        "### Code Quality Score (out of 10):\n"
        "- Score based on readability, efficiency, and structure.\n"
        "- Include a short justification.\n\n"
        "Only respond in this format. Code:\n"
        f"```python\n{code_input}\n```"
    )
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        temperature=0.5,
        messages=[
            {"role": "system", "content": "You are a meticulous Python code reviewer."},
            {"role": "user", "content": prompt},
        ],
    )
    return response.choices[0].message.content or ""


st.set_page_config(page_title="AI Code Review Bot", page_icon="🤖")
st.title("🤖 AI Code Review Bot")
st.markdown("Paste your code below and get AI-powered review with improvements, explanations, and a quality score.")

code_input = st.text_area(
    "🧾 Enter your Python code:",
    height=300,
    placeholder="e.g. def add(a, b): return a + b",
)

max_code_length = 800
if len(code_input) > max_code_length:
    code_input = code_input[:max_code_length]
    st.warning("Your code was too long and has been truncated to fit token limits.")

if st.button("🚀 Review My Code"):
    if not code_input.strip():
        st.error("Please enter some code first.")
    else:
        try:
            with st.spinner("Analyzing code with AI..."):
                response = review_code(get_client(), code_input)
        except AuthenticationError:
            st.error(
                "OpenAI authentication failed. Check that your Streamlit secret contains a valid OpenAI API key."
            )
            st.stop()

        st.subheader("📋 Review Result")
        st.markdown(response)
