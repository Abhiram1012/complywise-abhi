import streamlit as st

# --- 1. SESSION INITIALIZATION ---
def get_snowflake_session():
    try:
        from snowflake.snowpark.context import get_active_session
        return get_active_session()
    except Exception:
        # Running outside Snowflake (Streamlit Cloud / Local)
        return st.connection("snowflake").session()

# --- 2. LOGO FUNCTION (Using Local/GitHub File) ---
def get_logo():
    # Ensure this file is in the root of your GitHub repo
    return "comply_logo.jpg"

# --- 3. PAGE CONFIG ---
st.set_page_config(
    layout="wide",
    page_title="ComplyWise Login"
)

# --- 4. USER DATABASE ---
USER_DATABASE = [
    {"userid": "admin", "password": "admin123"},
    {"userid": "abhiram", "password": "snow123"}
]

# --- 5. SESSION STATE ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "view" not in st.session_state:
    st.session_state.view = "login"
if "current_user" not in st.session_state:
    st.session_state.current_user = ""

# --- 6. LOGIN PAGE UI ---
def show_login_page():
    st.markdown("""
        <style>
        /* Light gray background for the whole page */
        .stApp {
            background-color: #f4f7f9;
        }

        /* White Card with Border (Left Side) */
        .login-card {
            background-color: white;
            padding: 45px;
            border-radius: 15px;
            border: 1px solid #e0e6ed;
            box-shadow: 0px 10px 25px rgba(0,0,0,0.05);
            margin-top: 10px;
        }

        /* Blue Gradient Panel (Right Side) */
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
        }

        /* Button Styling */
        div.stButton > button:first-child {
            background-color: #007bff;
            color: white;
            border-radius: 8px;
            border: none;
            font-weight: 600;
        }

        /* Text Input styling */
        .stTextInput input {
            border: 1px solid #d1d9e0 !important;
            border-radius: 8px !important;
        }
        </style>
    """, unsafe_allow_html=True)

    # Creating the Split Screen (Left for Card, Right for Blue Panel)
    col_left, col_right = st.columns([1, 1.2], gap="large")

    # ---------------- LEFT PANEL (Login Card) ----------------
    with col_left:
        st.markdown('<div class="login-card">', unsafe_allow_html=True)
        
        # Display GitHub Logo
        st.image(get_logo(), width=300)
        st.write("##")

        if st.session_state.view == "login":
            st.subheader("Sign In")
            input_user = st.text_input("User ID", placeholder="Enter your User ID").strip()
            input_pass = st.text_input("Password", type="password", placeholder="Enter your password").strip()

            c1, c2 = st.columns([1.5, 1])
            with c2:
                if st.button("Forgot Password?", key="forgot_btn", type="secondary"):
                    st.session_state.view = "forgot"
                    st.rerun()

            if st.button("Sign In", key="login_btn", type="primary", use_container_width=True):
                user_match = next((u for u in USER_DATABASE if u["userid"] == input_user and u["password"] == input_pass), None)
                if user_match:
                    st.session_state.logged_in = True
                    st.session_state.current_user = input_user
                    st.rerun()
                else:
                    st.error("Invalid Credentials")

        elif st.session_state.view == "forgot":
            st.subheader("Contact Support")
            st.info("📧 support@info.comply.com\n\nPlease contact IT for a password reset.")
            if st.button("← Back to Login"):
                st.session_state.view = "login"
                st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True) # End Card

    # ---------------- RIGHT PANEL (Blue Image/Info) ----------------
    with col_right:
        st.markdown("""
            <div class="blue-panel">
                <h1 style='color:white; font-size:42px; margin-bottom: 20px;'>
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

# --- 7. MAIN DASHBOARD ---
def show_main_app():
    st.sidebar.image(get_logo(), width=150)
    st.sidebar.success(f"User: {st.session_state.current_user}")

    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()

    st.title("❄️ Dashboard")
    st.success("Successfully logged into ComplyWise!")
    # Your Snowflake RAG/Analytics logic goes here

# --- 8. EXECUTION ---
if not st.session_state.logged_in:
    show_login_page()
else:
    show_main_app()
