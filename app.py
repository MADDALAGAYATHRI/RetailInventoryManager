import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import os
from utils.data_manager import DataManager
from utils.ml_models import StressPredictor
import numpy as np

# Page configuration
st.set_page_config(
    page_title="MindGuard - Mental Health Monitoring",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load custom CSS
def load_css():
    with open("styles/theme.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css()

# Initialize managers
@st.cache_resource
def get_data_manager():
    return DataManager()



data_manager = get_data_manager()

# Initialize session state
if 'user_id' not in st.session_state:
    st.session_state.user_id = 'anonymous_user'
if 'privacy_mode' not in st.session_state:
    st.session_state.privacy_mode = True

# Sidebar
with st.sidebar:
    st.image("https://via.placeholder.com/200x80/4A90A4/FFFFFF?text=MindGuard", use_column_width=True)
    
    # Welcome message
    st.markdown(f"**Welcome to MindGuard!** 👋")
    
    st.markdown("---")
    
    # Privacy indicator
    privacy_status = "🔒 Private Mode" if st.session_state.privacy_mode else "📊 Standard Mode"
    st.markdown(f"**Status:** {privacy_status}")
    
    # Quick stats
    st.markdown("### Quick Overview")
    recent_data = data_manager.get_recent_data(st.session_state.user_id, days=7)
    
    if not recent_data.empty:
        avg_mood = recent_data['mood_score'].mean()
        avg_stress = recent_data['stress_level'].mean()
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Avg Mood", f"{avg_mood:.1f}/10")
        with col2:
            st.metric("Avg Stress", f"{avg_stress:.1f}/10")
    else:
        st.info("Complete your first check-in to see stats!")

# Main content
st.title("🧠 MindGuard Mental Health Monitoring")
st.markdown("*Your personal companion for mental wellness and stress management*")

# Welcome section
st.markdown("---")
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    ### 📝 Daily Check-In
    Track your mood, stress levels, and daily activities
    """)
    if st.button("Start Check-In", use_container_width=True):
        st.switch_page("pages/1_Daily_Check_In.py")

with col2:
    st.markdown("""
    ### 📊 Lifestyle Analysis
    Understand patterns in your sleep, exercise, and work
    """)
    if st.button("View Analysis", use_container_width=True):
        st.switch_page("pages/2_Lifestyle_Analysis.py")

with col3:
    st.markdown("""
    ### 🎯 Stress Prediction
    AI-powered insights and early intervention alerts
    """)
    if st.button("Check Predictions", use_container_width=True):
        st.switch_page("pages/3_Stress_Prediction.py")

st.markdown("---")

# Recent trends visualization
st.subheader("📈 Recent Trends")
recent_data = data_manager.get_recent_data(st.session_state.user_id, days=14)

if not recent_data.empty:
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=recent_data['date'],
        y=recent_data['mood_score'],
        mode='lines+markers',
        name='Mood Score',
        line=dict(color='#52C41A', width=3),
        marker=dict(size=8)
    ))
    
    fig.add_trace(go.Scatter(
        x=recent_data['date'],
        y=recent_data['stress_level'],
        mode='lines+markers',
        name='Stress Level',
        line=dict(color='#FF7875', width=3),
        marker=dict(size=8)
    ))
    
    fig.update_layout(
        title="Mood and Stress Trends (Last 14 Days)",
        xaxis_title="Date",
        yaxis_title="Score (1-10)",
        hovermode='x unified',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#2C3E50'),
        height=400
    )
    
    fig.update_yaxis(range=[0, 10])
    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("📋 Start tracking your mental health by completing your first daily check-in!")

# Quick actions
st.markdown("---")
st.subheader("🚀 Quick Actions")

col1, col2, col3, col4 = st.columns(4)

with col1:
    if st.button("🎯 Get Interventions", use_container_width=True):
        st.switch_page("pages/4_Interventions.py")

with col2:
    if st.button("📚 Learn & Cope", use_container_width=True):
        st.switch_page("pages/6_Educational_Resources.py")

with col3:
    if st.button("📊 View Progress", use_container_width=True):
        st.switch_page("pages/5_Progress_Tracking.py")

with col4:
    if st.button("🔐 Privacy Settings", use_container_width=True):
        st.switch_page("pages/7_Privacy_Settings.py")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #8E8E93; font-size: 0.9em;'>
    <p>🛡️ Your data is encrypted and stored securely. We prioritize your privacy above all.</p>
    <p>For immediate crisis support, contact your local emergency services or mental health crisis line.</p>
</div>
""", unsafe_allow_html=True)
