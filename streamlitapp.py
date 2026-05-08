import streamlit as st
import base64
import random
import time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

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
def get_snowflake_session():
    try:
        from snowflake.snowpark.context import get_active_session
        return get_active_session()
    except:
        return st.connection("snowflake").session()

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "view" not in st.session_state:
    st.session_state.view = "login"
if "reset_step" not in st.session_state:
    st.session_state.reset_step = "verify_user"
if "otp_code" not in st.session_state:
    st.session_state.otp_code = None
if "target_email" not in st.session_state:
    st.session_state.target_email = None

# ---------------------------------------------------------
# 3. HELPER FUNCTIONS
# ---------------------------------------------------------
def get_base64_of_bin_file(bin_file):
    try:
        with open(bin_file, 'rb') as f:
            return base64.b64encode(f.read()).decode()
    except: 
        return ""

def send_external_email(target_email, otp_code):
    """Sends email via SMTP to any recipient (non-Snowflake users)."""
    try:
        # These must be set in your Streamlit Secrets
        smtp_user = st.secrets["email"]["smtp_user"]
        smtp_pass = st.secrets["email"]["smtp_pass"]
        smtp_server = "smtp.gmail.com"  # Use smtp.office365.com for Outlook
        smtp_port = 465 

        msg = MIMEMultipart()
        msg["From"] = f"ComplyWise Security <{smtp_user}>"
        msg["To"] = target_email
        msg["Subject"] = "Your ComplyWise Verification Code"

        body = f"""
        <html>
            <body>
                <h3>ComplyWise Password Reset</h3>
                <p>Your verification code is: <b style='font-size: 20px; color: #004a99;'>{otp_code}</b></p>
                <p>This code is valid for 10 minutes. If you did not request this, please ignore this email.</p>
            </body>
        </html>
        """
        msg.attach(MIMEText(body, "html"))

        with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
            server.login(smtp_user, smtp_pass)
            server.send_message(msg)
        return True
    except Exception as e:
        st.error(f"Email Error: {e}")
        return False

# ---------------------------------------------------------
# 4. UI: LOGIN PAGE
# ---------------------------------------------------------
def show_login_page():
    logo_base64 = get_base64_of_bin_file("comply logo.jpg")

    st.markdown(f"""
        <style>
        [data-testid="stHeader"] {{ visibility: hidden; display: none !important; }}
        .block-container {{ padding-top: 2rem !important; }}
        .stApp {{ background-color: #f4f7f9; }}
        .login-card {{
            background-color: white; padding: 40px; border-radius: 15px;
            border: 1px solid #e0e6ed; box-shadow: 0px 10px 25px rgba(0,0,0,0.05);
        }}
        .custom-logo {{ width: 280px; margin-bottom: 25px; display: block; }}
        .blue-panel {{
            background-color: #004a99; background-image: linear-gradient(160deg, #004a99 0%, #002d5c 100%);
            padding: 60px 50px; border-radius: 20px; color: white; min-height: 520px;
            display: flex; flex-direction: column; justify-content: center;
        }}
        </style>
    """, unsafe_allow_html=True)

    col_left, col_right = st.columns([1, 1.2], gap="large")

    with col_left:
        st.markdown(f'''<div class="login-card"><img src="data:image/jpeg;base64,{logo_base64}" class="custom-logo">''', unsafe_allow_html=True)

        if st.session_state.view == "login":
            st.subheader("Sign In")
            u_input = st.text_input("User ID or Email", placeholder="Enter ID or Email")
            u_pass = st.text_input("Password", type="password", placeholder="Enter Password")

            c1, c2 = st.columns([1.5, 1])
            with c2:
                if st.button("Forgot Password?", key="fg_btn"):
                    st.session_state.view = "forgot"
                    st.session_state.reset_step = "verify_user"
                    st.rerun()

            if st.button("Sign In", type="primary", use_container_width=True):
                session = get_snowflake_session()
                # Use parameterized query or basic cleaning to prevent SQL issues
                clean_uid = u_input.strip().replace("'", "''")
                user_record = session.sql(f"""
                    SELECT * FROM ML_DATASETS.DATA.COMPLYWISE_USERS 
                    WHERE (USERID = '{clean_uid}' OR EMAIL = '{clean_uid}') 
                    AND PASSWORD = '{u_pass.replace("'", "''")}'
                """).collect()

                if len(user_record) > 0:
                    st.session_state.logged_in = True
                    st.rerun()
                else:
                    st.error("Invalid credentials")

        elif st.session_state.view == "forgot":
            st.subheader("Reset Password")
            
            if st.session_state.reset_step == "verify_user":
                email_target = st.text_input("Enter Registered Email", placeholder="email@example.com")
                if st.button("Send OTP", type="primary", use_container_width=True):
                    session = get_snowflake_session()
                    exists = session.sql(f"SELECT 1 FROM ML_DATASETS.DATA.COMPLYWISE_USERS WHERE EMAIL = '{email_target.strip().replace("'", "''")}'").collect()
                    
                    if len(exists) > 0:
                        otp = str(random.randint(1000, 9999))
                        st.session_state.otp_code = otp
                        st.session_state.target_email = email_target
                        with st.spinner("Sending OTP..."):
                            if send_external_email(email_target, otp):
                                st.session_state.reset_step = "enter_otp"
                                st.rerun()
                    else:
                        st.error("Email not found in database")

            elif st.session_state.reset_step == "enter_otp":
                st.write(f"OTP sent to: **{st.session_state.target_email}**")
                otp_in = st.text_input("Enter 4-Digit OTP", placeholder="0000")
                if st.button("Verify OTP", type="primary", use_container_width=True):
                    if otp_in == st.session_state.otp_code:
                        st.session_state.reset_step = "new_password"
                        st.rerun()
                    else:
                        st.error("Incorrect OTP")

            elif st.session_state.reset_step == "new_password":
                new_p = st.text_input("New Password", type="password")
                conf_p = st.text_input("Confirm Password", type="password")
                if st.button("Update Password", type="primary", use_container_width=True):
                    if new_p == conf_p and new_p != "":
                        session = get_snowflake_session()
                        session.sql(f"""
                            UPDATE ML_DATASETS.DATA.COMPLYWISE_USERS 
                            SET PASSWORD = '{new_p.replace("'", "''")}' 
                            WHERE EMAIL = '{st.session_state.target_email.replace("'", "''")}'
                        """).collect()
                        st.success("Password Updated!")
                        time.sleep(1.5)
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
    st.success("Successfully Authenticated")
    if st.button("Log Out"):
        st.session_state.logged_in = False
        st.rerun()
