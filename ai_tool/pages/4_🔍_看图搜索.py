"""🔍 看图搜索 Agent"""
import streamlit as st

from vision_app import run_app

st.set_page_config(page_title="看图搜索 Agent", page_icon="🔍", layout="centered")
run_app()
