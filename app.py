import streamlit as st
import os
from dotenv import load_dotenv
from google import genai

 
load_dotenv()

 
st.set_page_config(
    page_title="Gemini AI Chatbot",
    page_icon="🤖",
    layout="centered"
)

 
st.title("🤖 Gemini AI Chatbot")
st.write("Ask Gemini anything!")

 
api_key = os.getenv("GEMINI_API_KEY")

 
if not api_key:
    st.error("Gemini API key not found!")
    st.info(
        "Please create a .env file and add your "
        "GEMINI_API_KEY."
    )
    st.stop()

 
try:
    client = genai.Client(api_key=api_key)
except Exception as e:
    st.error(f"Client initialization error: {e}")
    st.stop()

 
if "messages" not in st.session_state:
    st.session_state.messages = []

 
if st.button("generate response"):
    st.session_state.messages = []
    st.rerun()

 
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

 
prompt = st.chat_input("Type your message here...")

if prompt:

     
    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })

    with st.chat_message("user"):
        st.markdown(prompt)

     
    with st.chat_message("assistant"):
        with st.spinner("Gemini is thinking..."):

            try:
                response = client.models.generate_content(
                    model="gemini-3.5-flash-lite",
                    contents=prompt
                )

                answer = response.text

                if not answer:
                    answer = "Gemini returned an empty response."

                st.markdown(answer)

                 
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": answer
                })

            except Exception as e:
                st.error(f"Error generating response: {e}")