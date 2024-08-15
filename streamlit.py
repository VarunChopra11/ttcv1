import streamlit as st
import openai
import os

# Streamlit UI
st.title("Azure OpenAI Integration")
user_input = st.text_input("Enter your prompt", "Retrieve mails of John Doe")

if st.button("Generate Response"):
    # Azure OpenAI setup
    endpoint = os.getenv("ENDPOINT_URL", "https://mailaeretro.openai.azure.com/")
    api_key = os.getenv("AZURE_OPENAI_API_KEY")
    deployment = os.getenv("DEPLOYMENT_NAME", "ttcv1Deployment")

    # Set the API base, key, and version
    openai.api_type = "azure"
    openai.api_key = api_key
    openai.api_base = endpoint
    openai.api_version = "2024-05-01-preview"

    try:
        completion = openai.ChatCompletion.create(
            deployment_id=deployment,
            messages= [
                {
                "role": "system",
                "content": "You are an email retrieval system that interprets user queries about emails including time periods, senders, and date ranges and maps them to specific commands according to dataset. For example, given the input: Show me last 10 days mails, the system should produce the output: {show_mails_of_days} {10}."
                },
                {
                "role": "user",
                "content": user_input
                }],
            max_tokens=800,
            temperature=0.7,
            top_p=0.95,
            frequency_penalty=0,
            presence_penalty=0,
        )
        st.write("Response:", completion.choices[0].message['content'])
    except Exception as e:
        st.error(f"Error: {str(e)}")
