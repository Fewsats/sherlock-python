import streamlit as st
from sherlock.core import Sherlock
from claudette import Chat, models
import os
from dotenv import load_dotenv
from toolslm.xml import folder2ctx, files2ctx

load_dotenv()

# Initialize Sherlock client
s = Sherlock(os.getenv('SHERLOCK_AGENT_PRIVATE_KEY_HEX', ''))

# Create context from sherlock source files
base_dir = os.path.dirname(os.path.realpath(__file__))
sherlock_dir = os.path.join(base_dir, '..', '..', 'sherlock')
readme_path = os.path.join(base_dir, '..', '..', 'README.md')

sherlock_context = folder2ctx(sherlock_dir, prefix=False, file_re=r'^[a-zA-Z0-9]+\.py$')
sherlock_context += files2ctx([readme_path])
demo_context = files2ctx([
    os.path.join(base_dir, 'main.py'),
    os.path.join(base_dir, 'requirements.txt'),
    os.path.join(base_dir, '.env.example')
])

# Initialize Claudette chat with context
sp = f'''You are a helpful assistant that has access to a domain registrar and DNS management API. 
Keep responses concise and clear. You also have access to the Sherlock Domains Python SDK source code, and the code for this streamlit demo to help answer questions about its implementation.

<sherlock_context>
{sherlock_context}
</sherlock_context>

<demo_context>
{demo_context}
</demo_context>
'''

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
        full_response = []
        
        def trace_cb(msgs):
            print('msgs', msgs)
            for msg in msgs:
                if msg.content and msg.role == 'assistant':
                    for block in msg.content:
                        if block.type == 'text':
                            st.markdown(block.text)
                        elif block.type == 'tool_use':
                            args = ', '.join(f'{k}={repr(v)}' for k,v in block.input.items())
                            st.markdown(f">`{block.name}({args})`")
                # Show tool results
                if msg.role == 'user' and isinstance(msg.content, list):
                    for content in msg.content:
                        if content.get('type') == 'tool_result':
                            st.markdown(f"`{content['content']}`")                
        response = chat.toolloop(prompt, trace_func=trace_cb)
        content = response.content[0].text
        st.session_state.messages.append({"role": "assistant", "content": content})