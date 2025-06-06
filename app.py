# -*- coding: utf-8 -*-
"""
Created on Thu Jun  5 20:35:24 2025

@author: xiexiangfei
"""
import streamlit as st
import os
from PIL import Image
from io import BytesIO

# ======================= 页面配置和介绍 ===========================
st.set_page_config(page_title="Text2Image with CLIP", layout="centered")

st.title("🧠 Text2Image with CLIP")
st.markdown("使用 OpenAI 的 **CLIP 模型**，将自然语言描述逐步优化生成图像，并可导出动画。")

# 📖 项目简介
with st.expander("📖 什么是 Text-to-Image？点击展开了解"):
    st.markdown("""
    本项目使用 [OpenAI CLIP](https://openai.com/research/clip) 模型，将文本提示（Prompt）映射为图像特征。

    系统通过优化一张初始噪声图，使其在 CLIP 的嵌入空间中尽可能“接近”目标文本的嵌入向量，从而得到与描述相符的图像。

    每张图像是一步优化的结果，最终生成 10 张图像并合成为动画，形象展示了 AI 是如何“理解并画出”你输入的语言描述的。
    """)

# 📌 使用方法说明
with st.expander("📌 如何使用？（点击展开）"):
    st.markdown("""
    - 在上方下拉菜单中选择一个主题（如 `a_rainbow_flower`）
    - 页面将自动播放生成图像过程的 GIF 动画
    - 可点击“下载 GIF 动画”将整个过程保存下来
    - 使用滑块查看某一步生成图像
    - 页面底部展示所有 PNG 图像，便于逐帧查看和对比
    """)

# ======================= 图像处理部分 ===========================

# 图像目录（你已经生成图像的地方）
image_dir = "images"

# 获取所有 .png 图像文件
image_files = sorted([f for f in os.listdir(image_dir) if f.endswith(".png")])

# 提取所有主题（如 a_rainbow_flower）
themes = sorted(set(f.rsplit('_step_', 1)[0] for f in image_files))
selected_theme = st.selectbox("选择一个生成主题", themes)

# ======================= 自动播放动画 ===========================
st.header("🎞️ 自动播放动画")

frames = []
for i in range(1, 11):
    img_path = os.path.join(image_dir, f"{selected_theme}_step_{i*10}.png")
    image = Image.open(img_path).convert("RGB").resize((512, 512))
    frames.append(image)

# 合成 GIF 到内存
gif_buffer = BytesIO()
frames[0].save(
    gif_buffer,
    format='GIF',
    save_all=True,
    append_images=frames[1:],
    duration=500,
    loop=0
)
gif_bytes = gif_buffer.getvalue()

# 显示 GIF 动画
st.image(gif_bytes, caption=f"{selected_theme} 自动播放", output_format="GIF")

# 下载 GIF 按钮
st.download_button(
    label="📥 下载 GIF 动画",
    data=gif_bytes,
    file_name=f"{selected_theme}.gif",
    mime="image/gif"
)

# ======================= 拖动查看单张图 ===========================
st.header("🖼️ 分步预览每一张 PNG")

step_map = {i: i * 10 for i in range(1, 11)}
step = st.slider("拖动查看第几步图像", 1, 10, 10)
actual_step = step_map[step]
file_name = f"{selected_theme}_step_{actual_step}.png"
image_path = os.path.join(image_dir, file_name)

if os.path.exists(image_path):
    st.image(Image.open(image_path), caption=f"第 {step} 步 / 实际文件: {file_name}", use_column_width=True)
else:
    st.warning(f"未找到图像：{file_name}")

# ======================= 展示所有图像分页 ===========================
st.header("📂 PNG 图像文件总览（按顺序）")

for i in range(1, 11):
    png_path = os.path.join(image_dir, f"{selected_theme}_step_{i*10}.png")
    st.image(Image.open(png_path), caption=f"Step {i} - {os.path.basename(png_path)}", use_column_width=True)
