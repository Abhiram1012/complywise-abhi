import streamlit as st

# ---------------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------------
st.set_page_config(
    page_title="ComplyWise Login",
    page_icon="🔒",
    layout="wide"
)

# ---------------------------------------------------------
# REMOVE TOP HEADER / EMPTY SPACE
# ---------------------------------------------------------
st.markdown("""
<style>

/* Remove Streamlit Header */
[data-testid="stHeader"] {
    display: none;
}

/* Remove top padding */
.block-container {
    padding-top: 0rem !important;
    margin-top: 0rem !important;
}

/* Remove unnecessary gaps */
[data-testid="stVerticalBlock"] {
    gap: 0rem;
}

/* Background */
.stApp {
    background-color: #f4f7f9;
}

/* Login Card */
.login-card {
    background-color: white;
    padding: 45px;
    border-radius: 18px;
    border: 1px solid #e0e6ed;
    box-shadow: 0px 10px 25px rgba(0,0,0,0.05);
}

/* Right Blue Panel */
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

/* Input Boxes */
.stTextInput input {
    border-radius: 8px !important;
    border: 1px solid #d1d9e0 !important;
    padding: 10px !important;
}

/* Login Button */
div.stButton > button:first-child {
    background-color: #007bff;
    color: white;
    border: none;
    border-radius: 8px;
    font-weight: 600;
    height: 45px;
}

/* Forgot Password Button */
.forgot-btn button {
    background: transparent !important;
    border: none !important;
    color: #007bff !important;
    box-shadow: none !important;
    font-size: 14px !important;
}

</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# SESSION STATES
# ---------------------------------------------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "view" not in st.session_state:
    st.session_state.view = "login"

if "current_user" not in st.session_state:
    st.session_state.current_user = ""

# ---------------------------------------------------------
# LOGO
# ---------------------------------------------------------
def get_logo():
    return "comply logo.jpg"

# ---------------------------------------------------------
# USERS
# ---------------------------------------------------------
USER_DATABASE = [
    {"userid": "admin", "password": "admin123"},
    {"userid": "abhiram", "password": "snow123"}
]

# ---------------------------------------------------------
# LOGIN PAGE
# ---------------------------------------------------------
def show_login_page():

    col_left, col_right = st.columns([1, 1.2], gap="large")

    # =====================================================
    # LEFT SIDE
    # =====================================================
    with col_left:

        st.markdown('<div class="login-card">', unsafe_allow_html=True)

        # LOGO
        st.image(get_logo(), width=250)

        # -------------------------------------------------
        # LOGIN VIEW
        # -------------------------------------------------
        if st.session_state.view == "login":

            st.subheader("Sign In")

            input_user = st.text_input(
                "User ID",
                placeholder="Enter Username"
            ).strip()

            input_pass = st.text_input(
                "Password",
                type="password",
                placeholder="Enter Password"
            ).strip()

            # Forgot Password
            col_space, col_forgot = st.columns([3, 1])

            with col_forgot:

                st.markdown(
                    '<div class="forgot-btn">',
                    unsafe_allow_html=True
                )

                forgot = st.button(
                    "Forgot Password?",
                    key="fg_btn"
                )

                st.markdown(
                    '</div>',
                    unsafe_allow_html=True
                )

            if forgot:
                st.session_state.view = "forgot"
                st.rerun()

            # LOGIN BUTTON
            if st.button(
                "Sign In",
                use_container_width=True
            ):

                user_match = next(
                    (
                        u for u in USER_DATABASE
                        if u["userid"] == input_user
                        and u["password"] == input_pass
                    ),
                    None
                )

                if user_match:
                    st.session_state.logged_in = True
                    st.session_state.current_user = input_user
                    st.rerun()

                else:
                    st.error("Invalid credentials")

        # -------------------------------------------------
        # FORGOT PASSWORD VIEW
        # -------------------------------------------------
        elif st.session_state.view == "forgot":

            st.subheader("Account Support")

            st.info("""
            Email: support@info.comply.com

            Please contact IT for password assistance.
            """)

            if st.button("← Back to Sign In"):
                st.session_state.view = "login"
                st.rerun()

        st.markdown('</div>', unsafe_allow_html=True)

    # =====================================================
    # RIGHT SIDE
    # =====================================================
    with col_right:

        st.markdown("""
        <div class="blue-panel">

            <h1 style="
                color:white;
                font-size:42px;
                line-height:1.2;
                margin-bottom:20px;
            ">
                Real-time Clinical, Financial,
                and Compliance Integrity
            </h1>

            <p style="
                color:#e0e0e0;
                font-size:20px;
                line-height:1.6;
                font-style: italic;
            ">
                Preventing risk, fraud, and revenue leakage
                through continuous data validation.
            </p>

            <div style="
                margin-top:60px;
                border-top: 1px solid rgba(255,255,255,0.2);
                padding-top:40px;
                text-align:center;
            ">

                <h2 style="color:white;">
                    ComplyWise Flow Intelligence
                </h2>

                <p style="
                    font-size:18px;
                    color:#d9e6ff;
                ">
                    Data → Processing → Insights →
                    Secure Flow → Output
                </p>

            </div>

        </div>
        """, unsafe_allow_html=True)

# ---------------------------------------------------------
# MAIN APP
# ---------------------------------------------------------
def show_main_app():

    st.sidebar.image(get_logo(), width=150)

    st.sidebar.divider()

    st.sidebar.write(
        f"Logged in as: **{st.session_state.current_user}**"
    )

    if st.sidebar.button(
        "Log Out",
        use_container_width=True
    ):
        st.session_state.logged_in = False
        st.rerun()

    st.title("❄️ ComplyWise Dashboard")

    st.success(
        f"Welcome back, {st.session_state.current_user}!"
    )

    st.divider()

    st.write("Dashboard Loaded Successfully")

# ---------------------------------------------------------
# APP EXECUTION
# ---------------------------------------------------------
if not st.session_state.logged_in:
    show_login_page()
else:
    show_main_app()
