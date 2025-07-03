import streamlit as st

def check_authentication():
    """Check if user is authenticated, redirect to login if not"""
    if 'user_authenticated' not in st.session_state or not st.session_state.user_authenticated:
        st.switch_page("pages/0_Login.py")
        return False
    return True

def ensure_user_session():
    """Ensure user session state is properly initialized"""
    if 'user_id' not in st.session_state:
        if 'user_authenticated' in st.session_state and st.session_state.user_authenticated:
            # User is authenticated but user_id is missing
            st.session_state.user_id = st.session_state.get('user_id', 'anonymous_user')
        else:
            # Not authenticated, redirect to login
            st.switch_page("pages/0_Login.py")
            st.stop()