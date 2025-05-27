import streamlit as st
from supabase import create_client, Client
from config import SUPABASE_URL, SUPABASE_KEY, SESSION_KEY
from utils import show_success, show_error, set_auth_cookie, delete_auth_cookie

def init_supabase() -> Client:
    """Initialize Supabase client."""
    return create_client(SUPABASE_URL, SUPABASE_KEY)

def login_user(email: str, password: str) -> bool:
    """Login user with email and password."""
    if not email or not password:
        show_error("Vui lòng nhập email và mật khẩu")
        return False
    
    try:
        supabase = init_supabase()
        response = supabase.auth.sign_in_with_password({"email": email, "password": password})
        user = response.user
        session = response.session
        
        if user and session:
            st.session_state[SESSION_KEY] = {
                "id": user.id,
                "email": user.email,
                "access_token": session.access_token,
                "refresh_token": session.refresh_token
            }
            set_auth_cookie(session.access_token)
            return True
        else:
            show_error("Đăng nhập thất bại")
            return False
    except Exception as e:
        show_error(f"Lỗi đăng nhập: {str(e)}")
        return False

def register_user(email: str, password: str, confirm_password: str) -> bool:
    """Register a new user."""
    if not email or not password or not confirm_password:
        show_error("Vui lòng điền đầy đủ thông tin")
        return False
    
    if password != confirm_password:
        show_error("Mật khẩu không khớp")
        return False
    
    try:
        supabase = init_supabase()
        response = supabase.auth.sign_up({
            "email": email,
            "password": password
        })
        
        if response.user:
            show_success("Đăng ký thành công! Vui lòng kiểm tra email để xác nhận tài khoản.")
            return True
        else:
            show_error("Đăng ký thất bại")
            return False
    except Exception as e:
        show_error(f"Lỗi đăng ký: {str(e)}")
        return False

def logout_user():
    """Logout current user."""
    if SESSION_KEY in st.session_state:
        del st.session_state[SESSION_KEY]
    delete_auth_cookie()
    
    try:
        supabase = init_supabase()
        supabase.auth.sign_out()
    except Exception:
        pass  # Ignore errors during logout

def is_authenticated():
    """Check if user is authenticated."""
    return SESSION_KEY in st.session_state

def get_current_user():
    """Get current authenticated user."""
    if is_authenticated():
        return st.session_state[SESSION_KEY]
    return None

def show_login_form():
    """Display login form."""
    st.subheader("Đăng nhập")
    with st.form("login_form"):
        email = st.text_input("Email", key="login_email")
        password = st.text_input("Mật khẩu", type="password", key="login_password")
        submit = st.form_submit_button("Đăng nhập")
        
        if submit:
            if login_user(email, password):
                st.experimental_rerun()

def show_register_form():
    """Display registration form."""
    st.subheader("Đăng ký")
    with st.form("register_form"):
        email = st.text_input("Email", key="register_email")
        password = st.text_input("Mật khẩu", type="password", key="register_password")
        confirm_password = st.text_input("Xác nhận mật khẩu", type="password", key="confirm_password")
        submit = st.form_submit_button("Đăng ký")
        
        if submit:
            register_user(email, password, confirm_password)