import streamlit as st
import google.generativeai as genai
from PIL import Image

# 设置页面
st.set_page_config(page_title="AI作业督导", page_icon="📚")
st.title("📚 AI 作业督导系统")

# 从设置中安全获取密钥
if "GEMINI_API_KEY" in st.secrets:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')
else:
    st.error("请输入 API 密钥以继续。")
    st.stop()

# 界面设计
tab1, tab2 = st.tabs(["📅 作业规划", "✅ 提交证明"])

with tab1:
    st.header("第一步：上传清单")
    uploaded_list = st.file_uploader("拍摄作业清单", type=['jpg', 'png', 'jpeg'], key="list")
    if uploaded_list:
        img = Image.open(uploaded_list)
        st.image(img, caption="已收到的清单", width=300)
        if st.button("让AI制定计划"):
            with st.spinner('AI 正在看你的作业...'):
                prompt = "你是一个严谨且有幽默感的督导老师。请识别图中所有的作业任务，并根据现在的时间为我制定一个详细的完成计划。如果任务非常重，请给我一点鼓励或警告。"
                response = model.generate_content([prompt, img])
                st.markdown(f"### 📋 AI 的规划建议：\n{response.text}")

with tab2:
    st.header("第二步：完成打卡")
    uploaded_proof = st.file_uploader("拍摄完成的作业（证明材料）", type=['jpg', 'png', 'jpeg'], key="proof")
    if uploaded_proof:
        img_p = Image.open(uploaded_proof)
        st.image(img_p, caption="你提交的证明", width=300)
        if st.button("请求AI审核"):
            with st.spinner('AI 正在检查你有没有偷懒...'):
                prompt = "请核对这张作业图片是否真的完成了作业要求。如果看起来完成了，请热烈夸奖；如果看起来是乱涂乱画或完全没做，请给出一个有趣的轻微惩罚（比如：罚做20个深蹲，或者不准玩手机10分钟）。"
                response = model.generate_content([prompt, img_p])
                st.success(response.text)
