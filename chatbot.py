from dotenv import load_dotenv
import streamlit as st
from langchain_groq import ChatGroq
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI
from langchain_ollama import ChatOllama

# load the env variables
load_dotenv()

# streamlit page setup
st.set_page_config(
    page_title="Chatbot", # Got emoji from emojidb.org
    page_icon="🤖",
    layout="centered"
)
st.title("🗫 Generative AI Chatbot")

options_map = {
    "OpenAI": ["gpt-4.1-2025-04-14", "GPT-4.1 nano"],
    "Gemini": ["gemini-2.5-flash", "gemini-3.5-flash-lite"],
    "Groq": ["llama-3.3-70b-versatile", "llama-3.1-8b-instant"],
    "Ollama": ["gemma2:2b"]
}

#initiate session vars
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "provider" not in st.session_state:
    st.session_state.provider = "Groq"

if "model" not in st.session_state:
    st.session_state.model = options_map["Groq"][0]

def update_model():
    st.session_state.model = options_map[st.session_state.provider][0]

# prompt for provider
provider = st.selectbox(
    "Select a provider",
    list(options_map.keys()),
    index=list(options_map.keys()).index(st.session_state.provider),
    key = "provider",
    on_change=update_model
)

# prompt for model (depends on provider)
model = st.selectbox(
    "Select a model",
    options_map[st.session_state.provider],
    key = "model"
)

st.write("You picked: ", st.session_state.provider, "->", st.session_state.model)

#show chat history
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

#llm initiate
chat_object_types = {
    "OpenAI": ChatOpenAI,
    "Gemini": ChatGoogleGenerativeAI,
    "Groq": ChatGroq,
    "Ollama": ChatOllama
}

# Initialize the llm with the selected model
llm = chat_object_types[st.session_state.provider](
    model=st.session_state.model,
    temperature=0.0,
)

#input box
user_prompt = st.chat_input("Ask Chatbot...")

if user_prompt:
    st.chat_message("user").markdown(user_prompt)
    st.session_state.chat_history.append({"role": "user", "content": user_prompt})

    response = llm.invoke(
        input=[{"role": "system", "content": "You are a helpful assistant"}, *st.session_state.chat_history]
    )
    assistant_response = response.content
    st.session_state.chat_history.append({"role": "assistant", "content": assistant_response})

    with st.chat_message("assistant"):
        st.markdown(assistant_response)