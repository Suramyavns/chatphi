from dotenv import load_dotenv
from huggingface_hub import InferenceClient
import os
import streamlit as st

load_dotenv()
st.set_page_config('PHI-CHAT',page_icon='microsoft.png')
st.title('PHI-CHAT')

client = InferenceClient(api_key=os.getenv('apiKey'))

messages = []
chat=[]

if 'messages' not in st.session_state:
    st.session_state['messages']=messages
else:
    messages = st.session_state.messages

if 'chat' not in st.session_state:
    st.session_state['chat']=chat
else:
    chat = st.session_state.chat

user_input = st.chat_input('Your message: ')
if user_input:
    chat.append(f'{user_input}')
    messages.append({"role": "user", "content": user_input})
    response = []
    for message in client.chat_completion(
        model="microsoft/Phi-3.5-mini-instruct",
        messages=messages,
        max_tokens=1000,
        stream=True,
    ):
        response.append(message.choices[0].delta.content)
    chat.append(f'{''.join(response)}')
    st.session_state.message=message
    st.session_state.chat=chat
for index in range(len(st.session_state.chat)):
    if index%2==0:
        st.markdown('**YOU**'+': '+st.session_state.chat[index])
    else:
        st.markdown('**PHI:**'+st.session_state.chat[index])
