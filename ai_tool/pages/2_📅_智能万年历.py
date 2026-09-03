"""📅 智能万年历"""
import streamlit as st

from calendar_app import run_app

st.set_page_config(page_title="智能万年历", page_icon="📅", layout="centered")
run_app()
