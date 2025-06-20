import streamlit as st
import requests
from zhipuai import ZhipuAI
import base64

if "openai_api_key" not in st.session_state:
    st.session_state["openai_api_key"] = ""

st.set_page_config(
    page_title="Emotional AI",
    page_icon="🇨🇳",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.balloons()

st.title("🤩 Hello, Welcome to Emotional AI!")

# ZhipuAI API Key
ZHIPU_API_KEY = "12121212121212121212121212121212"  # 替换为你的智谱AI API Key

with st.container():
    st.header("OpenAI Settings")
    st.markdown(f"""
       | **OpenAI API Key** | **Description** |
       |--------------------|-----------------|
       | {st.session_state["openai_api_key"]} | Your OpenAI API key for accessing the OpenAI services. |        
    """)

# 智谱AI 对话区
st.header("智谱AI 对话")
col1, col2 = st.columns([4,1])
with col1:
    user_input = st.text_input("请输入您的问题：", "", key="zhipuai_input")
with col2:
    ask_clicked = st.button("Ask", key="ask_zhipuai")

if 'zhipuai_history' not in st.session_state:
    st.session_state['zhipuai_history'] = []

if ask_clicked and user_input.strip():
    try:
        client = ZhipuAI(api_key=ZHIPU_API_KEY)
        # 构造对话历史
        messages = []
        for q, a in st.session_state['zhipuai_history']:
            messages.append({"role": "user", "content": q})
            messages.append({"role": "assistant", "content": a})
        messages.append({"role": "user", "content": user_input})
        response = client.chat.completions.create(
            model="glm-4-plus",
            messages=messages
        )
        # 修正返回内容的获取方式
        answer = response.choices[0].message.content
        st.session_state['zhipuai_history'].append((user_input, answer))
    except Exception as e:
        st.session_state['zhipuai_history'].append((user_input, f"请求异常: {e}"))

# 结果展示区
if st.session_state['zhipuai_history']:
    st.subheader("对话历史")
    for idx, (q, a) in enumerate(reversed(st.session_state['zhipuai_history'])):
        with st.expander(f"你：{q}", expanded=(idx==0)):
            st.markdown(f"**ZhipuAI 回复：**\n{a}")

# 智谱AI 图片生成区
st.header("智谱AI 图片生成")
col_img1, col_img2 = st.columns([4,1])
with col_img1:
    img_prompt = st.text_input("请输入你想生成的图片描述：", "", key="zhipuai_img_prompt")
with col_img2:
    img_ask_clicked = st.button("生成图片", key="zhipuai_img_ask")

if 'zhipuai_img_history' not in st.session_state:
    st.session_state['zhipuai_img_history'] = []

if img_ask_clicked and img_prompt.strip():
    try:
        client = ZhipuAI(api_key=ZHIPU_API_KEY)
        response = client.images.generations(
            model="cogview-4-250304",
            prompt=img_prompt
        )
        img_url = response.data[0].url
        st.session_state['zhipuai_img_history'].append((img_prompt, img_url))
    except Exception as e:
        st.session_state['zhipuai_img_history'].append((img_prompt, f"请求异常: {e}"))

# 图片生成历史展示区
if st.session_state['zhipuai_img_history']:
    st.subheader("图片生成历史")
    for idx, (desc, url) in enumerate(reversed(st.session_state['zhipuai_img_history'])):
        with st.expander(f"描述：{desc}", expanded=(idx==0)):
            if url.startswith("http"):
                st.image(url, caption=desc)
            else:
                st.error(url)

# 智谱AI 图片/视频理解区
st.header("智谱AI 图片/视频理解")
media_file = st.file_uploader("请上传图片或视频：", type=["jpg", "jpeg", "png", "bmp", "gif", "mp4", "mov", "avi"], key="zhipuai_media_upload")
media_ask = st.button("理解内容", key="zhipuai_media_ask")

if 'zhipuai_media_history' not in st.session_state:
    st.session_state['zhipuai_media_history'] = []

if media_ask and media_file is not None:
    try:
        # 读取并base64编码
        media_bytes = media_file.read()
        media_base64 = base64.b64encode(media_bytes).decode('utf-8')
        # 判断类型
        if media_file.type.startswith('image/'):
            media_type = 'image_url'
        elif media_file.type.startswith('video/'):
            media_type = 'video_url'
        else:
            st.session_state['zhipuai_media_history'].append((media_file.name, "暂不支持的文件类型"))
            media_type = None
        if media_type:
            client = ZhipuAI(api_key=ZHIPU_API_KEY)
            response = client.chat.completions.create(
                model="glm-4v-plus-0111",
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": media_type,
                                media_type: {
                                    "url": media_base64
                                }
                            },
                            {
                                "type": "text",
                                "text": "请描述这个内容"
                            }
                        ]
                    }
                ]
            )
            answer = response.choices[0].message.content
            st.session_state['zhipuai_media_history'].append((media_file.name, answer))
    except Exception as e:
        st.session_state['zhipuai_media_history'].append((media_file.name, f"请求异常: {e}"))

# 图片/视频理解历史展示区
if st.session_state['zhipuai_media_history']:
    st.subheader("图片/视频理解历史")
    for idx, (fname, result) in enumerate(reversed(st.session_state['zhipuai_media_history'])):
        with st.expander(f"文件：{fname}", expanded=(idx==0)):
            st.markdown(f"**理解结果：**\n{result}")