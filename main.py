import os
import streamlit as st
from openai import AzureOpenAI
from azure.identity import DefaultAzureCredential, get_bearer_token_provider

st.title("Azure OpenAI Integration")
user_input = st.text_input("Enter your prompt", "Retrieve mails of John Doe")

if st.button("Generate Response"):
    endpoint = os.getenv("ENDPOINT_URL", "https://mailaeretro.openai.azure.com/")
    deployment = os.getenv("DEPLOYMENT_NAME", "ttcv1Deployment")

    token_provider = get_bearer_token_provider(
        DefaultAzureCredential(),
        "https://cognitiveservices.azure.com/.default")
        
    client = AzureOpenAI(
        azure_endpoint=endpoint,
        azure_ad_token_provider=token_provider,
        api_version="2024-05-01-preview",
    )
        
    try:
        completion = client.chat.completions.create(
            model=deployment,
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
            stop=None,
            stream=False
        )
        st.write("Response:", completion.choices[0].message.content)
    except Exception as e:
        st.error(f"Error: {str(e)}")