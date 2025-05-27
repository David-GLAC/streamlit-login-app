import streamlit as st
from auth import get_current_user, logout_user
from supabase import create_client
from config import SUPABASE_URL, SUPABASE_KEY

def init_supabase():
    """Initialize Supabase client."""
    return create_client(SUPABASE_URL, SUPABASE_KEY)

def show_dashboard():
    """Display dashboard content for authenticated users."""
    user = get_current_user()
    
    st.title(f"Xin chào, {user['email']}")
    
    # Thêm menu sidebar
    st.sidebar.title("Menu")
    menu_options = ["Thông tin cá nhân", "Cài đặt", "Quản lý"]
    selected_menu = st.sidebar.selectbox("Chọn chức năng", menu_options)
    
    # Hiển thị nội dung theo lựa chọn menu
    if selected_menu == "Thông tin cá nhân":
        show_profile(user)
    elif selected_menu == "Cài đặt":
        show_settings()
    else:
        show_management()
    
    # Nút đăng xuất ở cuối sidebar
    if st.sidebar.button("Đăng xuất"):
        logout_user()
        st.experimental_rerun()

def show_profile(user):
    """Show user profile information."""
    st.header("Thông tin cá nhân")
    
    try:
        # Lấy thông tin người dùng từ database
        supabase = init_supabase()
        response = supabase.from_('profiles').select('*').eq('id', user['id']).execute()
        profile = response.data[0] if response.data else None
        
        if profile:
            col1, col2 = st.columns(2)
            with col1:
                st.subheader("Thông tin cơ bản")
                st.write(f"Email: {user['email']}")
                st.write(f"Họ tên: {profile.get('full_name', 'Chưa cập nhật')}")
                st.write(f"Số điện thoại: {profile.get('phone', 'Chưa cập nhật')}")
            
            with col2:
                st.subheader("Cập nhật thông tin")
                with st.form("update_profile"):
                    full_name = st.text_input("Họ tên", value=profile.get('full_name', ''))
                    phone = st.text_input("Số điện thoại", value=profile.get('phone', ''))
                    
                    if st.form_submit_button("Cập nhật"):
                        supabase.from_('profiles').update({
                            'full_name': full_name,
                            'phone': phone
                        }).eq('id', user['id']).execute()
                        st.success("Cập nhật thành công!")
                        st.experimental_rerun()
        else:
            st.info("Chưa có thông tin cá nhân. Vui lòng cập nhật!")
            with st.form("create_profile"):
                full_name = st.text_input("Họ tên")
                phone = st.text_input("Số điện thoại")
                
                if st.form_submit_button("Lưu thông tin"):
                    supabase.from_('profiles').insert({
                        'id': user['id'],
                        'full_name': full_name,
                        'phone': phone
                    }).execute()
                    st.success("Lưu thông tin thành công!")
                    st.experimental_rerun()
    except Exception as e:
        st.error(f"Lỗi khi tải thông tin: {str(e)}")

def show_settings():
    """Show user settings."""
    st.header("Cài đặt")
    
    # Đổi mật khẩu
    st.subheader("Đổi mật khẩu")
    with st.form("change_password"):
        current_password = st.text_input("Mật khẩu hiện tại", type="password")
        new_password = st.text_input("Mật khẩu mới", type="password")
        confirm_password = st.text_input("Xác nhận mật khẩu mới", type="password")
        
        if st.form_submit_button("Đổi mật khẩu"):
            if new_password != confirm_password:
                st.error("Mật khẩu mới không khớp!")
            else:
                try:
                    supabase = init_supabase()
                    supabase.auth.update_user({"password": new_password})
                    st.success("Đổi mật khẩu thành công!")
                except Exception as e:
                    st.error(f"Lỗi đổi mật khẩu: {str(e)}")
    
    # Cài đặt thông báo
    st.subheader("Cài đặt thông báo")
    email_notify = st.checkbox("Nhận thông báo qua email", value=True)
    push_notify = st.checkbox("Nhận thông báo đẩy", value=False)
    
    if st.button("Lưu cài đặt thông báo"):
        st.success("Đã lưu cài đặt thông báo!")

def show_management():
    """Show management dashboard."""
    st.header("Quản lý")
    st.info("Đây là phần quản lý. Tính năng đang được phát triển.")
    
    # Placeholder cho các tính năng quản lý
    tab1, tab2, tab3 = st.tabs(["Dự án", "Nhiệm vụ", "Báo cáo"])
    
    with tab1:
        st.subheader("Danh sách dự án")
        st.text("Chức năng quản lý dự án sẽ được hiển thị ở đây.")
    
    with tab2:
        st.subheader("Nhiệm vụ của tôi")
        st.text("Các nhiệm vụ được giao sẽ hiển thị ở đây.")
    
    with tab3:
        st.subheader("Báo cáo & Thống kê")
        st.text("Báo cáo và thống kê sẽ được hiển thị ở đây.")