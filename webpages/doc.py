import os
import time
import streamlit as st
import openai
from streamlit_chatbox import *
from langchain.embeddings import OpenAIEmbeddings
from llama_index.llms import AzureOpenAI
from llama_index import VectorStoreIndex, SimpleDirectoryReader, ServiceContext, LangchainEmbedding
from llama_index import set_global_service_context

openai.api_type = st.secrets["openai_api_type"]
openai.api_base = st.secrets["openai_api_base"]
openai.api_key = st.secrets["openai_api_key"]
openai.api_version = st.secrets["openai_api_version"]

def doc_page():
    chat_box = ChatBox()

    if 'index' not in st.session_state:
        st.session_state["index"] = None
    if 'documents_folder' not in st.session_state:
        st.session_state["documents_folder"] = "./" + str(int(time.time()))

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
        st.markdown("上传你自己的文档，然后围绕着这个文档和喵聊聊。")
        uploaded_file = st.file_uploader('upload', type=['pdf', 'txt', 'docx', 'md'], label_visibility="collapsed")
        if st.button('上传 :scroll:') and uploaded_file is not None:
            with st.spinner("文件上传中..."):
                if not os.path.exists(st.session_state["documents_folder"]):
                    os.makedirs(st.session_state["documents_folder"])
                with open(st.session_state["documents_folder"] + "/" + uploaded_file.name, mode='wb') as w:
                    w.write(uploaded_file.getvalue())
                documents = SimpleDirectoryReader(st.session_state["documents_folder"]).load_data()
                st.session_state["index"] = VectorStoreIndex.from_documents(documents)
                os.remove(st.session_state["documents_folder"] + "/" + uploaded_file.name)
                os.rmdir(st.session_state["documents_folder"])
            st.success('成功上传文件!', icon="✅")

    llm = AzureOpenAI(engine="gpt35", model="gpt-35-turbo")

    embedding_llm = LangchainEmbedding(
        OpenAIEmbeddings(
            model="text-embedding-ada-002",
            deployment="ada002",
            openai_api_key=st.secrets["openai_api_key"],
            openai_api_base=st.secrets["openai_api_base"],
            openai_api_type=st.secrets["openai_api_type"],
            openai_api_version=st.secrets["openai_api_version"],
        ),
        embed_batch_size=1,
    )

    service_context = ServiceContext.from_defaults(
        llm=llm,
        embed_model=embedding_llm,
    )

    set_global_service_context(service_context)

    chat_box.init_session()
    chat_box.output_messages()
    user_input = st.chat_input()
    if user_input:
        with st.spinner("寻找答案中..."):
            chat_box.user_say(user_input)
            query_engine = st.session_state["index"].as_query_engine(response_mode="compact")
            response = query_engine.query(user_input)
            chat_box.ai_say(str(response))
