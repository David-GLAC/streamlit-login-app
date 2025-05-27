import streamlit as st
from datetime import datetime, timedelta
import extra_streamlit_components as stx

def get_cookie_manager():
    """Get or create a cookie manager."""
    if "cookie_manager" not in st.session_state:
        st.session_state.cookie_manager = stx.CookieManager()
    return st.session_state.cookie_manager

def set_auth_cookie(token, expiry_days=7):
    """Set authentication cookie."""
    cookie_manager = get_cookie_manager()
    expiry = datetime.now() + timedelta(days=expiry_days)
    cookie_manager.set("auth_token", token, expires_at=expiry)

def get_auth_cookie():
    """Get authentication cookie."""
    cookie_manager = get_cookie_manager()
    return cookie_manager.get("auth_token")

def delete_auth_cookie():
    """Delete authentication cookie."""
    cookie_manager = get_cookie_manager()
    cookie_manager.delete("auth_token")

def show_success(message):
    """Show success message."""
    st.success(message)

def show_error(message):
    """Show error message."""
    st.error(message)

def show_info(message):
    """Show info message."""
    st.info(message)