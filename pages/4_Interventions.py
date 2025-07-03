import streamlit as st
import pandas as pd
from datetime import datetime, date
from utils.data_manager import DataManager
from utils.interventions import InterventionEngine

st.set_page_config(page_title="Interventions", page_icon="🎯", layout="wide")

# Load custom CSS
def load_css():
    with open("styles/theme.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css()

# Initialize components
@st.cache_resource
def get_data_manager():
    return DataManager()

@st.cache_resource
def get_intervention_engine():
    return InterventionEngine()

data_manager = get_data_manager()
intervention_engine = get_intervention_engine()

st.title("🎯 Personalized Stress Interventions")
st.markdown("*Evidence-based recommendations tailored to your current situation*")

# Get recent data
recent_data = data_manager.get_recent_data(st.session_state.user_id, days=7)

if recent_data.empty:
    st.warning("📋 No recent data available. Please complete some daily check-ins to get personalized recommendations.")
    if st.button("Complete Daily Check-In"):
        st.switch_page("pages/1_Daily_Check_In.py")
    st.stop()

# Current situation assessment
latest_entry = recent_data.iloc[-1]
current_stress = latest_entry['stress_level']
current_mood = latest_entry['mood_score']
current_energy = latest_entry['energy_level']

st.markdown("---")
st.subheader("📊 Current Situation")

col1, col2, col3 = st.columns(3)
with col1:
    stress_color = "#FF4D4F" if current_stress >= 7 else "#FAAD14" if current_stress >= 5 else "#52C41A"
    st.markdown(f"""
    <div style="text-align: center; padding: 15px; border-radius: 10px; background-color: {stress_color}20;">
        <h4 style="color: {stress_color}; margin: 0;">Stress Level</h4>
        <h2 style="color: {stress_color}; margin: 0;">{current_stress}/10</h2>
    </div>
    """, unsafe_allow_html=True)

with col2:
    mood_color = "#52C41A" if current_mood >= 7 else "#FAAD14" if current_mood >= 5 else "#FF4D4F"
    st.markdown(f"""
    <div style="text-align: center; padding: 15px; border-radius: 10px; background-color: {mood_color}20;">
        <h4 style="color: {mood_color}; margin: 0;">Mood Score</h4>
        <h2 style="color: {mood_color}; margin: 0;">{current_mood}/10</h2>
    </div>
    """, unsafe_allow_html=True)

with col3:
    energy_color = "#52C41A" if current_energy >= 7 else "#FAAD14" if current_energy >= 5 else "#FF4D4F"
    st.markdown(f"""
    <div style="text-align: center; padding: 15px; border-radius: 10px; background-color: {energy_color}20;">
        <h4 style="color: {energy_color}; margin: 0;">Energy Level</h4>
        <h2 style="color: {energy_color}; margin: 0;">{current_energy}/10</h2>
    </div>
    """, unsafe_allow_html=True)

# Get personalized interventions
user_profile = {
    'current_stress': current_stress,
    'current_mood': current_mood,
    'current_energy': current_energy,
    'avg_sleep': recent_data['sleep_hours'].mean(),
    'avg_exercise': recent_data['exercise_minutes'].mean(),
    'avg_work_hours': recent_data['work_hours'].mean(),
    'recent_symptoms': latest_entry.get('symptoms', ''),
    'preferred_activities': st.session_state.get('preferred_activities', [])
}

interventions = intervention_engine.get_personalized_interventions(user_profile)

# Immediate interventions (for current high stress)
if current_stress >= 7:
    st.markdown("---")
    st.subheader("🚨 Immediate Relief Strategies")
    st.error("High stress detected. Here are some quick techniques to help you right now:")
    
    immediate_interventions = intervention_engine.get_immediate_interventions(current_stress)
    
    for i, intervention in enumerate(immediate_interventions, 1):
        with st.expander(f"🎯 {intervention['title']} ({intervention['duration']})", expanded=i==1):
            st.markdown(intervention['description'])
            st.markdown("**Steps:**")
            for step in intervention['steps']:
                st.markdown(f"• {step}")
            
            if 'audio_guide' in intervention:
                st.markdown(f"🎵 **Audio Guide**: {intervention['audio_guide']}")
            
            # Track completion
            if st.button(f"✅ I completed this exercise", key=f"immediate_{i}"):
                st.success("Great job! Consistency with these techniques will improve their effectiveness.")
                # Log intervention completion
                data_manager.log_intervention(st.session_state.user_id, intervention['title'])

# Personalized intervention categories
st.markdown("---")
st.subheader("🎯 Personalized Recommendations")

# Organize interventions by category
categories = {
    'Physical': [i for i in interventions if i['category'] == 'Physical'],
    'Mental': [i for i in interventions if i['category'] == 'Mental'],
    'Social': [i for i in interventions if i['category'] == 'Social'],
    'Lifestyle': [i for i in interventions if i['category'] == 'Lifestyle']
}

# Create tabs for different categories
tab1, tab2, tab3, tab4 = st.tabs(["💪 Physical", "🧠 Mental", "👥 Social", "🏠 Lifestyle"])

with tab1:
    st.markdown("### Physical Interventions")
    physical_interventions = categories['Physical']
    
    for intervention in physical_interventions:
        with st.expander(f"{intervention['icon']} {intervention['title']} - {intervention['duration']}"):
            col1, col2 = st.columns([3, 1])
            
            with col1:
                st.markdown(intervention['description'])
                st.markdown("**Benefits:**")
                for benefit in intervention['benefits']:
                    st.markdown(f"• {benefit}")
                
                if intervention['steps']:
                    st.markdown("**How to do it:**")
                    for step in intervention['steps']:
                        st.markdown(f"• {step}")
            
            with col2:
                st.markdown(f"**Difficulty:** {intervention['difficulty']}")
                st.markdown(f"**Best Time:** {intervention['best_time']}")
                
                if st.button("✅ I'll try this", key=f"physical_{intervention['title']}"):
                    st.success("Added to your action plan!")
                    data_manager.log_intervention_plan(st.session_state.user_id, intervention['title'])

with tab2:
    st.markdown("### Mental & Cognitive Interventions")
    mental_interventions = categories['Mental']
    
    for intervention in mental_interventions:
        with st.expander(f"{intervention['icon']} {intervention['title']} - {intervention['duration']}"):
            col1, col2 = st.columns([3, 1])
            
            with col1:
                st.markdown(intervention['description'])
                st.markdown("**Benefits:**")
                for benefit in intervention['benefits']:
                    st.markdown(f"• {benefit}")
                
                if intervention['steps']:
                    st.markdown("**Instructions:**")
                    for step in intervention['steps']:
                        st.markdown(f"• {step}")
                
                if 'guided_script' in intervention:
                    st.markdown("**Guided Script:**")
                    st.markdown(f"*{intervention['guided_script']}*")
            
            with col2:
                st.markdown(f"**Difficulty:** {intervention['difficulty']}")
                st.markdown(f"**Best Time:** {intervention['best_time']}")
                
                if st.button("✅ I'll try this", key=f"mental_{intervention['title']}"):
                    st.success("Added to your action plan!")
                    data_manager.log_intervention_plan(st.session_state.user_id, intervention['title'])

with tab3:
    st.markdown("### Social & Connection Interventions")
    social_interventions = categories['Social']
    
    for intervention in social_interventions:
        with st.expander(f"{intervention['icon']} {intervention['title']} - {intervention['duration']}"):
            col1, col2 = st.columns([3, 1])
            
            with col1:
                st.markdown(intervention['description'])
                st.markdown("**Benefits:**")
                for benefit in intervention['benefits']:
                    st.markdown(f"• {benefit}")
                
                if intervention['steps']:
                    st.markdown("**Suggestions:**")
                    for step in intervention['steps']:
                        st.markdown(f"• {step}")
            
            with col2:
                st.markdown(f"**Difficulty:** {intervention['difficulty']}")
                st.markdown(f"**Best Time:** {intervention['best_time']}")
                
                if st.button("✅ I'll try this", key=f"social_{intervention['title']}"):
                    st.success("Added to your action plan!")
                    data_manager.log_intervention_plan(st.session_state.user_id, intervention['title'])

with tab4:
    st.markdown("### Lifestyle & Environmental Interventions")
    lifestyle_interventions = categories['Lifestyle']
    
    for intervention in lifestyle_interventions:
        with st.expander(f"{intervention['icon']} {intervention['title']} - {intervention['duration']}"):
            col1, col2 = st.columns([3, 1])
            
            with col1:
                st.markdown(intervention['description'])
                st.markdown("**Benefits:**")
                for benefit in intervention['benefits']:
                    st.markdown(f"• {benefit}")
                
                if intervention['steps']:
                    st.markdown("**Implementation:**")
                    for step in intervention['steps']:
                        st.markdown(f"• {step}")
            
            with col2:
                st.markdown(f"**Difficulty:** {intervention['difficulty']}")
                st.markdown(f"**Best Time:** {intervention['best_time']}")
                
                if st.button("✅ I'll try this", key=f"lifestyle_{intervention['title']}"):
                    st.success("Added to your action plan!")
                    data_manager.log_intervention_plan(st.session_state.user_id, intervention['title'])

# Crisis resources
st.markdown("---")
st.subheader("🆘 Crisis Support Resources")

with st.expander("🚨 If you're in crisis or need immediate help"):
    st.markdown("""
    **If you're having thoughts of self-harm or suicide, please reach out immediately:**
    
    🇺🇸 **United States:**
    - National Suicide Prevention Lifeline: **988**
    - Crisis Text Line: Text HOME to **741741**
    
    🇬🇧 **United Kingdom:**
    - Samaritans: **116 123** (free, 24/7)
    
    🇨🇦 **Canada:**
    - Talk Suicide Canada: **1-833-456-4566**
    
    🌍 **International:**
    - International Association for Suicide Prevention: [https://www.iasp.info/resources/Crisis_Centres/](https://www.iasp.info/resources/Crisis_Centres/)
    
    **Remember: You're not alone, and help is available.**
    """)

# Action plan summary
st.markdown("---")
st.subheader("📋 Your Action Plan")

planned_interventions = data_manager.get_planned_interventions(st.session_state.user_id)

if planned_interventions:
    st.success(f"You have {len(planned_interventions)} interventions in your action plan!")
    
    for i, intervention in enumerate(planned_interventions, 1):
        st.markdown(f"{i}. **{intervention}**")
    
    if st.button("📊 Track My Progress"):
        st.switch_page("pages/5_Progress_Tracking.py")
else:
    st.info("Add some interventions to your action plan by clicking '✅ I'll try this' on techniques that appeal to you.")

# Navigation
st.markdown("---")
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("🏠 Back to Dashboard"):
        st.switch_page("app.py")
with col2:
    if st.button("📚 Educational Resources"):
        st.switch_page("pages/6_Educational_Resources.py")
with col3:
    if st.button("🔮 Stress Predictions"):
        st.switch_page("pages/3_Stress_Prediction.py")
