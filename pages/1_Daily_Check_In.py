import streamlit as st
import pandas as pd
from datetime import datetime, date
from utils.data_manager import DataManager

st.set_page_config(page_title="Daily Check-In", page_icon="📝", layout="wide")

# Load custom CSS
def load_css():
    with open("styles/theme.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css()

# Initialize data manager
@st.cache_resource
def get_data_manager():
    return DataManager()

data_manager = get_data_manager()

st.title("📝 Daily Check-In")
st.markdown("*Take a moment to reflect on your current state*")

# Check if already checked in today
today = date.today()
existing_entry = data_manager.get_entry_by_date(st.session_state.user_id, today)

if existing_entry is not None:
    st.success("✅ You've already completed today's check-in!")
    st.markdown("### Today's Entry:")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Mood Score", f"{existing_entry['mood_score']}/10")
    with col2:
        st.metric("Stress Level", f"{existing_entry['stress_level']}/10")
    with col3:
        st.metric("Energy Level", f"{existing_entry['energy_level']}/10")
    
    if st.button("Update Today's Entry"):
        st.session_state.update_mode = True
        st.rerun()
else:
    st.info("🌅 Let's start your daily check-in")

# Check-in form
if existing_entry is None or st.session_state.get('update_mode', False):
    with st.form("daily_checkin"):
        st.markdown("### How are you feeling today?")
        
        col1, col2 = st.columns(2)
        
        with col1:
            mood_score = st.slider(
                "Mood Score (1=Very Low, 10=Excellent)",
                min_value=1, max_value=10, value=5,
                help="Rate your overall mood today"
            )
            
            stress_level = st.slider(
                "Stress Level (1=Very Relaxed, 10=Very Stressed)",
                min_value=1, max_value=10, value=5,
                help="How stressed do you feel right now?"
            )
            
            energy_level = st.slider(
                "Energy Level (1=Exhausted, 10=Very Energetic)",
                min_value=1, max_value=10, value=5,
                help="Rate your energy level today"
            )
        
        with col2:
            sleep_hours = st.number_input(
                "Hours of Sleep Last Night",
                min_value=0.0, max_value=24.0, value=7.0, step=0.5,
                help="How many hours did you sleep?"
            )
            
            exercise_minutes = st.number_input(
                "Exercise Minutes Today",
                min_value=0, max_value=720, value=0, step=5,
                help="Minutes of physical activity"
            )
            
            work_hours = st.number_input(
                "Work Hours Today",
                min_value=0.0, max_value=24.0, value=8.0, step=0.5,
                help="Hours spent working or studying"
            )
        
        st.markdown("### Additional Information")
        
        col3, col4 = st.columns(2)
        
        with col3:
            social_interaction = st.selectbox(
                "Social Interaction Level",
                ["None", "Minimal", "Moderate", "High"],
                help="How much social interaction did you have?"
            )
            
            caffeine_intake = st.number_input(
                "Caffeine Servings",
                min_value=0, max_value=20, value=0,
                help="Cups of coffee, tea, or other caffeinated drinks"
            )
        
        with col4:
            alcohol_intake = st.number_input(
                "Alcohol Servings",
                min_value=0, max_value=20, value=0,
                help="Standard drinks consumed"
            )
            
            meditation_minutes = st.number_input(
                "Meditation/Mindfulness Minutes",
                min_value=0, max_value=480, value=0, step=5,
                help="Time spent in meditation or mindfulness practice"
            )
        
        mood_notes = st.text_area(
            "Additional Notes (Optional)",
            placeholder="Any specific thoughts, events, or feelings you'd like to record...",
            help="This information helps improve our recommendations"
        )
        
        # Symptoms checklist
        st.markdown("### Symptoms Check")
        symptoms = st.multiselect(
            "Select any symptoms you're experiencing:",
            ["Headache", "Fatigue", "Anxiety", "Irritability", "Difficulty concentrating", 
             "Muscle tension", "Sleep problems", "Appetite changes", "Mood swings", "None"]
        )
        
        submitted = st.form_submit_button("💾 Save Check-In", use_container_width=True)
        
        if submitted:
            # Prepare data
            checkin_data = {
                'user_id': st.session_state.user_id,
                'date': today,
                'mood_score': mood_score,
                'stress_level': stress_level,
                'energy_level': energy_level,
                'sleep_hours': sleep_hours,
                'exercise_minutes': exercise_minutes,
                'work_hours': work_hours,
                'social_interaction': social_interaction,
                'caffeine_intake': caffeine_intake,
                'alcohol_intake': alcohol_intake,
                'meditation_minutes': meditation_minutes,
                'mood_notes': mood_notes,
                'symptoms': ', '.join(symptoms) if symptoms else '',
                'timestamp': datetime.now()
            }
            
            # Save data
            success = data_manager.save_daily_entry(checkin_data)
            
            if success:
                st.success("✅ Check-in saved successfully!")
                st.balloons()
                
                # Reset update mode
                if 'update_mode' in st.session_state:
                    del st.session_state.update_mode
                
                # Show quick insights
                st.markdown("### Quick Insights")
                
                if stress_level >= 7:
                    st.warning("🚨 High stress detected. Consider some relaxation techniques.")
                elif stress_level <= 3:
                    st.success("😌 Great! You're feeling relaxed today.")
                
                if sleep_hours < 6:
                    st.warning("😴 You might benefit from more sleep tonight.")
                elif sleep_hours >= 8:
                    st.success("💤 Excellent sleep duration!")
                
                if exercise_minutes >= 30:
                    st.success("💪 Great job staying active!")
                elif exercise_minutes == 0:
                    st.info("🚶‍♀️ Consider adding some physical activity to your day.")
                
                # Navigation buttons
                col1, col2, col3 = st.columns(3)
                with col1:
                    if st.button("🎯 Get Personalized Interventions"):
                        st.switch_page("pages/4_Interventions.py")
                with col2:
                    if st.button("📊 View Lifestyle Analysis"):
                        st.switch_page("pages/2_Lifestyle_Analysis.py")
                with col3:
                    if st.button("🏠 Back to Dashboard"):
                        st.switch_page("app.py")
            else:
                st.error("❌ Failed to save check-in. Please try again.")

# Navigation
st.markdown("---")
col1, col2 = st.columns(2)
with col1:
    if st.button("🏠 Back to Dashboard"):
        st.switch_page("app.py")
with col2:
    if st.button("📊 View My Progress"):
        st.switch_page("pages/5_Progress_Tracking.py")
