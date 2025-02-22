import streamlit as st
import time
from openai import OpenAI  # or the specific NVIDIA SDK you're using

def show_math_solver():
    # Set up NVIDIA API client
    client = OpenAI(
        base_url="https://api.groq.com/openai/v1",
        api_key=st.secrets["GROQ_API_KEY"]
    )

    # Initialize session state for messages
    if "messages" not in st.session_state:
        st.session_state.messages = []  # Start with an empty chat history


    # Display the main title only if it has not been displayed
    if "title_displayed" not in st.session_state:
        st.title("Data Engineer AI")
        st.session_state.title_displayed = True

    # Display the ongoing conversation in the main area
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # User input area for new messages
    prompt = st.chat_input("Ask a math question here")
    if prompt:
        # Add the new user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Generate a response from the API
        response_text = ""
        completion = client.chat.completions.create(
            model="qwen-2.5-32b",
            messages=[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages],
            temperature=0.5,
            max_tokens=1024,
            stream=True
        )

        # Stream assistant's response in real-time
        with st.chat_message("assistant"):
            placeholder = st.empty()
            for chunk in completion:
                if chunk.choices[0].delta.content is not None:
                    response_text += chunk.choices[0].delta.content
                    placeholder.markdown(response_text)
                    time.sleep(0.05)

        # Append the assistant's complete response to session state after the loop
        if response_text:
            st.session_state.messages.append({"role": "assistant", "content": response_text})
