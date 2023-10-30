import streamlit as st


def paint_page():
    st.markdown("[点击跳转](http://47.100.136.183:7860/)")
    st.markdown("AI画图服务会不定时关闭，请见谅。一些例子请看下面。")
    tab1, tab2 = st.tabs(["文字生成图片", "图片生成图片"])
    with tab1:
        col1, col2 = st.columns([1, 1])
        col1.markdown(
            "medium shot of a woman traveller ready for the journey waiting on the train station, detailed sharp, flash photo")
        col2.image("1.png")
        col1, col2 = st.columns([1, 1])
        col1.markdown(
            "full body photo,fashion photography of cute astronaut girl with long green hair,in space with galaxy behind,35mm,detailed,sunlight passing through hair")
        col2.image("2.png")
    with tab2:
        col1, col2, col3 = st.columns([1, 1, 1])
        col1.image("211.png")
        col1.image("221.png")
        col2.image("212.png")
        col2.image("222.png")
        col3.image("213.png")
        col3.image("223.png")
