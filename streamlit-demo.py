import streamlit as st
from sherlock.core import Sherlock
from claudette import Chat, models
import os
from dotenv import load_dotenv
from toolslm.xml import folder2ctx

load_dotenv()

# Initialize Sherlock client
s = Sherlock(os.getenv('SHERLOCK_AGENT_PRIVATE_KEY_HEX', ''))

# Create context from sherlock source files
sherlock_context = folder2ctx('sherlock', file_glob='*.py')

print(sherlock_context)
# Initialize Claudette chat with context
sp = f'''You are a helpful assistant that has access to a domain registrar and DNS management API. 
Keep responses concise and clear. You also have access to the Sherlock SDK source code to help answer questions about its implementation.

{sherlock_context}'''

chat = Chat(models[1], sp=sp, tools=s.as_tools())

st.title("Sherlock Domains Assistant")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []
    # Add initial AI welcome message
    welcome_msg = """Hello! I can help you manage domains and DNS records through the Sherlock API. I can:
- Check domain availability
- Register new domains
- Manage DNS records
- Look up domain information

I also have access to the Sherlock Domains Python SDK source code, so I can explain how any feature works under the hood!

What can I help you with?"""
    st.session_state.messages.append({"role": "assistant", "content": welcome_msg})

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("What would you like to know about domains?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
        
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        response = chat.toolloop(prompt)
        content = response.content[0].text
        message_placeholder.markdown(content)
        st.session_state.messages.append({"role": "assistant", "content": content})