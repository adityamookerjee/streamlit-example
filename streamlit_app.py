import streamlit as st
import requests  # Don't forget to import requests

st.title("Curative Member Booklets Chatbot")


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
        else:
            st.error("The request failed. Please try again later.")
            # Optionally, you can add more error handling code here
