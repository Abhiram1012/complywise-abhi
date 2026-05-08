import streamlit as st

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
if "current_user" not in st.session_state:
    st.session_state.current_user = ""

# ---------------------------------------------------------
# 3. ASSETS & DATABASE
# ---------------------------------------------------------
def get_logo():
    return "comply logo.jpg"

USER_DATABASE = [
    {"userid": "admin", "password": "admin123"},
    {"userid": "abhiram", "password": "snow123"}
]

# ---------------------------------------------------------
# 4. UI: LOGIN PAGE
# ---------------------------------------------------------
def show_login_page():
    # FINAL CSS OVERRIDE
    st.markdown("""
        <style>
        /* 1. Hide the global Streamlit header */
        header, [data-testid="stHeader"] {
            display: none !important;
        }

        /* 2. Remove padding from the very top of the app */
        .block-container {
            padding-top: 0rem !important;
        }

        .stApp {
            background-color: #f4f7f9;
        }

        /* 3. The Card: Ensure it has no extra top margin */
        .login-card {
            background-color: white;
            padding: 20px 45px 45px 45px;
            border-radius: 15px;
            border: 1px solid #e0e6ed;
            box-shadow: 0px 10px 25px rgba(0,0,0,0.05);
            margin-top: 10px; /* Adjust this to move the whole card up/down */
        }

        /* 4. THE FIX: Target the specific image container to remove the top gap */
        [data-testid="stImage"] > img {
            margin-top: -60px !important; /* Adjust this number until the box disappears */
            clip-path: inset(60px 0 0 0); /* This hides the top 60px of the image if it's white space */
        }
        
        /* Ensure the container doesn't show the white background of the image */
        [data-testid="stImage"] {
            background: transparent !important;
        }

        .blue-panel {
            background-color: #004a99;
            background-image: linear-gradient(160deg, #004a99 0%, #002d5c 100%);
            padding: 60px 50px;
            border-radius: 20px;
            color: white;
            min-height: 520px;
            display: flex;
            flex-direction: column;
            justify-content: center;
            box-shadow: 0px 4px 20px rgba(0,0,0,0.2);
        }

        div.stButton > button:first-child {
            background-color: #007bff;
            color: white;
            border-radius: 8px;
            border: none;
            font-weight: 600;
        }
        </style>
    """, unsafe_allow_html=True)

    col_left, col_right = st.columns([1, 1.2], gap="large")

    with col_left:
        st.markdown('<div class="login-card">', unsafe_allow_html=True)
        
        # Display Logo
        st.image(get_logo(), width=280)
        
        # Space between logo and text
        st.markdown("<div style='margin-bottom: 20px;'></div>", unsafe_allow_html=True)

        if st.session_state.view == "login":
            st.subheader("Sign In")
            input_user = st.text_input("User ID", placeholder="Enter Username").strip()
            input_pass = st.text_input("Password", type="password", placeholder="Enter Password").strip()

            c1, c2 = st.columns([1.5, 1])
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
            st.info("Email: **support@info.comply.com**")
            if st.button("← Back to Sign In"):
                st.session_state.view = "login"
                st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)

    with col_right:
        st.markdown("""
            <div class="blue-panel">
                <h1 style='color:white; font-size:42px; line-height:1.2; margin-bottom:20px;'>
                    Real-time Clinical, Financial, and Compliance Integrity
                </h1>
                <p style='color:#e0e0e0; font-size:20px; line-height:1.6; font-style: italic;'>
                    Preventing risk, fraud, and revenue leakage through continuous data validation.
                </p>
            </div>
        """, unsafe_allow_html=True)

# ---------------------------------------------------------
# 5. UI: MAIN APPLICATION
# ---------------------------------------------------------
def show_main_app():
    st.title("❄️ ComplyWise Dashboard")
    if st.button("Log Out"):
        st.session_state.logged_in = False
        st.rerun()

# ---------------------------------------------------------
# 6. EXECUTION LOGIC
# ---------------------------------------------------------
if not st.session_state.logged_in:
    show_login_page()
else:
    show_main_app()
