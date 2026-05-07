import streamlit as st
import os

# ---------------------------------------------------------
# 1. PAGE CONFIGURATION
# ---------------------------------------------------------
st.set_page_config(
    layout="wide",
    page_title="ComplyWise Login",
    page_icon="🔒"
)

# ---------------------------------------------------------
# 2. SESSION INITIALIZATION
# ---------------------------------------------------------
def get_snowflake_session():
    try:
        from snowflake.snowpark.context import get_active_session
        return get_active_session()
    except Exception:
        return st.connection("snowflake").session()

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "view" not in st.session_state:
    st.session_state.view = "login"
if "current_user" not in st.session_state:
    st.session_state.current_user = ""

# ---------------------------------------------------------
# 3. ASSETS (LOGO)
# ---------------------------------------------------------
def get_logo():
    if os.path.exists("comply logo.jpg"):
        return "comply logo.jpg"
    return "https://i.ibb.co/Xz9R94p/complywise-logo.png"

# ---------------------------------------------------------
# 4. USER DATABASE
# ---------------------------------------------------------
USER_DATABASE = [
    {"userid": "admin", "password": "admin123"},
    {"userid": "abhiram", "password": "snow123"}
]

# ---------------------------------------------------------
# 5. UI: LOGIN PAGE
# ---------------------------------------------------------
def show_login_page():
    # CUSTOM CSS TO REMOVE TOP BOX AND ALIGN CARD
    st.markdown("""
        <style>
        /* Hide the top Streamlit header/padding where that box usually sits */
        header {visibility: hidden;}
        .main .block-container {
            padding-top: 2rem !important;
            padding-bottom: 0rem !important;
        }

        .stApp {
            background-color: #f4f7f9;
        }

        /* Login Card with Border */
        .login-card {
            background-color: white;
            padding: 40px;
            border-radius: 15px;
            border: 1px solid #e0e6ed;
            box-shadow: 0px 10px 25px rgba(0,0,0,0.05);
            margin-top: 0px;
        }

        /* Blue Panel */
        .blue-panel {
            background-color: #004a99;
            background-image: linear-gradient(160deg, #004a99 0%, #002d5c 100%);
            padding: 60px 50px;
            border-radius: 20px;
            color: white;
            min-height: 550px;
            display: flex;
            flex-direction: column;
            justify-content: center;
        }

        /* Input Styling */
        .stTextInput input {
            border: 1px solid #d1d9e0 !important;
            border-radius: 8px !important;
        }

        /* Primary Button */
        div.stButton > button:first-child {
            background-color: #007bff;
            color: white;
            border-radius: 8px;
            font-weight: 600;
        }
        </style>
    """, unsafe_allow_html=True)

    col_left, col_right = st.columns([1, 1.2], gap="large")

    with col_left:
        # We wrap the card start here
        st.markdown('<div class="login-card">', unsafe_allow_html=True)
        
        # LOGO
        st.image(get_logo(), width=280)
        
        st.write("---") # Visual separator

        if st.session_state.view == "login":
            st.subheader("Sign In")
            
            input_user = st.text_input("User ID", placeholder="Enter Username", key="user_in").strip()
            input_pass = st.text_input("Password", type="password", placeholder="Enter Password", key="pass_in").strip()

            c1, c2 = st.columns([1.3, 1])
            with c2:
                if st.button("Forgot Password?", key="fg_btn"):
                    st.session_state.view = "forgot"
                    st.rerun()

            if st.button("Sign In", key="login_btn", type="primary", use_container_width=True):
                user_match = next((u for u in USER_DATABASE if u["userid"] == input_user and u["password"] == input_pass), None)
                if user_match:
                    st.session_state.logged_in = True
                    st.session_state.current_user = input_user
                    st.rerun()
                else:
                    st.error("Invalid credentials.")

        elif st.session_state.view == "forgot":
            st.subheader("Support")
            st.info("Email: **support@info.comply.com**")
            if st.button("← Back"):
                st.session_state.view = "login"
                st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)

    with col_right:
        st.markdown("""
            <div class="blue-panel">
                <h1 style='color:white; font-size:42px; line-height:1.2;'>
                    Real-time Clinical, Financial, and Compliance Integrity
                </h1>
                <p style='color:#e0e0e0; font-size:20px; line-height:1.6; font-style: italic; margin-top:20px;'>
                    Preventing risk, fraud, and revenue leakage through continuous data validation.
                </p>
                <div style="margin-top:60px; border-top: 1px solid rgba(255,255,255,0.2); padding-top: 40px; text-align:center;">
                    <h2 style='color:white;'>ComplyWise Flow Intelligence</h2>
                    <p style='font-size:18px; color:#d9e6ff;'>
                        Data → Processing → Insights → Secure Flow → Output
                    </p>
                </div>
            </div>
        """, unsafe_allow_html=True)

# ---------------------------------------------------------
# 6. MAIN APPLICATION
# ---------------------------------------------------------
def show_main_app():
    st.sidebar.image(get_logo(), width=150)
    if st.sidebar.button("Log Out"):
        st.session_state.logged_in = False
        st.rerun()
    st.title("❄️ Dashboard")
    st.success(f"Welcome back, {st.session_state.current_user}!")

if not st.session_state.logged_in:
    show_login_page()
else:
    show_main_app()
