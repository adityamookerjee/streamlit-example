import streamlit as st
import requests  # Don't forget to import requests

st.title("Curative Member Booklets Chatbot")
import re

def extract_urls_from_response(api_response):
    source_documents = api_response.get("source_document", [])
    formatted_urls = []

    for document in source_documents:
        matches = re.findall(r'Link: \[PDF Link\]\((https://[^)]+)\)', document)
        for match in matches:
            formatted_urls.append(match)

    formatted_urls = list(set(formatted_urls))  # Remove duplicates if any
    formatted_urls.sort()

    if formatted_urls:
        result = "Here are some sections of the Curative Member Portal Benefits Guide that I used in my answer:\n"
        for url in formatted_urls:
            page_number = re.search(r'#page=(\d+)', url).group(1)
            result += "\n"
            result += f"Page {page_number} : {url}"
            result += "\n"
        return result
    else:
        return None

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("What is up?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        
        # Send a POST request
        response = requests.post(
            "https://ai-guild.dev.curative.com/chatbot",
            json={"query": prompt}
        )

        # Check the request was successful
        if response.status_code == 200:
            assistant_message = response.json().get("answer", "")
            # Your handling code, for example appending to messages and showing in UI
            st.session_state.messages.append({"role": "assistant", "content": assistant_message})
            message_placeholder.markdown(assistant_message)
            extracted_references = extract_urls_from_response(response.json())
            if extracted_references:
                st.session_state.messages.append({"role": "assistant", "content": extracted_references})
                message_placeholder.markdown(extracted_references)
                
        else:
            st.error("The request failed. Please try again later.")
            # Optionally, you can add more error handling code here
