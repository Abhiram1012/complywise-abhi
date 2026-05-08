import streamlit as st
import base64
import random
import time

# ---------------------------------------------------------
# 1. PAGE CONFIGURATION
# ---------------------------------------------------------
st.set_page_config(
    layout="wide",
    page_title="ComplyWise | Secure Login",
    page_icon="🔒"
)

# ---------------------------------------------------------
# 2. SESSION INITIALIZATION
# ---------------------------------------------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "view" not in st.session_state:
    st.session_state.view = "login"
if "reset_step" not in st.session_state:
    st.session_state.reset_step = "verify_user"
if "otp_code" not in st.session_state:
    st.session_state.otp_code = None
if "target_user" not in st.session_state:
    st.session_state.target_user = None

# ---------------------------------------------------------
# 3. ASSETS (IMAGE CONVERSION)
# ---------------------------------------------------------
def get_base64_of_bin_file(bin_file):
    try:
        with open(bin_file, 'rb') as f:
            return base64.b64encode(f.read()).decode()
    except: return ""

# ---------------------------------------------------------
# 4. UI: LOGIN & FORGOT PASSWORD
# ---------------------------------------------------------
def show_login_page():
    logo_base64 = get_base64_of_bin_file("comply logo.jpg")

    st.markdown(f"""
        <style>
        [data-testid="stHeader"] {{ visibility: hidden; display: none !important; }}
        .block-container {{ padding-top: 2rem !important; }}
        .stApp {{ background-color: #f4f7f9; }}
        
        .login-card {{
            background-color: white;
            padding: 40px;
            border-radius: 15px;
            border: 1px solid #e0e6ed;
            box-shadow: 0px 10px 25px rgba(0,0,0,0.05);
        }}
        .custom-logo {{ width: 280px; margin-bottom: 25px; display: block; }}
        
        .blue-panel {{
            background-color: #004a99;
            background-image: linear-gradient(160deg, #004a99 0%, #002d5c 100%);
            padding: 60px 50px;
            border-radius: 20px;
            color: white;
            min-height: 520px;
            display: flex;
            flex-direction: column;
            justify-content: center;
        }}
        </style>
    """, unsafe_allow_html=True)

    col_left, col_right = st.columns([1, 1.2], gap="large")

    with col_left:
        st.markdown(f'''<div class="login-card"><img src="data:image/jpeg;base64,{logo_base64}" class="custom-logo">''', unsafe_allow_html=True)

        # --- VIEW: LOGIN ---
        if st.session_state.view == "login":
            st.subheader("Sign In")
            u_id = st.text_input("User ID", placeholder="Enter Username")
            u_pass = st.text_input("Password", type="password", placeholder="Enter Password")

            c1, c2 = st.columns([1.5, 1])
            with c2:
                if st.button("Forgot Password?", key="fg_btn"):
                    st.session_state.view = "forgot"
                    st.session_state.reset_step = "verify_user"
                    st.rerun()

            if st.button("Sign In", type="primary", use_container_width=True):
                # Replace with Snowflake Query: SELECT * FROM COMPLYWISE_USERS WHERE USERID=%s AND PASSWORD=%s
                if u_id == "admin" and u_pass == "admin123":
                    st.session_state.logged_in = True
                    st.rerun()
                else:
                    st.error("Invalid credentials")

        # --- VIEW: FORGOT PASSWORD ---
        elif st.session_state.view == "forgot":
            st.subheader("Reset Password")
            
            # STEP 1: Verify User ID
            if st.session_state.reset_step == "verify_user":
                target = st.text_input("Enter your User ID to receive OTP")
                if st.button("Send OTP", type="primary", use_container_width=True):
                    # Simulate DB Check: if user in Snowflake...
                    st.session_state.otp_code = str(random.randint(1000, 9999))
                    st.session_state.target_user = target
                    st.session_state.reset_step = "enter_otp"
                    st.toast(f"OTP Sent! (Debug: {st.session_state.otp_code})")
                    st.rerun()

            # STEP 2: Enter OTP
            elif st.session_state.reset_step == "enter_otp":
                st.write(f"OTP sent for user: **{st.session_state.target_user}**")
                otp_in = st.text_input("Enter 4-Digit OTP")
                if st.button("Verify OTP", type="primary", use_container_width=True):
                    if otp_in == st.session_state.otp_code:
                        st.session_state.reset_step = "new_password"
                        st.rerun()
                    else:
                        st.error("Incorrect OTP")

            # STEP 3: Change Password
            elif st.session_state.reset_step == "new_password":
                new_p = st.text_input("New Password", type="password")
                conf_p = st.text_input("Confirm Password", type="password")
                if st.button("Update Password", type="primary", use_container_width=True):
                    if new_p == conf_p:
                        # Update Snowflake: UPDATE COMPLYWISE_USERS SET PASSWORD=%s WHERE USERID=%s
                        st.success("Password Updated Successfully!")
                        time.sleep(1)
                        st.session_state.view = "login"
                        st.rerun()
                    else:
                        st.error("Passwords do not match")

            if st.button("← Back to Login"):
                st.session_state.view = "login"
                st.rerun()

        st.markdown('</div>', unsafe_allow_html=True)

    with col_right:
        st.markdown('<div class="blue-panel"><h1>ComplyWise Integrity</h1><p>Continuous data validation and risk prevention.</p></div>', unsafe_allow_html=True)

# ---------------------------------------------------------
# 5. EXECUTION
# ---------------------------------------------------------
if not st.session_state.logged_in:
    show_login_page()
else:
    st.title("Main Dashboard")
    if st.button("Log Out"):
        st.session_state.logged_in = False
        st.rerun()
