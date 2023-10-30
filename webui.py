import streamlit as st
from streamlit_option_menu import option_menu
from webpages.chat import chat_page
from webpages.cust import cust_page
from webpages.doc import doc_page
from webpages.lang import lang_page
from webpages.paint import paint_page


st.set_page_config(
    page_title="墨点小助手",
    page_icon=":cat:"
)

hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

def check_password():
    def password_entered():
        if st.session_state["password"] == st.secrets["password"]:
            st.session_state["password_correct"] = True
            del st.session_state["password"]
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        st.text_input(
            "请输入密码：", type="password", on_change=password_entered, key="password"
        )
        return False
    elif not st.session_state["password_correct"]:
        st.text_input(
            "请输入密码：", type="password", on_change=password_entered, key="password"
        )
        st.error("😕 密码不正确")
        return False
    else:
        return True

if check_password():
    with st.sidebar:
        st.columns(3)[1].image("modian.png")
        choose = option_menu("墨点小助手",
                             ["和喵聊聊", "文档助手", "语言专家", "定制聊天", "智能画图"],
                             icons=['chat-heart', 'archive', 'translate', 'book', 'image'],
                             menu_icon="robot",
                             default_index=0,
                             )

    if choose == "和喵聊聊":
        chat_page()

    elif choose == "文档助手":
        doc_page()

    elif choose == "语言专家":
        lang_page()

    elif choose == "定制聊天":
        cust_page()
        
    elif choose == "智能画图":
        paint_page()