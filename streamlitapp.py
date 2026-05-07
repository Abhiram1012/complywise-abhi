import streamlit as st

# --- 1. SESSION INITIALIZATION ---
def get_snowflake_session():
    try:
        from snowflake.snowpark.context import get_active_session
        return get_active_session()
    except Exception:
        # Running outside Snowflake (Streamlit Cloud / Local)
        return st.connection("snowflake").session()

# --- 2. LOGO FUNCTION ---
def get_logo():
    return "comply logo.jpg"

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

# --- 6. LOGIN PAGE ---
def show_login_page():

    st.markdown("""
        <style>

        .stApp {
            background-color: #f5f7fa;
        }

        .blue-panel {
            background-color: #004a99;
            background-image: linear-gradient(160deg, #004a99 0%, #002d5c 100%);
            padding: 50px;
            border-radius: 20px;
            color: white;
            min-height: 500px;
            box-shadow: 0px 4px 20px rgba(0,0,0,0.2);
        }

        div.stButton > button:first-child {
            background-color: #007bff;
            color: white;
            border-radius: 8px;
            border: none;
            padding: 10px 20px;
            font-weight: 600;
        }

        div.stButton > button:first-child:hover {
            background-color: #0056b3;
            color: white;
        }

        </style>
    """, unsafe_allow_html=True)

    col_left, col_right = st.columns([1, 1.2], gap="large")

    # ---------------- LEFT PANEL ----------------
    with col_left:

        # Logo
        st.image(get_logo(), width=300)

        st.write("")

        if st.session_state.view == "login":

            st.subheader("Login")

            input_user = st.text_input(
                "User ID",
                placeholder="Enter your User ID"
            ).strip()

            input_pass = st.text_input(
                "Password",
                type="password",
                placeholder="Enter your password"
            ).strip()

            _, c2 = st.columns([1.5, 1])

            with c2:
                if st.button(
                    "Forgot Password?",
                    key="forgot_btn",
                    type="secondary"
                ):
                    st.session_state.view = "forgot"
                    st.rerun()

            if st.button(
                "Sign In",
                key="login_btn",
                type="primary",
                use_container_width=True
            ):

                user_match = next(
                    (
                        item for item in USER_DATABASE
                        if item["userid"] == input_user
                        and item["password"] == input_pass
                    ),
                    None
                )

                if user_match:
                    st.session_state.logged_in = True
                    st.session_state.current_user = input_user
                    st.rerun()
                else:
                    st.error("Invalid Credentials")

        # -------- FORGOT PASSWORD --------
        elif st.session_state.view == "forgot":

            st.subheader("Contact Support")

            st.info("""
            📧 support@info.comply.com
            
            Please contact the support team to reset your password.
            """)

            if st.button("← Back to Login"):
                st.session_state.view = "login"
                st.rerun()

    # ---------------- RIGHT PANEL ----------------
    with col_right:

        st.markdown("""
            <div class="blue-panel">

                <h1 style='color:white; font-size:42px;'>
                    Real-time Clinical, Financial,
                    and Compliance Integrity
                </h1>

                <p style='color:#e0e0e0; font-size:20px; line-height:1.8;'>
                    Preventing risk, fraud, and revenue leakage
                    through continuous data validation.
                </p>

                <br><br>

                <div style="text-align:center; margin-top:60px;">

                    <h2 style='color:white;'>
                        ComplyWise Flow Intelligence
                    </h2>

                    <p style='font-size:18px; color:#d9e6ff;'>
                        Data → Processing → Insights →
                        Secure Flow → Output
                    </p>

                </div>

            </div>
        """, unsafe_allow_html=True)

# --- 7. MAIN APPLICATION ---
def show_main_app():

    st.sidebar.image(get_logo(), width=180)

    st.sidebar.success(
        f"Logged in as: {st.session_state.current_user}"
    )

    if st.sidebar.button("Logout"):

        st.session_state.logged_in = False
        st.session_state.current_user = ""
        st.session_state.view = "login"

        st.rerun()

    # Main Dashboard
    st.title("❄️ ComplyWise Dashboard")

    st.success("Successfully logged into ComplyWise!")

    st.write("---")

    st.subheader("Welcome")

    st.write("""
    This dashboard provides:
    
    - Clinical Integrity Monitoring
    - Financial Compliance Tracking
    - Revenue Leakage Prevention
    - Risk & Fraud Detection
    - Real-time Operational Insights
    """)

# --- 8. APP EXECUTION ---
if not st.session_state.logged_in:
    show_login_page()
else:
    show_main_app()
