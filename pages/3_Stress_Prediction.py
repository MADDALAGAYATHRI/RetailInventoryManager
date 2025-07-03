import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta, date
from utils.data_manager import DataManager
from utils.ml_models import StressPredictor



st.set_page_config(page_title="Stress Prediction", page_icon="🔮", layout="wide")

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
def get_stress_predictor():
    return StressPredictor()

data_manager = get_data_manager()
stress_predictor = get_stress_predictor()

st.title("🔮 AI-Powered Stress Prediction")
st.markdown("*Early detection and intervention recommendations based on your patterns*")

# Ensure user session is properly initialized
if 'user_id' not in st.session_state:
    st.session_state.user_id = st.session_state.get('user_id', 'anonymous_user')

# Get historical data
historical_data = data_manager.get_recent_data(st.session_state.user_id, days=90)

if len(historical_data) < 7:
    st.warning("📊 We need at least 7 days of data to make accurate predictions. Please complete more daily check-ins.")
    if st.button("Complete Daily Check-In"):
        st.switch_page("pages/1_Daily_Check_In.py")
    st.stop()

# Train model with historical data
with st.spinner("🤖 Training AI model with your data..."):
    model_trained = stress_predictor.train_model(historical_data)

if not model_trained:
    st.error("❌ Unable to train prediction model. Please ensure you have sufficient data variance.")
    st.stop()

# Current status assessment
st.markdown("---")
st.subheader("📊 Current Stress Assessment")

# Get latest entry
latest_entry = historical_data.iloc[-1]
current_stress = latest_entry['stress_level']

# Predict stress for today based on latest patterns
current_features = stress_predictor.prepare_features(latest_entry)
predicted_stress = stress_predictor.predict_stress(current_features)

col1, col2, col3 = st.columns(3)

with col1:
    # Current stress level
    stress_color = "#FF4D4F" if current_stress >= 7 else "#FAAD14" if current_stress >= 5 else "#52C41A"
    st.markdown(f"""
    <div style="text-align: center; padding: 20px; border-radius: 10px; background-color: {stress_color}20;">
        <h3 style="color: {stress_color};">Current Stress</h3>
        <h1 style="color: {stress_color}; margin: 0;">{current_stress}/10</h1>
    </div>
    """, unsafe_allow_html=True)

with col2:
    # Predicted stress trend
    pred_color = "#FF4D4F" if predicted_stress >= 7 else "#FAAD14" if predicted_stress >= 5 else "#52C41A"
    trend_arrow = "📈" if predicted_stress > current_stress else "📉" if predicted_stress < current_stress else "➡️"
    st.markdown(f"""
    <div style="text-align: center; padding: 20px; border-radius: 10px; background-color: {pred_color}20;">
        <h3 style="color: {pred_color};">Predicted Trend</h3>
        <h1 style="color: {pred_color}; margin: 0;">{trend_arrow} {predicted_stress:.1f}/10</h1>
    </div>
    """, unsafe_allow_html=True)

with col3:
    # Risk level
    risk_level = "HIGH" if predicted_stress >= 7 else "MODERATE" if predicted_stress >= 5 else "LOW"
    risk_color = "#FF4D4F" if risk_level == "HIGH" else "#FAAD14" if risk_level == "MODERATE" else "#52C41A"
    st.markdown(f"""
    <div style="text-align: center; padding: 20px; border-radius: 10px; background-color: {risk_color}20;">
        <h3 style="color: {risk_color};">Risk Level</h3>
        <h1 style="color: {risk_color}; margin: 0;">{risk_level}</h1>
    </div>
    """, unsafe_allow_html=True)

# Stress prediction for next 7 days
st.markdown("---")
st.subheader("📈 7-Day Stress Forecast")

# Generate predictions for next 7 days
future_dates = [date.today() + timedelta(days=i) for i in range(1, 8)]
future_predictions = []

# Use rolling averages and trends for future predictions
recent_avg = historical_data.tail(7).mean()

for i, future_date in enumerate(future_dates):
    # Simulate future features based on recent patterns with some variation
    future_features = {
        'sleep_hours': recent_avg['sleep_hours'] + np.random.normal(0, 0.5),
        'exercise_minutes': recent_avg['exercise_minutes'] + np.random.normal(0, 10),
        'work_hours': recent_avg['work_hours'] + np.random.normal(0, 1),
        'caffeine_intake': recent_avg['caffeine_intake'] + np.random.normal(0, 0.5),
        'alcohol_intake': recent_avg['alcohol_intake'] + np.random.normal(0, 0.3),
        'meditation_minutes': recent_avg['meditation_minutes'] + np.random.normal(0, 5),
        'mood_score': recent_avg['mood_score'] + np.random.normal(0, 0.5),
        'energy_level': recent_avg['energy_level'] + np.random.normal(0, 0.5)
    }
    
    pred_features = stress_predictor.prepare_features(pd.Series(future_features))
    pred_stress = stress_predictor.predict_stress(pred_features)
    future_predictions.append(pred_stress)

# Create forecast visualization
fig = go.Figure()

# Historical data
fig.add_trace(go.Scatter(
    x=historical_data['date'].tail(14),
    y=historical_data['stress_level'].tail(14),
    mode='lines+markers',
    name='Historical Stress',
    line=dict(color='#1890FF', width=3),
    marker=dict(size=8)
))

# Future predictions
fig.add_trace(go.Scatter(
    x=future_dates,
    y=future_predictions,
    mode='lines+markers',
    name='Predicted Stress',
    line=dict(color='#FF7875', width=3, dash='dash'),
    marker=dict(size=8, symbol='diamond')
))

# Add stress level zones
fig.add_hrect(y0=0, y1=3, fillcolor="green", opacity=0.1, annotation_text="Low Stress Zone")
fig.add_hrect(y0=3, y1=7, fillcolor="yellow", opacity=0.1, annotation_text="Moderate Stress Zone")
fig.add_hrect(y0=7, y1=10, fillcolor="red", opacity=0.1, annotation_text="High Stress Zone")

fig.update_layout(
    title="Stress Level Forecast",
    xaxis_title="Date",
    yaxis_title="Stress Level (1-10)",
    hovermode='x unified',
    height=500,
    yaxis=dict(range=[0, 10])
)

st.plotly_chart(fig, use_container_width=True)

# Key factors analysis
st.markdown("---")
st.subheader("🔍 Key Stress Factors")

# Get feature importance
feature_importance = stress_predictor.get_feature_importance()

if feature_importance:
    col1, col2 = st.columns(2)
    
    with col1:
        # Feature importance chart
        factors = list(feature_importance.keys())
        importance = list(feature_importance.values())
        
        fig_importance = px.bar(
            x=importance, y=factors,
            orientation='h',
            title="Factors Most Predictive of Your Stress",
            labels={'x': 'Importance Score', 'y': 'Lifestyle Factors'},
            color=importance,
            color_continuous_scale='RdYlGn_r'
        )
        fig_importance.update_layout(height=400, showlegend=False)
        st.plotly_chart(fig_importance, use_container_width=True)
    
    with col2:
        st.markdown("#### 💡 Factor Insights")
        
        # Analyze top factors
        top_factors = sorted(feature_importance.items(), key=lambda x: x[1], reverse=True)[:3]
        
        for factor, importance in top_factors:
            if importance > 0.15:  # Significant factor
                factor_name = factor.replace('_', ' ').title()
                st.markdown(f"**{factor_name}** (Impact: {importance:.1%})")
                
                # Get recent trend for this factor
                recent_values = historical_data[factor].tail(7).values
                if len(recent_values) > 1:
                    trend = "increasing" if recent_values[-1] > recent_values[0] else "decreasing"
                    avg_val = np.mean(recent_values)
                    
                    if factor == 'sleep_hours':
                        if avg_val < 7:
                            st.markdown(f"   • Your {factor_name.lower()} is {trend} (avg: {avg_val:.1f}h). Aim for 7-9 hours.")
                        else:
                            st.markdown(f"   • Good {factor_name.lower()} pattern (avg: {avg_val:.1f}h).")
                    elif factor == 'work_hours':
                        if avg_val > 9:
                            st.markdown(f"   • Long work hours detected (avg: {avg_val:.1f}h). Consider work-life balance.")
                        else:
                            st.markdown(f"   • Reasonable work hours (avg: {avg_val:.1f}h).")
                    elif factor == 'exercise_minutes':
                        if avg_val < 30:
                            st.markdown(f"   • Low exercise levels (avg: {avg_val:.0f} min). Increase physical activity.")
                        else:
                            st.markdown(f"   • Good exercise routine (avg: {avg_val:.0f} min/day).")
                    else:
                        st.markdown(f"   • Current pattern: {trend} (avg: {avg_val:.1f})")

# Early warning system
st.markdown("---")
st.subheader("⚠️ Early Warning System")

warnings = []
recommendations = []

# Check for high-risk patterns
if max(future_predictions) >= 8:
    warnings.append("🚨 **High Stress Alert**: Predicted stress levels may reach critical levels in the coming days.")
    recommendations.append("Consider scheduling stress management activities and reduce non-essential commitments.")

if predicted_stress > current_stress + 1.5:
    warnings.append("📈 **Rising Stress Trend**: Your stress levels are predicted to increase significantly.")
    recommendations.append("Implement preventive measures now to avoid stress escalation.")

# Check recent patterns
recent_data = historical_data.tail(3)
if (recent_data['stress_level'] >= 6).all():
    warnings.append("🔄 **Persistent High Stress**: You've had elevated stress for multiple consecutive days.")
    recommendations.append("Consider professional support or intensive stress management techniques.")

if recent_data['sleep_hours'].mean() < 6:
    warnings.append("😴 **Sleep Deprivation Risk**: Poor sleep may be contributing to stress vulnerability.")
    recommendations.append("Prioritize sleep hygiene and aim for 7-9 hours per night.")

# Display warnings and recommendations
if warnings:
    st.markdown("#### ⚠️ Alerts")
    for warning in warnings:
        st.warning(warning)
    
    st.markdown("#### 💡 Recommended Actions")
    for rec in recommendations:
        st.markdown(f"• {rec}")
else:
    st.success("✅ No immediate stress risks detected. Your patterns look healthy!")

# Intervention suggestions
if predicted_stress >= 6 or max(future_predictions) >= 7:
    st.markdown("---")
    st.info("🎯 **Proactive Intervention Recommended**: Based on your stress predictions, consider implementing stress management strategies now.")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🎯 Get Personalized Interventions", use_container_width=True):
            st.switch_page("pages/4_Interventions.py")
    with col2:
        if st.button("📚 Learn Coping Strategies", use_container_width=True):
            st.switch_page("pages/6_Educational_Resources.py")

# Navigation
st.markdown("---")
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("🏠 Back to Dashboard"):
        st.switch_page("app.py")
with col2:
    if st.button("📊 Lifestyle Analysis"):
        st.switch_page("pages/2_Lifestyle_Analysis.py")
with col3:
    if st.button("📈 Progress Tracking"):
        st.switch_page("pages/5_Progress_Tracking.py")
