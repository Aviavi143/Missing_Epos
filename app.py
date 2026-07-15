import streamlit as st
import pandas as pd
import time

# --------------------------------------------------
# Page Config
# --------------------------------------------------
st.set_page_config(
    page_title="Missing Values Checker",
    page_icon="✅",
    layout="wide"
)

# --------------------------------------------------
# Custom CSS
# --------------------------------------------------
st.markdown("""
<style>

/* Main Background */
.stApp {
    background: linear-gradient(135deg, #0f172a, #1e293b);
}

/* Main Title */
.main-title {
    text-align: center;
    font-size: 60px;
    font-weight: bold;
    color: white;
    margin-top: 20px;
}

.sub-title {
    text-align: center;
    color: #d1d5db;
    font-size: 18px;
    margin-bottom: 30px;
}

/* Upload Section */
.upload-container {
    border: 2px dashed #6b7280;
    border-radius: 15px;
    padding: 25px;
    background-color: rgba(255,255,255,0.05);
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: #111827;
}

/* Cards */
.card {
    background-color: rgba(255,255,255
