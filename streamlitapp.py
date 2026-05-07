import streamlit as st
from snowflake.snowpark.context import get_active_session
import os

# --- 1. PAGE CONFIG ---
st.set_page_config(layout="wide", page_title="ComplyWise Login")

# --- 2. USER DATABASE ---
USER_DATABASE = [
    {"userid": "admin", "password": "admin123"},
    {"userid": "abhiram", "password": "snow123"}
]

# --- 3. SESSION STATE ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "view" not in st.session_state:
    st.session_state.view = "login"

# --- 4. LOGO RETRIEVAL ---
def get_logo():
    try:
        # Tries to get from Snowflake Stage first
        session = get_active_session()
        logo_data = session.file.get_stream('@"ML_DATASETS"."DATA"."PIC"/comply logo.jpg')
        return logo_data.read()
    except:
        # Fallback to local GitHub file or Web URL
        if os.path.exists("comply logo.jpg"):
            return "comply logo.jpg"
        return "https://i.ibb.co/Xz9R94p/complywise-logo.png"

# --- 5. UI LAYOUT ---
def show_login_page():
    # THE NUCLEAR CSS FIX: Deletes the ghost box and pulls content to the very top
    st.markdown("""
        <style>
        /* 1. Hide Streamlit elements that cause the white box */
        header, [data-testid="stHeader"], [data-testid="stToolbar"], .stDeployButton {
            display: none !important;
            height: 0 !important;
            visibility: hidden !important;
        }

        /* 2. Force content to the actual top of the page */
        .main .block-container {
            padding-top: 0px !important;
            margin-top: -80px !important; /* Adjust this value if the box is still visible */
            padding-bottom: 0px !important;
        }

        .stApp {
            background-color: #f4f7f9;
        }

        /* 3. Login Card (The bordered box for the left side) */
        .login-card {
            background-color: white;
            padding: 40px;
            border-radius: 15px;
            border: 1px solid #e0e6ed;
            box-shadow: 0px 10px 25px rgba(0,0,0,0.05);
            margin-top: 20px;
        }

        /* 4. Blue side panel */
        .blue-panel {
            background-color: #004a99;
            background-image: linear-gradient(160deg, #004a99 0%, #002d5c 100%);
            padding: 50px;
            border-radius: 20px;
            color: white;
            min-height: 550px;
            display: flex;
            flex-direction: column;
            justify-content: center;
            box-shadow: 0px 4px 20px rgba(0,0,0,0.2);
            margin-top: 20px;
        }

        /* 5. Button and Input styling */
        div.stButton > button:first-child {
            background-color: #007bff;
            color: white;
            border-radius: 8px;
            font-weight: 600;
        }
        
        .stTextInput input {
            border: 1px solid #d1d9e0 !important;
        }
        </style>
    """, unsafe_allow_html=True)

    # Split screen
    col_left, col_right = st.columns([1, 1.2], gap="large")

    with col_left:
        # Opening the login card div
        st.markdown('<div class="login-card">', unsafe_allow_html=True)
        
        # Logo
        st.image(get_logo(), width=280)
        st.write("---")

        if st.session_state.view == "login":
            st.subheader("Sign In")
            input_user = st.text_input("User ID", placeholder="Enter your ID").strip()
            input_pass = st.text_input("Password", type="password", placeholder="Enter password").strip()
            
            c1, c2 = st.columns([1.5, 1])
            with c2:
                if st.button("Forgot Password?", key="fg_btn"):
                    st.session_state.view = "forgot"
                    st.rerun()

            if st.button("Sign In", key="login_btn", type="primary", use_container_width=True):
                user_match = next((item for item in USER_DATABASE if item["userid"] == input_user and item["password"] == input_pass), None)
                if user_match:
                    st.session_state.logged_in = True
                    st.session_state.current_user = input_user
                    st.rerun()
                else:
                    st.error("Invalid Credentials")

        elif st.session_state.view == "forgot":
            st.subheader("Contact Support")
            st.info("Email: support@info.comply.com")
            if st.button("← Back to Login"):
                st.session_state.view = "login"
                st.rerun()
        
        # Closing the login card div
        st.markdown('</div>', unsafe_allow_html=True)

    with col_right:
        st.markdown(f"""
            <div class="blue-panel">
                <h1 style='color: white; font-size: 42px;'>Real-time Clinical, Financial, and Compliance Integrity</h1>
                <p style='color: #e0e0e0; font-size: 1.3rem; margin-top: 20px;'>
                    Preventing risk, fraud, and revenue leakage through continuous data validation.
                </p>
                <div style="text-align: center; margin-top: 60px; border-top: 1px solid rgba(255,255,255,0.2); padding-top: 40px;">
                    <h3 style='color: white;'>ComplyWise Flow Intelligence</h3>
                    <p style='color: #d9e6ff;'>Data → Processing → Insights → Secure Flow → Output</p>
                </div>
            </div>
        """, unsafe_allow_html=True)

# --- 6. MAIN APP ---
def show_main_app():
    st.sidebar.image(get_logo(), width=150)
    st.sidebar.write(f"Logged in: **{st.session_state.current_user}**")
    if st.sidebar.button("Logout", use_container_width=True):
        st.session_state.logged_in = False
        st.rerun()

    st.title("❄️ Dashboard")
    st.success("Successfully logged into ComplyWise!")

# --- 7. EXECUTION ---
if not st.session_state.logged_in:
    show_login_page()
else:
    show_main_app()
