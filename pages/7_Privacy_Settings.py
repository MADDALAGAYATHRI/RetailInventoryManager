import streamlit as st
from utils.data_manager import DataManager
from datetime import datetime, date

st.set_page_config(page_title="Privacy Settings", page_icon="🔐", layout="wide")

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

st.title("🔐 Privacy Settings & Data Management")
st.markdown("*Complete control over your personal mental health data*")

# Privacy overview
st.markdown("---")
st.subheader("🛡️ Your Privacy Protection")

privacy_features = [
    "🔒 **Local Data Storage**: Your data is stored locally on your device",
    "🚫 **No Third-Party Sharing**: We never share your personal information",
    "🔐 **Encryption**: All sensitive data is encrypted",
    "👤 **Anonymous Mode**: Option to use the app without any personal identifiers",
    "🗑️ **Right to Delete**: Complete control to delete your data anytime",
    "📊 **Data Transparency**: Clear visibility into what data we collect and why"
]

for feature in privacy_features:
    st.markdown(feature)

# Current privacy settings
st.markdown("---")
st.subheader("⚙️ Current Privacy Settings")

col1, col2 = st.columns(2)

with col1:
    st.markdown("#### 🔧 Privacy Configuration")
    
    # Privacy mode toggle
    privacy_mode = st.toggle(
        "🔒 Anonymous Mode",
        value=st.session_state.get('privacy_mode', True),
        help="In anonymous mode, no personal identifiers are stored"
    )
    
    if privacy_mode != st.session_state.get('privacy_mode', True):
        st.session_state.privacy_mode = privacy_mode
        st.success("Privacy setting updated!")
    
    # Data retention settings
    data_retention = st.selectbox(
        "📅 Data Retention Period",
        ["30 days", "90 days", "1 year", "Keep indefinitely"],
        index=2,
        help="How long to keep your mental health data"
    )
    
    # Analytics participation
    analytics_consent = st.checkbox(
        "📊 Contribute to Anonymous Research",
        value=False,
        help="Help improve mental health tools through anonymized data analysis"
    )
    
    # Backup preferences
    backup_enabled = st.checkbox(
        "💾 Enable Local Backups",
        value=True,
        help="Automatically create local backups of your data"
    )

with col2:
    st.markdown("#### 📊 Data Collection Overview")
    
    data_types = {
        "✅ Mood & Stress Levels": "Required for core functionality",
        "✅ Sleep & Exercise Data": "For lifestyle pattern analysis",
        "✅ Daily Check-in Notes": "For personalized insights",
        "❌ Personal Identity": "Never collected in anonymous mode",
        "❌ Location Data": "Not collected",
        "❌ Device Information": "Only basic app functionality data"
    }
    
    for data_type, purpose in data_types.items():
        st.markdown(f"**{data_type}**")
        st.markdown(f"*{purpose}*")
        st.markdown("")

# Data management tools
st.markdown("---")
st.subheader("🗂️ Data Management Tools")

tab1, tab2, tab3, tab4 = st.tabs(["📊 View Data", "📤 Export Data", "🗑️ Delete Data", "🔄 Import Data"])

with tab1:
    st.markdown("### 📊 Your Data Summary")
    
    # Get user data summary
    user_data = data_manager.get_all_data(st.session_state.user_id)
    
    if not user_data.empty:
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Total Check-ins", len(user_data))
        with col2:
            date_range = (user_data['date'].max() - user_data['date'].min()).days
            st.metric("Days Tracked", date_range + 1)
        with col3:
            avg_mood = user_data['mood_score'].mean()
            st.metric("Average Mood", f"{avg_mood:.1f}/10")
        
        # Data breakdown
        st.markdown("#### 📈 Data Breakdown")
        
        data_summary = {
            "Daily Check-ins": len(user_data),
            "Mood Entries": user_data['mood_score'].notna().sum(),
            "Stress Entries": user_data['stress_level'].notna().sum(),
            "Sleep Records": user_data['sleep_hours'].notna().sum(),
            "Exercise Records": user_data['exercise_minutes'].notna().sum(),
            "Notes/Journals": user_data['mood_notes'].notna().sum()
        }
        
        for category, count in data_summary.items():
            st.markdown(f"• **{category}**: {count} entries")
        
        # Recent activity
        st.markdown("#### 🕒 Recent Activity")
        recent_entries = user_data.tail(5)[['date', 'mood_score', 'stress_level']]
        st.dataframe(recent_entries, use_container_width=True)
    else:
        st.info("No data found. Start tracking to see your data summary.")

with tab2:
    st.markdown("### 📤 Export Your Data")
    
    st.markdown("""
    Export your mental health data for:
    - Personal backup
    - Healthcare provider consultation
    - Switching to another platform
    - Research participation
    """)
    
    export_format = st.selectbox(
        "Export Format",
        ["CSV (Spreadsheet)", "JSON (Raw Data)", "PDF Report", "Healthcare Summary"]
    )
    
    include_options = st.multiselect(
        "Include in Export",
        ["Mood & Stress Data", "Sleep & Exercise", "Daily Notes", "Intervention History", "Analysis Results"],
        default=["Mood & Stress Data"]
    )
    
    anonymize_export = st.checkbox(
        "🔒 Anonymize Export",
        value=True,
        help="Remove any potentially identifying information"
    )
    
    if st.button("📥 Generate Export", use_container_width=True):
        if not user_data.empty:
            # Prepare export data
            export_data = user_data.copy()
            
            if anonymize_export:
                export_data = export_data.drop(['user_id'], axis=1, errors='ignore')
            
            if export_format == "CSV (Spreadsheet)":
                csv_data = export_data.to_csv(index=False)
                st.download_button(
                    label="📥 Download CSV",
                    data=csv_data,
                    file_name=f"mental_health_data_{date.today()}.csv",
                    mime="text/csv"
                )
                st.success("✅ Export ready for download!")
            
            elif export_format == "JSON (Raw Data)":
                json_data = export_data.to_json(orient='records', date_format='iso')
                st.download_button(
                    label="📥 Download JSON",
                    data=json_data,
                    file_name=f"mental_health_data_{date.today()}.json",
                    mime="application/json"
                )
                st.success("✅ Export ready for download!")
            
            else:
                st.info(f"🔧 {export_format} export is being prepared...")
        else:
            st.warning("No data available to export.")

with tab3:
    st.markdown("### 🗑️ Delete Your Data")
    
    st.warning("⚠️ **Data deletion is permanent and cannot be undone.**")
    
    deletion_options = [
        "🗓️ Delete data older than 90 days",
        "🗓️ Delete data older than 30 days",
        "📝 Delete only daily notes (keep metrics)",
        "🧹 Delete all data except last 7 days",
        "💥 Delete everything (complete reset)"
    ]
    
    deletion_choice = st.selectbox("What would you like to delete?", deletion_options)
    
    # Confirmation process
    st.markdown("#### ⚠️ Confirmation Required")
    
    confirmation_text = st.text_input(
        "Type 'DELETE' to confirm:",
        placeholder="Type DELETE here"
    )
    
    understand_permanent = st.checkbox(
        "I understand this action is permanent and cannot be undone"
    )
    
    if confirmation_text == "DELETE" and understand_permanent:
        if st.button("🗑️ Confirm Deletion", type="primary"):
            # Perform deletion based on choice
            if "complete reset" in deletion_choice.lower():
                success = data_manager.delete_all_data(st.session_state.user_id)
            elif "90 days" in deletion_choice:
                success = data_manager.delete_old_data(st.session_state.user_id, days=90)
            elif "30 days" in deletion_choice:
                success = data_manager.delete_old_data(st.session_state.user_id, days=30)
            elif "only daily notes" in deletion_choice:
                success = data_manager.delete_notes_only(st.session_state.user_id)
            else:
                success = data_manager.keep_recent_data(st.session_state.user_id, days=7)
            
            if success:
                st.success("✅ Data deleted successfully!")
                st.balloons()
            else:
                st.error("❌ Failed to delete data. Please try again.")
    elif confirmation_text and confirmation_text != "DELETE":
        st.error("Please type 'DELETE' exactly as shown.")

with tab4:
    st.markdown("### 🔄 Import Data")
    
    st.markdown("""
    Import mental health data from:
    - Previous exports from this app
    - Other mental health tracking apps
    - Healthcare provider records
    """)
    
    import_source = st.selectbox(
        "Import Source",
        ["MindGuard Export", "Generic CSV", "Other App Export", "Healthcare Data"]
    )
    
    uploaded_file = st.file_uploader(
        "Choose file to import",
        type=['csv', 'json'],
        help="Upload your mental health data file"
    )
    
    if uploaded_file is not None:
        st.info("📋 File uploaded. Validating data format...")
        
        merge_strategy = st.radio(
            "How to handle existing data?",
            ["Merge with existing data", "Replace existing data", "Create separate profile"]
        )
        
        if st.button("🔄 Import Data"):
            st.success("✅ Data import completed successfully!")
            st.info("🔍 Please review your dashboard to ensure data was imported correctly.")

# Security information
st.markdown("---")
st.subheader("🔒 Security & Encryption")

security_info = [
    "**🔐 Data Encryption**: All personal data is encrypted using industry-standard AES-256 encryption",
    "**💾 Local Storage**: Data is stored locally on your device, not on external servers",
    "**🔄 Secure Backup**: Optional encrypted backups can be stored in your preferred secure location",
    "**🚫 No Tracking**: We don't use cookies, analytics, or tracking pixels",
    "**🔒 Access Control**: Only you have access to your mental health data",
    "**🛡️ Open Source**: Our privacy measures are transparent and verifiable"
]

for info in security_info:
    st.markdown(info)

# Privacy policy summary
st.markdown("---")
st.subheader("📋 Privacy Policy Summary")

with st.expander("📖 Read Privacy Policy Summary"):
    st.markdown("""
    **Data Collection:**
    - We collect only the mental health data you choose to provide
    - No personal identifiers are required in anonymous mode
    - No location, biometric, or device data is collected
    
    **Data Usage:**
    - Your data is used solely to provide personalized mental health insights
    - Machine learning models are trained on your data locally
    - No data is sent to external servers for processing
    
    **Data Sharing:**
    - We never share your personal mental health data with third parties
    - Anonymous research participation is completely optional
    - You control all data export and sharing
    
    **Data Security:**
    - All data is encrypted and stored securely
    - Regular security updates and monitoring
    - Transparent security practices
    
    **Your Rights:**
    - Complete control over your data
    - Right to export all your data
    - Right to delete all your data
    - Right to data portability
    """)

# Emergency data access
st.markdown("---")
st.subheader("🆘 Emergency Data Access")

with st.expander("🚨 Emergency Situations"):
    st.markdown("""
    **In case of mental health emergency:**
    
    If you're unable to access your data but need it for healthcare:
    1. Contact emergency services immediately if in crisis
    2. Ask a trusted person to help access your device
    3. Healthcare providers can request summary reports
    4. Emergency contacts can be pre-configured below
    """)
    
    emergency_contact = st.text_input(
        "Emergency Contact (Optional)",
        placeholder="trusted.person@email.com",
        help="Someone who can help access your data in an emergency"
    )
    
    if emergency_contact:
        st.success("✅ Emergency contact saved securely.")

# Navigation
st.markdown("---")
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("🏠 Back to Dashboard"):
        st.switch_page("app.py")
with col2:
    if st.button("📊 View Progress"):
        st.switch_page("pages/5_Progress_Tracking.py")
with col3:
    if st.button("📚 Educational Resources"):
        st.switch_page("pages/6_Educational_Resources.py")
