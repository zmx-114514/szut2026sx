"""💗 AI 伴侣"""
import streamlit as st

from companion_app import run_app

st.set_page_config(page_title="AI 伴侣", page_icon="💗", layout="centered")
run_app()
