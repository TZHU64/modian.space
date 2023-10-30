import streamlit as st
import openai
from streamlit_option_menu import option_menu

openai.api_type = st.secrets["openai_api_type"]
openai.api_base = st.secrets["openai_api_base"]
openai.api_key = st.secrets["openai_api_key"]
openai.api_version = st.secrets["openai_api_version"]

def eng_request(user_input,gpt_type):
    if gpt_type == "GPT-4":
        id = "gpt4"
    else:
        id = "gpt35"
    response = openai.ChatCompletion.create(
        deployment_id=id,
        messages=[
            {"role": "system",
             "content": "I want you to act as an English translator, spelling corrector and improver. I will speak to you in any language and you will detect the language, translate it and answer in the corrected and improved version of my text, in English. I want you to replace my simplified A0-level words and sentences with more beautiful and elegant, upper level English words and sentences. Keep the meaning same, but make them more literary. I want you to only reply the correction, the improvements and nothing else, do not write explanations."},
            {"role": "user", "content": user_input},
        ],
        temperature=0.7
    )
    return response


def chn_request(user_input, gpt_type):
    if gpt_type == "GPT-4":
        id = "gpt4"
    else:
        id = "gpt35"
    response = openai.ChatCompletion.create(
        deployment_id=id,
        messages=[
            {"role": "system",
             "content": "下面我让你来充当翻译家，你的目标是把任何语言翻译成中文，请翻译时不要带翻译腔，而是要翻译得自然、流畅和地道，使用优美和高雅的表达方式。"},
            {"role": "user", "content": user_input},
        ],
        temperature=0.7
    )
    return response


def academic_request(user_input,gpt_type):
    if gpt_type == "GPT-4":
        id = "gpt4"
    else:
        id = "gpt35"
    response = openai.ChatCompletion.create(
        deployment_id=id,
        messages=[
            {"role": "system",
             "content": "Below is a paragraph from an academic paper. Polish the writing to meet the academic style, improve the spelling, grammar, clarity, concision and overall readability. When necessary, rewrite the whole sentence. Furthermore, list all modification and explain the reasons to do so in markdown table."},
            {"role": "user", "content": user_input},
        ],
        temperature=0.7
    )
    return response


def lang_page():
    with st.sidebar:
        gpt_type = st.selectbox("请选择模型:", ["ChatGPT (GPT-3.5)", "GPT-4"], index=0)
        st.markdown("""___""")

    lang_choose = option_menu("语言专家",
                              ["英语专家", "中文翻译", "英语学术"],
                              icons=['cup', 'cup-hot','cup-straw'],
                              menu_icon='globe-asia-australia',
                              default_index=0,
                              orientation="horizontal",
                              )
    if lang_choose == "英语专家":
        st.markdown(
            "AI已被赋予了英语专家的角色：它将担任英语翻译、拼写校对和修辞改进的角色。你可以用任何语言和它交流，它会识别你的语言，并将句子替换成更为优美和高雅的英语表达方式，它会确保意思不变，但使其更具文学性。")

    elif lang_choose == "中文翻译":
        st.markdown(
            "AI已被赋予了中文翻译的角色：它将充当翻译家，它的目标是把任何语言翻译成中文，翻译时不会带翻译腔，而是要翻译得自然、流畅和地道，使用优美和高雅的表达方式。")

    elif lang_choose == "英语学术":
        st.markdown(
            "Polish the writing to meet the academic style, improve the spelling, grammar, clarity, concision and overall readability. When necessary, rewrite the whole sentence. Furthermore, list all modification and explain the reasons to do so in markdown table."
        )

    user_input = st.text_area("input", key="input", label_visibility="collapsed")
    send_button = st.button(":pencil: 发送")
    if send_button:
        with st.spinner("处理中..."):
            if lang_choose == "英语专家":
                response = eng_request(user_input,gpt_type)
            elif lang_choose == "中文翻译":
                response = chn_request(user_input,gpt_type)
            elif lang_choose == "英语学术":
                response = academic_request(user_input,gpt_type)
            st.markdown(response["choices"][0]["message"]["content"])