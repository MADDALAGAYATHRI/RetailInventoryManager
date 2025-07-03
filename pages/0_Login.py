import streamlit as st
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.auth import AuthManager

def load_css():
    """Load custom CSS styling"""
    with open("styles/theme.css", "r") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

def get_auth_manager():
    """Get cached auth manager instance"""
    if 'auth_manager' not in st.session_state:
        st.session_state.auth_manager = AuthManager()
    return st.session_state.auth_manager

# Load CSS
load_css()

# Initialize auth manager
auth_manager = get_auth_manager()

# Page config
st.set_page_config(
    page_title="MindGuard - Login",
    page_icon="🧠",
    layout="centered"
)

# Check if user is already logged in
if 'user_authenticated' in st.session_state and st.session_state.user_authenticated:
    st.switch_page("app.py")

st.markdown("""
<div style="text-align: center; padding: 2rem 0;">
    <h1 style="color: #2E7D32; font-size: 3rem; margin-bottom: 0.5rem;">🧠 MindGuard</h1>
    <p style="color: #666; font-size: 1.2rem; margin-bottom: 2rem;">Mental Health Monitoring & Support</p>
</div>
""", unsafe_allow_html=True)

# Initialize session state
if 'login_step' not in st.session_state:
    st.session_state.login_step = 'phone'
if 'temp_phone' not in st.session_state:
    st.session_state.temp_phone = ''

col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    # Login form container
    with st.container():
        st.markdown('<div class="form-container">', unsafe_allow_html=True)
        
        if st.session_state.login_step == 'phone':
            st.subheader("🔐 Login to Your Account")
            st.markdown("Enter your phone number to receive a verification code")
            
            with st.form("login_phone_form"):
                col_country, col_phone = st.columns([1, 3])
                
                with col_country:
                    country_code = st.selectbox(
                        "Country",
                        ["+1", "+44", "+91", "+33", "+49", "+81", "+86", "+61", "+55", "+52"],
                        format_func=lambda x: {
                            "+1": "🇺🇸 +1 (US/CA)",
                            "+44": "🇬🇧 +44 (UK)",
                            "+91": "🇮🇳 +91 (India)",
                            "+33": "🇫🇷 +33 (France)",
                            "+49": "🇩🇪 +49 (Germany)",
                            "+81": "🇯🇵 +81 (Japan)",
                            "+86": "🇨🇳 +86 (China)",
                            "+61": "🇦🇺 +61 (Australia)",
                            "+55": "🇧🇷 +55 (Brazil)",
                            "+52": "🇲🇽 +52 (Mexico)"
                        }[x],
                        help="Select your country code"
                    )
                
                with col_phone:
                    phone_number = st.text_input(
                        "Phone Number",
                        placeholder="Enter your phone number",
                        help="Enter your phone number"
                    )
                
                submitted = st.form_submit_button("Send Verification Code", use_container_width=True)
                
                if submitted:
                    if phone_number:
                        # Check if user exists
                        if auth_manager.user_exists(phone_number, country_code):
                            # Send OTP
                            success, message = auth_manager.send_otp(phone_number, country_code)
                            if success:
                                st.session_state.temp_phone = phone_number
                                st.session_state.temp_country_code = country_code
                                st.session_state.login_step = 'otp'
                                st.success("📱 Verification code sent to your phone!")
                                st.rerun()
                            else:
                                st.error(f"❌ Failed to send verification code: {message}")
                        else:
                            st.error("❌ No account found with this phone number. Please sign up first.")
                    else:
                        st.error("❌ Please enter your phone number")
            
            # Link to signup
            st.markdown("---")
            st.markdown(
                '<div style="text-align: center; margin-top: 1rem;">'
                "Don't have an account? "
                '</div>',
                unsafe_allow_html=True
            )
            
            if st.button("Create New Account", use_container_width=True):
                st.switch_page("pages/0_Signup.py")
                
        elif st.session_state.login_step == 'otp':
            st.subheader("📱 Enter Verification Code")
            st.markdown(f"We sent a 6-digit code to **{st.session_state.temp_phone}**")
            
            with st.form("login_otp_form"):
                otp_code = st.text_input(
                    "Verification Code",
                    placeholder="123456",
                    max_chars=6,
                    help="Enter the 6-digit code sent to your phone"
                )
                
                col_verify, col_resend = st.columns(2)
                
                with col_verify:
                    verify_submitted = st.form_submit_button("Verify & Login", use_container_width=True)
                
                with col_resend:
                    resend_submitted = st.form_submit_button("Resend Code", use_container_width=True)
                
                if verify_submitted:
                    if otp_code and len(otp_code) == 6:
                        # Verify OTP
                        success, message = auth_manager.verify_otp(
                            st.session_state.temp_phone, 
                            otp_code,
                            st.session_state.temp_country_code
                        )
                        if success:
                            # Login user
                            login_success, login_message, user_id = auth_manager.login_user(
                                st.session_state.temp_phone,
                                st.session_state.temp_country_code
                            )
                            if login_success:
                                # Set session state
                                st.session_state.user_authenticated = True
                                st.session_state.user_id = user_id
                                st.session_state.user_phone = st.session_state.temp_phone
                                
                                # Get user data
                                user_data = auth_manager.get_user(
                                    st.session_state.temp_phone,
                                    st.session_state.temp_country_code
                                )
                                if user_data:
                                    st.session_state.user_name = user_data.get('name', 'User')
                                
                                # Clean up temp data
                                del st.session_state.temp_phone
                                del st.session_state.login_step
                                
                                st.success("✅ Login successful! Redirecting...")
                                st.rerun()
                            else:
                                st.error(f"❌ Login failed: {login_message}")
                        else:
                            st.error(f"❌ {message}")
                    else:
                        st.error("❌ Please enter a valid 6-digit code")
                
                if resend_submitted:
                    success, message = auth_manager.send_otp(
                        st.session_state.temp_phone,
                        st.session_state.temp_country_code
                    )
                    if success:
                        st.success("📱 New verification code sent!")
                    else:
                        st.error(f"❌ Failed to resend code: {message}")
            
            # Back to phone entry
            if st.button("← Change Phone Number"):
                st.session_state.login_step = 'phone'
                st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown(
    '<div style="text-align: center; color: #666; padding: 1rem;">'
    '<small>🔒 Your privacy is our priority. All data is stored locally and encrypted.</small>'
    '</div>',
    unsafe_allow_html=True
)