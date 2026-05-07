import streamlit as st

# =========================================================
# PAGE CONFIG
# =========================================================
st.set_page_config(
    page_title="ComplyWise Login",
    page_icon="🔒",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =========================================================
# SAFE CSS
# =========================================================
st.markdown("""
<style>

/* Remove top spacing */
.block-container {
    padding-top: 1rem !important;
}

/* Hide toolbar */
[data-testid="stToolbar"] {
    display: none;
}

/* Hide top decoration */
[data-testid="stDecoration"] {
    display: none;
}

/* Hide sidebar toggle */
[data-testid="collapsedControl"] {
    display: none;
}

/* App Background */
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

/* Text Inputs */
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

/* Forgot Password */
.forgot-btn button {
    background: transparent !important;
    border: none !important;
    color: #007bff !important;
    box-shadow: none !important;
    font-size: 14px !important;
}

</style>
""", unsafe_allow_html=True)

# =========================================================
# SESSION STATE
# =========================================================
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "view" not in st.session_state:
    st.session_state.view = "login"

if "current_user" not in st.session_state:
    st.session_state.current_user = ""

# =========================================================
# LOGO
# =========================================================
def get_logo():
    return "comply logo.jpg"

# =========================================================
# USER DATABASE
# =========================================================
USER_DATABASE = [
    {"userid": "admin", "password": "admin123"},
    {"userid": "abhiram", "password": "snow123"}
]

# =========================================================
# LOGIN PAGE
# =========================================================
def show_login_page():

    left_col, right_col = st.columns([1, 1.2], gap="large")

    # =====================================================
    # LEFT SIDE
    # =====================================================
    with left_col:

        st.markdown(
            '<div class="login-card">',
            unsafe_allow_html=True
        )

        # Logo
        st.image(get_logo(), width=260)

        st.markdown("<br>", unsafe_allow_html=True)

        # =================================================
        # LOGIN VIEW
        # =================================================
        if st.session_state.view == "login":

            st.subheader("Sign In")

            input_user = st.text_input(
                "User ID",
                placeholder="Enter Username"
            )

            input_pass = st.text_input(
                "Password",
                type="password",
                placeholder="Enter Password"
            )

            # Forgot Password
            spacer, forgot_col = st.columns([3, 1])

            with forgot_col:

                st.markdown(
                    '<div class="forgot-btn">',
                    unsafe_allow_html=True
                )

                forgot = st.button(
                    "Forgot Password?"
                )

                st.markdown(
                    '</div>',
                    unsafe_allow_html=True
                )

            if forgot:
                st.session_state.view = "forgot"
                st.rerun()

            # Login Button
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
                    st.error(
                        "Invalid credentials"
                    )

        # =================================================
        # FORGOT PASSWORD VIEW
        # =================================================
        elif st.session_state.view == "forgot":

            st.subheader("Account Support")

            st.info("""
Email: support@info.comply.com

Please contact IT for password assistance.
            """)

            if st.button("← Back to Sign In"):
                st.session_state.view = "login"
                st.rerun()

        st.markdown(
            '</div>',
            unsafe_allow_html=True
        )

    # =====================================================
    # RIGHT SIDE
    # =====================================================
    with right_col:

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
    font-style:italic;
">
Preventing risk, fraud, and revenue leakage
through continuous data validation.
</p>

<div style="
    margin-top:60px;
    border-top:1px solid rgba(255,255,255,0.2);
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

# =========================================================
# MAIN APP
# =========================================================
def show_main_app():

    st.sidebar.image(
        get_logo(),
        width=150
    )

    st.sidebar.divider()

    st.sidebar.write(
        f"Logged in as: "
        f"**{st.session_state.current_user}**"
    )

    if st.sidebar.button(
        "Log Out",
        use_container_width=True
    ):
        st.session_state.logged_in = False
        st.rerun()

    st.title("❄️ ComplyWise Dashboard")

    st.success(
        f"Welcome back, "
        f"{st.session_state.current_user}!"
    )

    st.divider()

    st.write(
        "Dashboard Loaded Successfully"
    )

# =========================================================
# APP EXECUTION
# =========================================================
if not st.session_state.logged_in:
    show_login_page()
else:
    show_main_app()
