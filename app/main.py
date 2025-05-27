import streamlit as st
from auth import is_authenticated, show_login_form, show_register_form
from dashboard import show_dashboard
from config import SESSION_KEY
from utils import get_cookie_manager, get_auth_cookie

def main():
    # Thiết lập trang
    st.set_page_config(
        page_title="Hệ thống đăng nhập",
        page_icon="🔐",
        layout="wide"
    )
    
    # Render cookie manager
    cookie_manager = get_cookie_manager()
    cookie_manager.get_all()
    
    # Kiểm tra cookie đăng nhập
    if not is_authenticated() and get_auth_cookie():
        st.warning("Phiên đăng nhập của bạn đã hết hạn. Vui lòng đăng nhập lại.")

    # Hiển thị nội dung tương ứng
    if is_authenticated():
        show_dashboard()
    else:
        st.title("Hệ thống đăng nhập")
        st.write("Chào mừng bạn đến với hệ thống đăng nhập!")
        
        # Tạo hai tab đăng nhập và đăng ký
        tab1, tab2 = st.tabs(["Đăng nhập", "Đăng ký"])
        
        with tab1:
            show_login_form()
        
        with tab2:
            show_register_form()

if __name__ == "__main__":
    main()