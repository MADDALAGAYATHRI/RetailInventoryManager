import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from datetime import datetime, timedelta
from utils.data_manager import DataManager

def check_authentication():
    """Check if user is authenticated, redirect to login if not"""
    if 'user_authenticated' not in st.session_state or not st.session_state.user_authenticated:
        st.switch_page("pages/0_Login.py")
        return False
    return True

# Check authentication before proceeding
if not check_authentication():
    st.stop()

st.set_page_config(page_title="Lifestyle Analysis", page_icon="📊", layout="wide")

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

st.title("📊 Lifestyle Pattern Analysis")
st.markdown("*Understanding the connections between your lifestyle and mental health*")

# Time period selection
col1, col2 = st.columns([3, 1])
with col2:
    time_period = st.selectbox(
        "Analysis Period",
        ["Last 7 Days", "Last 30 Days", "Last 90 Days"],
        index=1
    )

period_map = {
    "Last 7 Days": 7,
    "Last 30 Days": 30,
    "Last 90 Days": 90
}

days = period_map[time_period]

# Ensure user session is properly initialized
if 'user_id' not in st.session_state:
    st.session_state.user_id = st.session_state.get('user_id', 'anonymous_user')

# Get data
data = data_manager.get_recent_data(st.session_state.user_id, days=days)

if data.empty:
    st.warning("📋 No data available for analysis. Please complete some daily check-ins first!")
    if st.button("Start Daily Check-In"):
        st.switch_page("pages/1_Daily_Check_In.py")
    st.stop()

# Summary statistics
st.markdown("---")
st.subheader("📈 Summary Statistics")

col1, col2, col3, col4 = st.columns(4)

with col1:
    avg_mood = data['mood_score'].mean()
    mood_trend = "📈" if data['mood_score'].iloc[-1] > data['mood_score'].iloc[0] else "📉" if data['mood_score'].iloc[-1] < data['mood_score'].iloc[0] else "➡️"
    st.metric(
        "Average Mood", 
        f"{avg_mood:.1f}/10",
        delta=f"{mood_trend} Trend"
    )

with col2:
    avg_stress = data['stress_level'].mean()
    stress_trend = "📈" if data['stress_level'].iloc[-1] > data['stress_level'].iloc[0] else "📉" if data['stress_level'].iloc[-1] < data['stress_level'].iloc[0] else "➡️"
    st.metric(
        "Average Stress", 
        f"{avg_stress:.1f}/10",
        delta=f"{stress_trend} Trend"
    )

with col3:
    avg_sleep = data['sleep_hours'].mean()
    st.metric(
        "Average Sleep", 
        f"{avg_sleep:.1f} hrs",
        delta=f"Target: 7-9 hrs"
    )

with col4:
    total_exercise = data['exercise_minutes'].sum()
    st.metric(
        "Total Exercise", 
        f"{total_exercise} min",
        delta=f"Avg: {total_exercise/len(data):.0f} min/day"
    )

# Correlation analysis
st.markdown("---")
st.subheader("🔗 Lifestyle Correlations")

# Calculate correlations
correlations = {
    'Sleep & Mood': data['sleep_hours'].corr(data['mood_score']),
    'Exercise & Mood': data['exercise_minutes'].corr(data['mood_score']),
    'Work Hours & Stress': data['work_hours'].corr(data['stress_level']),
    'Sleep & Stress': data['sleep_hours'].corr(data['stress_level']),
    'Exercise & Stress': data['exercise_minutes'].corr(data['stress_level']),
    'Caffeine & Stress': data['caffeine_intake'].corr(data['stress_level'])
}

# Remove NaN correlations
correlations = {k: v for k, v in correlations.items() if not pd.isna(v)}

if correlations:
    col1, col2 = st.columns(2)
    
    with col1:
        # Positive correlations
        st.markdown("#### 💚 Positive Relationships")
        positive_corrs = {k: v for k, v in correlations.items() if v > 0.3}
        if positive_corrs:
            for factor, corr in positive_corrs.items():
                st.markdown(f"• **{factor}**: {corr:.2f} (Strong)")
        else:
            moderate_positive = {k: v for k, v in correlations.items() if 0.1 < v <= 0.3}
            for factor, corr in moderate_positive.items():
                st.markdown(f"• **{factor}**: {corr:.2f} (Moderate)")
    
    with col2:
        # Negative correlations
        st.markdown("#### ⚠️ Areas of Concern")
        negative_corrs = {k: v for k, v in correlations.items() if v < -0.3}
        if negative_corrs:
            for factor, corr in negative_corrs.items():
                st.markdown(f"• **{factor}**: {corr:.2f} (Strong)")
        else:
            moderate_negative = {k: v for k, v in correlations.items() if -0.3 <= v < -0.1}
            for factor, corr in moderate_negative.items():
                st.markdown(f"• **{factor}**: {corr:.2f} (Moderate)")

# Detailed visualizations
st.markdown("---")
st.subheader("📊 Detailed Analysis")

# Sleep analysis
st.markdown("#### 😴 Sleep Pattern Analysis")
fig_sleep = make_subplots(
    rows=2, cols=2,
    subplot_titles=("Sleep vs Mood", "Sleep vs Stress", "Sleep Hours Over Time", "Sleep Quality Distribution"),
    specs=[[{"secondary_y": False}, {"secondary_y": False}],
           [{"secondary_y": True}, {"secondary_y": False}]]
)

# Sleep vs Mood scatter
fig_sleep.add_trace(
    go.Scatter(x=data['sleep_hours'], y=data['mood_score'], 
               mode='markers', name='Sleep vs Mood',
               marker=dict(color='#52C41A', size=8, opacity=0.7)),
    row=1, col=1
)

# Sleep vs Stress scatter
fig_sleep.add_trace(
    go.Scatter(x=data['sleep_hours'], y=data['stress_level'], 
               mode='markers', name='Sleep vs Stress',
               marker=dict(color='#FF7875', size=8, opacity=0.7)),
    row=1, col=2
)

# Sleep over time
fig_sleep.add_trace(
    go.Scatter(x=data['date'], y=data['sleep_hours'], 
               mode='lines+markers', name='Sleep Hours',
               line=dict(color='#1890FF', width=3)),
    row=2, col=1
)

# Add recommended sleep range
fig_sleep.add_hline(y=7, line_dash="dash", line_color="green", 
                   annotation_text="Min Recommended", row=2, col=1)
fig_sleep.add_hline(y=9, line_dash="dash", line_color="green", 
                   annotation_text="Max Recommended", row=2, col=1)

# Sleep distribution
sleep_ranges = pd.cut(data['sleep_hours'], bins=[0, 6, 7, 9, 24], 
                     labels=['<6h', '6-7h', '7-9h', '>9h'])
sleep_dist = sleep_ranges.value_counts()

fig_sleep.add_trace(
    go.Bar(x=sleep_dist.index, y=sleep_dist.values,
           marker_color=['#FF4D4F', '#FAAD14', '#52C41A', '#1890FF']),
    row=2, col=2
)

fig_sleep.update_layout(height=600, showlegend=False, title_text="Sleep Analysis Dashboard")
fig_sleep.update_xaxes(title_text="Sleep Hours", row=1, col=1)
fig_sleep.update_xaxes(title_text="Sleep Hours", row=1, col=2)
fig_sleep.update_xaxes(title_text="Date", row=2, col=1)
fig_sleep.update_xaxes(title_text="Sleep Range", row=2, col=2)
fig_sleep.update_yaxes(title_text="Mood Score", row=1, col=1)
fig_sleep.update_yaxes(title_text="Stress Level", row=1, col=2)
fig_sleep.update_yaxes(title_text="Sleep Hours", row=2, col=1)
fig_sleep.update_yaxes(title_text="Days", row=2, col=2)

st.plotly_chart(fig_sleep, use_container_width=True)

# Exercise analysis
st.markdown("#### 💪 Exercise Impact Analysis")
col1, col2 = st.columns(2)

with col1:
    # Exercise vs mood
    fig_ex_mood = px.scatter(data, x='exercise_minutes', y='mood_score',
                            title='Exercise vs Mood Score',
                            labels={'exercise_minutes': 'Exercise Minutes',
                                   'mood_score': 'Mood Score'},
                            color='stress_level',
                            color_continuous_scale='RdYlGn_r')
    fig_ex_mood.update_layout(height=400)
    st.plotly_chart(fig_ex_mood, use_container_width=True)

with col2:
    # Weekly exercise pattern
    # Convert date column to datetime if it's not already
    if not pd.api.types.is_datetime64_any_dtype(data['date']):
        data['date'] = pd.to_datetime(data['date'])
    
    data['day_of_week'] = data['date'].dt.day_name()
    day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    weekly_exercise = data.groupby('day_of_week')['exercise_minutes'].mean().reindex(day_order)
    
    fig_weekly = px.bar(x=weekly_exercise.index, y=weekly_exercise.values,
                       title='Average Exercise by Day of Week',
                       labels={'x': 'Day', 'y': 'Average Minutes'},
                       color=weekly_exercise.values,
                       color_continuous_scale='Greens')
    fig_weekly.update_layout(height=400, showlegend=False)
    st.plotly_chart(fig_weekly, use_container_width=True)

# Work-life balance
st.markdown("#### ⚖️ Work-Life Balance Analysis")
col1, col2 = st.columns(2)

with col1:
    # Work hours vs stress
    fig_work = px.scatter(data, x='work_hours', y='stress_level',
                         title='Work Hours vs Stress Level',
                         labels={'work_hours': 'Work Hours',
                                'stress_level': 'Stress Level'},
                         color='mood_score',
                         color_continuous_scale='RdYlGn')
    fig_work.update_layout(height=400)
    st.plotly_chart(fig_work, use_container_width=True)

with col2:
    # Work hours distribution
    work_ranges = pd.cut(data['work_hours'], bins=[0, 6, 8, 10, 24], 
                        labels=['<6h', '6-8h', '8-10h', '>10h'])
    work_dist = work_ranges.value_counts()
    
    fig_work_dist = px.pie(values=work_dist.values, names=work_dist.index,
                          title='Work Hours Distribution',
                          color_discrete_sequence=['#52C41A', '#FAAD14', '#FF7875', '#FF4D4F'])
    fig_work_dist.update_layout(height=400)
    st.plotly_chart(fig_work_dist, use_container_width=True)

# Insights and recommendations
st.markdown("---")
st.subheader("💡 Personalized Insights")

insights = []

# Sleep insights
avg_sleep = data['sleep_hours'].mean()
if avg_sleep < 7:
    insights.append("😴 **Sleep Improvement Needed**: You're averaging less than 7 hours of sleep. Consider improving your sleep hygiene.")
elif avg_sleep > 9:
    insights.append("😴 **Monitor Sleep Quality**: You're sleeping more than 9 hours on average. Quality might be more important than quantity.")
else:
    insights.append("😴 **Good Sleep Duration**: You're maintaining healthy sleep hours (7-9 hours).")

# Exercise insights
avg_exercise = data['exercise_minutes'].mean()
if avg_exercise < 15:
    insights.append("💪 **Increase Physical Activity**: Try to aim for at least 30 minutes of exercise most days.")
elif avg_exercise >= 30:
    insights.append("💪 **Great Exercise Habits**: You're maintaining excellent physical activity levels.")

# Work-life balance
avg_work = data['work_hours'].mean()
if avg_work > 10:
    insights.append("⚖️ **Work-Life Balance**: Consider reducing work hours or improving work efficiency to reduce stress.")

# Stress patterns
high_stress_days = (data['stress_level'] >= 7).sum()
if high_stress_days > len(data) * 0.3:
    insights.append("🚨 **Stress Management Priority**: You've had high stress levels on multiple days. Consider stress reduction techniques.")

# Display insights
for insight in insights:
    st.markdown(f"• {insight}")

if not insights:
    st.success("🎉 You're maintaining excellent lifestyle patterns! Keep up the great work.")

# Navigation
st.markdown("---")
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("🏠 Back to Dashboard"):
        st.switch_page("app.py")
with col2:
    if st.button("🎯 Get Interventions"):
        st.switch_page("pages/4_Interventions.py")
with col3:
    if st.button("🔮 Stress Prediction"):
        st.switch_page("pages/3_Stress_Prediction.py")
