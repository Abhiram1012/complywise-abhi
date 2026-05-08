import streamlit as st

# ---------------------------------------------------------
# 1. PAGE CONFIGURATION (Must be at the very top)
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
    # Targeted CSS to remove empty boxes and ghost spacing
    st.markdown("""
        <style>
        /* 1. Remove the empty white box (Streamlit Header) at the top */
        header, [data-testid="stHeader"] {
            display: none !important;
        }
        
        /* 2. Remove default padding from the main block */
        .block-container {
            padding-top: 2rem !important;
        }

        .stApp {
            background-color: #f4f7f9;
        }

        /* 3. Login Card Styling */
        .login-card {
            background-color: white;
            padding: 40px;
            border-radius: 15px;
            border: 1px solid #e0e6ed;
            box-shadow: 0px 10px 25px rgba(0,0,0,0.05);
        }

        /* 4. Pull Logo to the top and remove its bottom margin */
        [data-testid="stImage"] {
            margin-top: -10px;
            margin-bottom: -20px;
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
        # The wrapper div for our card
        st.markdown('<div class="login-card">', unsafe_allow_html=True)
        
        # Display Logo
        st.image(get_logo(), width=280)
        
        # Smaller vertical spacer
        st.markdown("<div style='margin-bottom: 30px;'></div>", unsafe_allow_html=True)

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
                <div style="margin-top:60px; border-top: 1px solid rgba(255,255,255,0.2); padding-top: 40px; text-align:center;">
                    <h2 style='color:white;'>ComplyWise Flow Intelligence</h2>
                    <p style='font-size:18px; color:#d9e6ff;'>
                        Data → Processing → Insights → Secure Flow → Output
                    </p>
                </div>
            </div>
        """, unsafe_allow_html=True)

# ---------------------------------------------------------
# 5. UI: MAIN APPLICATION (POST-LOGIN)
# ---------------------------------------------------------
def show_main_app():
    st.title("❄️ ComplyWise Dashboard")
    st.success(f"Welcome back, {st.session_state.current_user}!")
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
