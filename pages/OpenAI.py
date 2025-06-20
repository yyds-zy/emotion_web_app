import streamlit as st

if "openai_api_key" not in st.session_state:
    st.session_state["openai_api_key"] = ""

st.set_page_config(
    page_title="OpenAI",
    page_icon="🤩",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title("OpenAI Settings")

openai_api_key = st.text_input("OpenAI API Key", value=st.session_state["openai_api_key"], type="default")

saved = st.button(
    "Save",
    on_click=lambda: st.session_state.update({"openai_api_key": st.session_state["openai_api_key"]}),
    use_container_width=True,
)

if saved:
    st.session_state["openai_api_key"] = openai_api_key
    st.success("API Key saved successfully!")