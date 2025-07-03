import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from datetime import datetime, timedelta, date
from utils.data_manager import DataManager

st.set_page_config(page_title="Progress Tracking", page_icon="📈", layout="wide")

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

st.title("📈 Progress Tracking Dashboard")
st.markdown("*Monitor your mental health journey and celebrate your improvements*")

# Time period selection
col1, col2, col3 = st.columns([2, 2, 2])
with col1:
    time_period = st.selectbox(
        "Time Period",
        ["Last 30 Days", "Last 60 Days", "Last 90 Days", "All Time"],
        index=0
    )

with col2:
    view_type = st.selectbox(
        "View Type",
        ["Overview", "Detailed Analysis", "Intervention Tracking"],
        index=0
    )

period_map = {
    "Last 30 Days": 30,
    "Last 60 Days": 60,
    "Last 90 Days": 90,
    "All Time": None
}

days = period_map[time_period]

# Get data
if days:
    data = data_manager.get_recent_data(st.session_state.user_id, days=days)
else:
    data = data_manager.get_all_data(st.session_state.user_id)

if data.empty:
    st.warning("📋 No data available for progress tracking. Please complete some daily check-ins first!")
    if st.button("Start Daily Check-In"):
        st.switch_page("pages/1_Daily_Check_In.py")
    st.stop()

# Calculate progress metrics
def calculate_progress_metrics(df):
    if len(df) < 2:
        return {}
    
    # Split data into first and second half for comparison
    mid_point = len(df) // 2
    first_half = df.iloc[:mid_point]
    second_half = df.iloc[mid_point:]
    
    metrics = {}
    
    # Average improvements
    metrics['mood_improvement'] = second_half['mood_score'].mean() - first_half['mood_score'].mean()
    metrics['stress_reduction'] = first_half['stress_level'].mean() - second_half['stress_level'].mean()
    metrics['energy_improvement'] = second_half['energy_level'].mean() - first_half['energy_level'].mean()
    
    # Sleep consistency
    metrics['sleep_consistency'] = -abs(second_half['sleep_hours'].std() - first_half['sleep_hours'].std())
    
    # Exercise increase
    metrics['exercise_improvement'] = second_half['exercise_minutes'].mean() - first_half['exercise_minutes'].mean()
    
    return metrics

progress_metrics = calculate_progress_metrics(data)

# Overview Dashboard
if view_type == "Overview":
    st.markdown("---")
    st.subheader("🎯 Key Progress Indicators")
    
    if progress_metrics:
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            mood_delta = progress_metrics['mood_improvement']
            mood_color = "normal" if abs(mood_delta) < 0.5 else ("inverse" if mood_delta > 0 else "off")
            st.metric(
                "Mood Progress", 
                f"{data['mood_score'].iloc[-1]:.1f}/10",
                delta=f"{mood_delta:+.1f}",
                delta_color=mood_color
            )
        
        with col2:
            stress_delta = progress_metrics['stress_reduction']
            stress_color = "normal" if abs(stress_delta) < 0.5 else ("normal" if stress_delta > 0 else "inverse")
            st.metric(
                "Stress Reduction", 
                f"{data['stress_level'].iloc[-1]:.1f}/10",
                delta=f"{stress_delta:+.1f}",
                delta_color=stress_color
            )
        
        with col3:
            energy_delta = progress_metrics['energy_improvement']
            energy_color = "normal" if abs(energy_delta) < 0.5 else ("normal" if energy_delta > 0 else "inverse")
            st.metric(
                "Energy Level", 
                f"{data['energy_level'].iloc[-1]:.1f}/10",
                delta=f"{energy_delta:+.1f}",
                delta_color=energy_color
            )
        
        with col4:
            exercise_delta = progress_metrics['exercise_improvement']
            st.metric(
                "Daily Exercise", 
                f"{data['exercise_minutes'].iloc[-1]:.0f} min",
                delta=f"{exercise_delta:+.0f} min",
                delta_color="normal" if exercise_delta >= 0 else "inverse"
            )
    
    # Main progress chart
    st.markdown("---")
    st.subheader("📊 Mental Health Trends")
    
    # Create main progress visualization
    fig = go.Figure()
    
    # Add trend lines
    fig.add_trace(go.Scatter(
        x=data['date'],
        y=data['mood_score'],
        mode='lines+markers',
        name='Mood Score',
        line=dict(color='#52C41A', width=3),
        marker=dict(size=6)
    ))
    
    fig.add_trace(go.Scatter(
        x=data['date'],
        y=data['stress_level'],
        mode='lines+markers',
        name='Stress Level',
        line=dict(color='#FF7875', width=3),
        marker=dict(size=6)
    ))
    
    fig.add_trace(go.Scatter(
        x=data['date'],
        y=data['energy_level'],
        mode='lines+markers',
        name='Energy Level',
        line=dict(color='#1890FF', width=3),
        marker=dict(size=6)
    ))
    
    # Add trend lines
    if len(data) > 7:
        # Calculate rolling averages
        data['mood_trend'] = data['mood_score'].rolling(window=7, center=True).mean()
        data['stress_trend'] = data['stress_level'].rolling(window=7, center=True).mean()
        
        fig.add_trace(go.Scatter(
            x=data['date'],
            y=data['mood_trend'],
            mode='lines',
            name='Mood Trend',
            line=dict(color='#52C41A', width=2, dash='dash'),
            opacity=0.7
        ))
        
        fig.add_trace(go.Scatter(
            x=data['date'],
            y=data['stress_trend'],
            mode='lines',
            name='Stress Trend',
            line=dict(color='#FF7875', width=2, dash='dash'),
            opacity=0.7
        ))
    
    fig.update_layout(
        title="Mental Health Progress Over Time",
        xaxis_title="Date",
        yaxis_title="Score (1-10)",
        hovermode='x unified',
        height=500,
        yaxis=dict(range=[0, 10])
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Weekly progress summary
    st.markdown("---")
    st.subheader("📅 Weekly Progress Summary")
    
    # Convert date column to datetime if it's not already
    if not pd.api.types.is_datetime64_any_dtype(data['date']):
        data['date'] = pd.to_datetime(data['date'])
    
    # Group data by week
    data['week'] = data['date'].dt.isocalendar().week
    data['year'] = data['date'].dt.year
    data['year_week'] = data['year'].astype(str) + '-W' + data['week'].astype(str).str.zfill(2)
    
    weekly_summary = data.groupby('year_week').agg({
        'mood_score': ['mean', 'std'],
        'stress_level': ['mean', 'std'],
        'energy_level': ['mean', 'std'],
        'sleep_hours': 'mean',
        'exercise_minutes': 'sum'
    }).round(2)
    
    # Flatten column names
    weekly_summary.columns = ['_'.join(col).strip() for col in weekly_summary.columns]
    weekly_summary = weekly_summary.tail(8)  # Last 8 weeks
    
    if not weekly_summary.empty:
        col1, col2 = st.columns(2)
        
        with col1:
            # Weekly mood and stress
            fig_weekly = go.Figure()
            
            fig_weekly.add_trace(go.Bar(
                x=weekly_summary.index,
                y=weekly_summary['mood_score_mean'],
                name='Avg Mood',
                marker_color='#52C41A',
                opacity=0.7
            ))
            
            fig_weekly.add_trace(go.Bar(
                x=weekly_summary.index,
                y=weekly_summary['stress_level_mean'],
                name='Avg Stress',
                marker_color='#FF7875',
                opacity=0.7
            ))
            
            fig_weekly.update_layout(
                title="Weekly Average Mood vs Stress",
                xaxis_title="Week",
                yaxis_title="Score (1-10)",
                barmode='group',
                height=400
            )
            
            st.plotly_chart(fig_weekly, use_container_width=True)
        
        with col2:
            # Weekly lifestyle factors
            fig_lifestyle = go.Figure()
            
            fig_lifestyle.add_trace(go.Scatter(
                x=weekly_summary.index,
                y=weekly_summary['sleep_hours_mean'],
                mode='lines+markers',
                name='Avg Sleep (hrs)',
                line=dict(color='#722ED1', width=3)
            ))
            
            # Add secondary y-axis for exercise
            fig_lifestyle.add_trace(go.Scatter(
                x=weekly_summary.index,
                y=weekly_summary['exercise_minutes_sum'] / 60,  # Convert to hours
                mode='lines+markers',
                name='Exercise (hrs/week)',
                line=dict(color='#FA8C16', width=3),
                yaxis='y2'
            ))
            
            fig_lifestyle.update_layout(
                title="Weekly Lifestyle Patterns",
                xaxis_title="Week",
                yaxis=dict(title="Sleep Hours", side="left"),
                yaxis2=dict(title="Exercise Hours", side="right", overlaying="y"),
                height=400
            )
            
            st.plotly_chart(fig_lifestyle, use_container_width=True)

# Detailed Analysis View
elif view_type == "Detailed Analysis":
    st.markdown("---")
    st.subheader("🔍 Detailed Progress Analysis")
    
    # Correlation analysis over time
    st.markdown("#### 📈 Pattern Recognition")
    
    # Calculate rolling correlations
    window_size = min(14, len(data) // 2)
    
    if len(data) >= window_size:
        rolling_corr_sleep_mood = data['sleep_hours'].rolling(window=window_size).corr(data['mood_score'])
        rolling_corr_exercise_stress = data['exercise_minutes'].rolling(window=window_size).corr(data['stress_level'])
        
        fig_corr = make_subplots(
            rows=2, cols=2,
            subplot_titles=("Sleep vs Mood Correlation", "Exercise vs Stress Correlation", 
                           "Mood Variability", "Stress Variability"),
            specs=[[{"secondary_y": False}, {"secondary_y": False}],
                   [{"secondary_y": False}, {"secondary_y": False}]]
        )
        
        # Rolling correlations
        fig_corr.add_trace(
            go.Scatter(x=data['date'], y=rolling_corr_sleep_mood,
                      mode='lines', name='Sleep-Mood Correlation',
                      line=dict(color='#52C41A')),
            row=1, col=1
        )
        
        fig_corr.add_trace(
            go.Scatter(x=data['date'], y=rolling_corr_exercise_stress,
                      mode='lines', name='Exercise-Stress Correlation',
                      line=dict(color='#FF7875')),
            row=1, col=2
        )
        
        # Variability analysis
        mood_rolling_std = data['mood_score'].rolling(window=7).std()
        stress_rolling_std = data['stress_level'].rolling(window=7).std()
        
        fig_corr.add_trace(
            go.Scatter(x=data['date'], y=mood_rolling_std,
                      mode='lines', name='Mood Variability',
                      line=dict(color='#1890FF')),
            row=2, col=1
        )
        
        fig_corr.add_trace(
            go.Scatter(x=data['date'], y=stress_rolling_std,
                      mode='lines', name='Stress Variability',
                      line=dict(color='#FA8C16')),
            row=2, col=2
        )
        
        fig_corr.update_layout(height=600, showlegend=False, title_text="Advanced Pattern Analysis")
        st.plotly_chart(fig_corr, use_container_width=True)
    
    # Goal achievement tracking
    st.markdown("#### 🎯 Goal Achievement")
    
    goals = {
        'Sleep (7-9 hrs)': ((data['sleep_hours'] >= 7) & (data['sleep_hours'] <= 9)).mean() * 100,
        'Exercise (≥30 min)': (data['exercise_minutes'] >= 30).mean() * 100,
        'Low Stress (<5)': (data['stress_level'] < 5).mean() * 100,
        'Good Mood (≥7)': (data['mood_score'] >= 7).mean() * 100,
        'Work-Life Balance (<10hrs)': (data['work_hours'] < 10).mean() * 100
    }
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Goal achievement chart
        fig_goals = go.Figure(data=[
            go.Bar(x=list(goals.keys()), y=list(goals.values()),
                   marker_color=['#52C41A' if v >= 70 else '#FAAD14' if v >= 50 else '#FF7875' for v in goals.values()])
        ])
        
        fig_goals.update_layout(
            title="Goal Achievement Rate (%)",
            yaxis_title="Achievement Rate (%)",
            height=400
        )
        
        fig_goals.add_hline(y=70, line_dash="dash", line_color="green", 
                           annotation_text="Target: 70%")
        
        st.plotly_chart(fig_goals, use_container_width=True)
    
    with col2:
        # Achievement insights
        st.markdown("**Goal Achievement Insights:**")
        
        for goal, achievement in goals.items():
            if achievement >= 70:
                st.success(f"✅ **{goal}**: {achievement:.1f}% - Excellent!")
            elif achievement >= 50:
                st.warning(f"⚠️ **{goal}**: {achievement:.1f}% - Good progress")
            else:
                st.error(f"❌ **{goal}**: {achievement:.1f}% - Needs improvement")
        
        # Best and worst performing areas
        best_goal = max(goals, key=goals.get)
        worst_goal = min(goals, key=goals.get)
        
        st.markdown("---")
        st.markdown(f"🏆 **Strongest Area**: {best_goal}")
        st.markdown(f"🎯 **Focus Area**: {worst_goal}")

# Intervention Tracking View
elif view_type == "Intervention Tracking":
    st.markdown("---")
    st.subheader("🎯 Intervention Effectiveness")
    
    # Get intervention data
    intervention_logs = data_manager.get_intervention_logs(st.session_state.user_id)
    planned_interventions = data_manager.get_planned_interventions(st.session_state.user_id)
    
    if intervention_logs:
        st.markdown("#### 📊 Intervention Usage")
        
        # Create intervention timeline
        intervention_df = pd.DataFrame(intervention_logs)
        intervention_df['date'] = pd.to_datetime(intervention_df['date'])
        
        # Count interventions by date
        daily_interventions = intervention_df.groupby('date').size().reset_index(name='count')
        
        # Merge with main data
        data_with_interventions = data.merge(daily_interventions, on='date', how='left')
        data_with_interventions['count'] = data_with_interventions['count'].fillna(0)
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Intervention usage over time
            fig_usage = px.bar(daily_interventions, x='date', y='count',
                              title='Daily Intervention Usage',
                              labels={'count': 'Number of Interventions', 'date': 'Date'})
            fig_usage.update_layout(height=400)
            st.plotly_chart(fig_usage, use_container_width=True)
        
        with col2:
            # Most used interventions
            intervention_counts = intervention_df['intervention_name'].value_counts().head(5)
            fig_popular = px.bar(x=intervention_counts.values, y=intervention_counts.index,
                               orientation='h', title='Most Used Interventions',
                               labels={'x': 'Usage Count', 'y': 'Intervention'})
            fig_popular.update_layout(height=400)
            st.plotly_chart(fig_popular, use_container_width=True)
        
        # Effectiveness analysis
        st.markdown("#### 📈 Intervention Effectiveness")
        
        # Compare mood/stress on days with vs without interventions
        with_interventions = data_with_interventions[data_with_interventions['count'] > 0]
        without_interventions = data_with_interventions[data_with_interventions['count'] == 0]
        
        if len(with_interventions) > 0 and len(without_interventions) > 0:
            effectiveness_metrics = {
                'Mood (with interventions)': with_interventions['mood_score'].mean(),
                'Mood (without interventions)': without_interventions['mood_score'].mean(),
                'Stress (with interventions)': with_interventions['stress_level'].mean(),
                'Stress (without interventions)': without_interventions['stress_level'].mean()
            }
            
            col1, col2 = st.columns(2)
            
            with col1:
                mood_improvement = effectiveness_metrics['Mood (with interventions)'] - effectiveness_metrics['Mood (without interventions)']
                st.metric(
                    "Mood Impact",
                    f"{effectiveness_metrics['Mood (with interventions)']:.1f}/10",
                    delta=f"{mood_improvement:+.1f} vs no interventions"
                )
            
            with col2:
                stress_reduction = effectiveness_metrics['Stress (without interventions)'] - effectiveness_metrics['Stress (with interventions)']
                st.metric(
                    "Stress Impact",
                    f"{effectiveness_metrics['Stress (with interventions)']:.1f}/10",
                    delta=f"{stress_reduction:+.1f} reduction"
                )
            
            if mood_improvement > 0.5 or stress_reduction > 0.5:
                st.success("🎉 Interventions are showing positive effects on your mental health!")
            elif mood_improvement > 0 or stress_reduction > 0:
                st.info("📈 Interventions are having a moderate positive effect. Keep it up!")
            else:
                st.warning("💭 Consider trying different intervention strategies or being more consistent.")
    
    else:
        st.info("📋 No intervention data available yet. Start using interventions to track their effectiveness!")
    
    # Planned interventions status
    if planned_interventions:
        st.markdown("#### 📋 Your Action Plan")
        st.write(f"You have {len(planned_interventions)} interventions planned:")
        
        for i, intervention in enumerate(planned_interventions, 1):
            st.markdown(f"{i}. {intervention}")
        
        if st.button("🎯 View Intervention Recommendations"):
            st.switch_page("pages/4_Interventions.py")

# Achievements and milestones
st.markdown("---")
st.subheader("🏆 Achievements & Milestones")

achievements = []

# Check for various achievements
if len(data) >= 7:
    achievements.append("🗓️ **Consistency Champion** - 7+ days of tracking")
if len(data) >= 30:
    achievements.append("📅 **Monthly Milestone** - 30+ days of tracking")

if progress_metrics and progress_metrics.get('mood_improvement', 0) > 1:
    achievements.append("😊 **Mood Booster** - Significant mood improvement")

if progress_metrics and progress_metrics.get('stress_reduction', 0) > 1:
    achievements.append("😌 **Stress Warrior** - Major stress reduction")

if 'sleep_hours' in data.columns:
    good_sleep_rate = ((data['sleep_hours'] >= 7) & (data['sleep_hours'] <= 9)).mean()
    if good_sleep_rate >= 0.7:
        achievements.append("😴 **Sleep Master** - 70%+ optimal sleep")

if 'exercise_minutes' in data.columns:
    exercise_rate = (data['exercise_minutes'] >= 30).mean()
    if exercise_rate >= 0.5:
        achievements.append("💪 **Fitness Enthusiast** - Regular exercise habits")

if achievements:
    for achievement in achievements:
        st.markdown(achievement)
else:
    st.info("Keep tracking your mental health to unlock achievements!")

# Export options
st.markdown("---")
st.subheader("📤 Export Your Data")

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("📊 Download Progress Report", use_container_width=True):
        # Create a summary report
        report_data = {
            'date': data['date'],
            'mood_score': data['mood_score'],
            'stress_level': data['stress_level'],
            'energy_level': data['energy_level'],
            'sleep_hours': data['sleep_hours'],
            'exercise_minutes': data['exercise_minutes']
        }
        report_df = pd.DataFrame(report_data)
        
        csv = report_df.to_csv(index=False)
        st.download_button(
            label="Download CSV",
            data=csv,
            file_name=f"mental_health_progress_{date.today()}.csv",
            mime="text/csv"
        )

with col2:
    if st.button("🏥 Healthcare Provider Summary", use_container_width=True):
        st.info("Healthcare summary prepared for professional consultation.")

with col3:
    if st.button("🔒 Privacy Controls", use_container_width=True):
        st.switch_page("pages/7_Privacy_Settings.py")

# Navigation
st.markdown("---")
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("🏠 Back to Dashboard"):
        st.switch_page("app.py")
with col2:
    if st.button("📝 Daily Check-In"):
        st.switch_page("pages/1_Daily_Check_In.py")
with col3:
    if st.button("🎯 Get Interventions"):
        st.switch_page("pages/4_Interventions.py")
