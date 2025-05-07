import openai
import streamlit as st

# Set up the OpenAI API key (you should add this in the Streamlit secrets.toml file)
openai.api_key = st.secrets["openai_api_key"]

# Function to reduce the input size by trimming the first few lines of code
def generate_code_review(input_code):
    # Limit the input to the first 5 lines of code for shorter input
    shortened_input = "\n".join(input_code.splitlines()[:5])  # Adjust number of lines as needed
    
    # Prompt for OpenAI
    prompt = f"Please review the following Python code for bugs, errors, and improvement suggestions:\n\n{shortened_input}"

    # Call the OpenAI API
    response = openai.Completion.create(
        engine="text-davinci-003",  # Or GPT-4 if using that model
        prompt=prompt,
        max_tokens=1000,  # Adjust this based on your needs
        temperature=0.7
    )

    return response['choices'][0]['text'].strip()

# Streamlit app UI setup
st.title("AI Code Review Bot")

# Input field for code
input_code = st.text_area("Paste your Python code here", height=300)

# Option to shorten the input code for analysis
shorten_input = st.checkbox("Shorten input code to the first 5 lines")

# Button to trigger code review
if st.button("Review Code"):
    if input_code:
        # Shorten the input code if the checkbox is selected
        if shorten_input:
            code_review = generate_code_review(input_code)
        else:
            code_review = generate_code_review(input_code)  # No shortening, if the checkbox is unchecked
        
        # Display the review result
        st.subheader("Code Review Result")
        st.write(code_review)
    else:
        st.warning("Please paste some code to review.")



