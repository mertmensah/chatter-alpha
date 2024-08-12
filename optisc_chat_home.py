import openai
import streamlit as st
import time

assistant_id = 'asst_kEaqnRablcCewoHO3oJoatlu'

client = openai

if "start_chat" not in st.session_state:
    st.session_state.start_chat = False
if "thread_id" not in st.session_state:
    st.session_state.thread_id = None

st.set_page_config(page_title="Supply Chain Consultant AI", page_icon=":speech_balloon:")

# replace for github
openai.api_key = 'yours'
# openai.api_key = 'replace_w_yours'

if st.sidebar.button("Start Chat"):
    st.session_state.start_chat = True
    thread = client.beta.threads.create()
    st.session_state.thread_id = thread.id


st.title("Your key to a state of the art supply chain, powered by AI")
st.write("We have compiled decades of applied theories from engineering, statistics, and supply chain management. Access this wealth of knowledge below.")


if st.button("Exit Chat"):
    st.session_state.messages = []  # Clear the chat history
    st.session_state.start_chat = False  # Reset the chat state
    st.session_state.thread_id = None

if st.session_state.start_chat:
    if "openai_model" not in st.session_state:
        st.session_state.openai_model = "gpt-3.5-turbo-1106" # "gpt-3.5-turbo-1106", "gpt-4-turbo-preview"
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Type your messages here."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        client.beta.threads.messages.create(
                thread_id=st.session_state.thread_id,
                role="user",
                content=prompt
            )
        
        run = client.beta.threads.runs.create(
            thread_id=st.session_state.thread_id,
            assistant_id=assistant_id,
            instructions="You are a world renowned scholar in supply chain management. You have multiple masters and PhD degrees in the field. You specialize in engineering, programming, statistics and supply chain management. You will be consulting users on how to optimize their network using leading theories and principles. Make sure you ask questions to the user to be able to provide them contextual answers. the field of supply chain is very wide, and you can only be valuable if you provide them with precise and implementable advice."
        )

        while run.status != 'completed':
            time.sleep(1)
            run = client.beta.threads.runs.retrieve(
                thread_id=st.session_state.thread_id,
                run_id=run.id
            )
        messages = client.beta.threads.messages.list(
            thread_id=st.session_state.thread_id
        )

        # Process and display assistant messages
        assistant_messages_for_run = [
            message for message in messages 
            if message.run_id == run.id and message.role == "assistant"
        ]
        for message in assistant_messages_for_run:
            st.session_state.messages.append({"role": "assistant", "content": message.content[0].text.value})
            with st.chat_message("assistant"):
                st.markdown(message.content[0].text.value)

else:
    st.write("Click 'Start Chat' to begin.")