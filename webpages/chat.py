import streamlit as st
import openai
from streamlit_chatbox import *

openai.api_type = st.secrets["openai_api_type"]
openai.api_base = st.secrets["openai_api_base"]
openai.api_key = st.secrets["openai_api_key"]
openai.api_version = st.secrets["openai_api_version"]


def generate_response(message_log, temp, gpt_type):
    if gpt_type == "GPT-4":
        id = "gpt4"
    else:
        id = "gpt35"
    response = openai.ChatCompletion.create(
        deployment_id=id,
        messages=message_log,
        temperature=temp,
    )
    for choice in response.choices:
        if "text" in choice:
            return choice.text
    return response.choices[0].message.content


def chat_page():
    chat_box = ChatBox()

    if 'generated' not in st.session_state:
        st.session_state['generated'] = []

    if 'past' not in st.session_state:
        st.session_state['past'] = []

    if 'message_log' not in st.session_state:
        st.session_state['message_log'] = [{"role": "system", "content": "You are a helpful assistant."}]

    chat_box.init_session()
    chat_box.output_messages()
    user_input = st.chat_input()

    with st.sidebar:
        cols = st.columns(2)
        export_btn = cols[0]
        if cols[1].button("清空对话", use_container_width=True, ):
            chat_box.init_session(clear=True)
            st.experimental_rerun()

        export_btn.download_button(
            "导出记录",
            "".join(chat_box.export2md()),
            file_name=f"Chat.md",
            mime="text/markdown",
            use_container_width=True,
        )
        st.markdown("""___""")
        st.markdown("这是一只基于GPT的聊天猫，你可以和它聊天，它会根据你的输入自动生成回复。")
        gpt_type = st.selectbox("请选择模型:", ["ChatGPT (GPT-3.5)", "GPT-4"], index=0)

    if user_input:
        with st.spinner("思考中..."):
            chat_box.user_say(user_input)
            st.session_state['message_log'].append({"role": "user", "content": user_input})
            output = generate_response(st.session_state['message_log'], 0.7, gpt_type)
            st.session_state['message_log'].append({"role": "assistant", "content": output})
            st.session_state['past'].append(user_input)
            st.session_state['generated'].append(output)
            chat_box.ai_say(output)
