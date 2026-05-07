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
        # Fallback for Streamlit Cloud / Local
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
    # Looks for file in your GitHub root folder
    local_path = "comply logo.jpg"
    if os.path.exists(local_path):
        return local_path
    else:
        # Guaranteed fallback to prevent MediaFileStorageError
        return "https://i.ibb.co/Xz9R94p/complywise-logo.png"

# ---------------------------------------------------------
# 4. USER DATABASE
# ---------------------------------------------------------
USER_DATABASE = [
    {"userid": "admin", "password": "admin123"},
    {"userid": "abhiram", "password": "snow123"}
]

# ---------------------------------------------------------
# 5. UI: LOGIN PAGE (WITH NUCLEAR CSS FIX)
# ---------------------------------------------------------
def show_login_page():
    # --- NUCLEAR CSS TO REMOVE TOP BOX AND PADDING ---
    st.markdown("""
        <style>
        /* 1. HIDE ALL TOP STREAMLIT ELEMENTS */
        header, footer, .stDeployButton, [data-testid="stHeader"], [data-testid="stToolbar"] {
            display: none !important;
            height: 0 !important;
            visibility: hidden !important;
        }

        /* 2. REMOVE ALL APP PADDING AND PULL CONTENT UP */
        .main .block-container {
            padding-top: 0px !important;
            margin-top: -80px !important; /* Forces content to top over the ghost box */
            padding-bottom: 0px !important;
        }

        /* 3. APP BACKGROUND */
        .stApp {
            background-color: #f4f7f9;
        }

        /* 4. LOGIN CARD (LEFT SIDE) */
        .login-card {
            background-color: white;
            padding: 40px;
            border-radius: 15px;
            border: 1px solid #e0e6ed;
            box-shadow: 0px 10px 25px rgba(0,0,0,0.05);
            margin-top: 30px;
        }

        /* 5. BLUE PANEL (RIGHT SIDE) */
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
            box-shadow: 0px 4px 20px rgba(0,0,0,0.2);
            margin-top: 30px;
        }

        /* 6. INPUTS AND BUTTONS */
        .stTextInput input {
            border: 1px solid #d1d9e0 !important;
            border-radius: 8px !important;
        }
        div.stButton > button:first-child {
            background-color: #007bff;
            color: white;
            border-radius: 8px;
            border: none;
            font-weight: 600;
        }
        
        /* Tighten gap between elements */
        [data-testid="stVerticalBlock"] {
            gap: 0.5rem !important;
        }
        </style>
    """, unsafe_allow_html=True)

    # Use a container to keep everything wrapped tightly
    main_container = st.container()
    
    with main_container:
        col_left, col_right = st.columns([1, 1.2], gap="large")

        # --- LEFT SIDE: LOGIN CARD ---
        with col_left:
            st.markdown('<div class="login-card">', unsafe_allow_html=True)
            
            # Logo is the first element inside the div
            st.image(get_logo(), width=280)
            st.write("---")

            if st.session_state.view == "login":
                st.subheader("Sign In")
                
                input_user = st.text_input("User ID", placeholder="Enter Username", key="user_field").strip()
                input_pass = st.text_input("Password", type="password", placeholder="Enter Password", key="pass_field").strip()

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
                st.subheader("Account Support")
                st.info("Email: **support@info.comply.com**\n\nPlease contact IT for password assistance.")
                if st.button("← Back to Sign In"):
                    st.session_state.view = "login"
                    st.rerun()
            
            st.markdown('</div>', unsafe_allow_html=True)

        # --- RIGHT SIDE: BLUE INFO PANEL ---
        with col_right:
            st.markdown("""
                <div class="blue-panel">
                    <h1 style='color:white; font-size:42px; line-height:1.2; margin-bottom:20px;'>
                        Real-time Clinical, Financial, and Compliance Integrity
                    </h1>
                    <p style='color:#e0e0e0; font-size:20px; line-height:1.6; font-style: italic;'>
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
# 6. UI: MAIN APPLICATION (POST-LOGIN)
# ---------------------------------------------------------
def show_main_app():
    # Sidebar
    st.sidebar.image(get_logo(), width=150)
    st.sidebar.divider()
    st.sidebar.write(f"Logged in as: **{st.session_state.current_user}**")
    
    if st.sidebar.button("Log Out", use_container_width=True):
        st.session_state.logged_in = False
        st.rerun()

    # Dashboard Content
    st.title("❄️ Dashboard")
    st.success(f"Welcome back, {st.session_state.current_user}!")
    st.divider()
    
    try:
        session = get_snowflake_session()
        st.write(f"Connected to Snowflake as: `{session.get_current_user()}`")
    except:
        st.warning("Snowflake session not active (Preview Mode).")

# ---------------------------------------------------------
# 7. EXECUTION LOGIC
# ---------------------------------------------------------
if not st.session_state.logged_in:
    show_login_page()
else:
    show_main_app()
