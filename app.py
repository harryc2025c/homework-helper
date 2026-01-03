import streamlit as st
import google.generativeai as genai
from PIL import Image

st.set_page_config(page_title="AI作业督导", page_icon="📚")
st.title("📚 AI 作业督导系统")

# 检查密钥
if "GEMINI_API_KEY" in st.secrets:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
    # 使用 models/ 前缀是目前最稳定的写法
    try:
       # 建议直接使用这个写法，这是目前最通用的
model = genai.GenerativeModel('gemini-1.5-flash')
    except Exception as e:
        st.error(f"模型初始化失败，请检查API权限: {e}")
else:
    st.error("请在 Settings -> Secrets 中输入 GEMINI_API_KEY")
    st.stop()

# 侧边栏：显示当前状态
st.sidebar.success("大脑连接状态：正常" if api_key else "大脑连接状态：断开")

# 上传组件
img_file = st.file_uploader("拍照上传你的作业清单或完成图", type=['jpg', 'png', 'jpeg'])

if img_file:
    img = Image.open(img_file)
    st.image(img, caption="图片已加载", width=300)
    
    task_type = st.radio("你想让AI做什么？", ["制定时间规划", "检查完成情况并打分"])
    
    if st.button("开始分析"):
        with st.spinner('AI 正在发功...'):
            try:
                if task_type == "制定时间规划":
                    prompt = "你是一个高效学习专家。请识别图中的作业，并根据任务量给我一个晚上2小时内的具体时间分配建议。"
                else:
                    prompt = "请检查这张作业是否写完了。如果写完了请夸我；如果没写完或在敷衍，请随机生成一个身体锻炼惩罚，并用毒舌语气说出来。"
                
                response = model.generate_content([prompt, img])
                st.write("---")
                st.markdown(response.text)
            except Exception as e:
                st.error(f"分析失败。错误原因：{e}")
                st.info("提示：如果显示 NotFound，请去 AI Studio 确认 API 密钥是否有效。")
