import streamlit as st
from snowflake.snowpark.context import get_active_session

# =========================================================
# PAGE CONFIG
# =========================================================
st.set_page_config(
    layout="wide",
    page_title="ComplyWise Login",
    page_icon="🔒"
)

# =========================================================
# USER DATABASE
# =========================================================
USER_DATABASE = [
    {"userid": "admin", "password": "admin123"},
    {"userid": "abhiram", "password": "snow123"}
]

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
# LOGO FUNCTION
# =========================================================
def get_logo():
    try:
        session = get_active_session()

        logo_data = session.file.get_stream(
            '@"ML_DATASETS"."DATA"."PIC"/comply logo.jpg'
        )

        return logo_data.read()

    except:
        return "comply logo.jpg"

# =========================================================
# LOGIN PAGE
# =========================================================
def show_login_page():

    # =====================================================
    # CSS
    # =====================================================
    st.markdown("""
    <style>

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

    /* Right Side Blue Panel */
    .blue-panel {
        background-color: #004a99;
        background-image:
            linear-gradient(
                160deg,
                #004a99 0%,
                #002d5c 100%
            );

        padding: 60px 50px;
        border-radius: 20px;
        color: white;
        min-height: 520px;

        display: flex;
        flex-direction: column;
        justify-content: center;

        box-shadow:
            0px 4px 20px rgba(0,0,0,0.2);
    }

    /* Input Fields */
    .stTextInput input {
        border-radius: 8px !important;
        border: 1px solid #d1d9e0 !important;
        padding: 10px !important;
    }

    /* Sign In Button */
    div.stButton > button:first-child {
        background-color: #007bff;
        color: white;
        border: none;
        border-radius: 8px;
        font-weight: 600;
        height: 45px;
    }

    </style>
    """, unsafe_allow_html=True)

    # =====================================================
    # LAYOUT
    # =====================================================
    left_col, right_col = st.columns(
        [1, 1.2],
        gap="large"
    )

    # =====================================================
    # LEFT SIDE
    # =====================================================
    with left_col:

        st.markdown(
            '<div class="login-card">',
            unsafe_allow_html=True
        )

        # Logo
        st.image(
            get_logo(),
            width=280
        )

        # Small spacing
        st.markdown(
            "<div style='height:15px'></div>",
            unsafe_allow_html=True
        )

        # =================================================
        # LOGIN VIEW
        # =================================================
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
            col_space, col_forgot = st.columns(
                [3, 1]
            )

            with col_forgot:

                if st.button(
                    "Forgot Password?",
                    key="fg_btn"
                ):
                    st.session_state.view = "forgot"
                    st.rerun()

            # Sign In Button
            if st.button(
                "Sign In",
                key="login_btn",
                use_container_width=True
            ):

                user_match = next(
                    (
                        item
                        for item in USER_DATABASE
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
                    st.error(
                        "Invalid Credentials"
                    )

        # =================================================
        # FORGOT PASSWORD VIEW
        # =================================================
        elif st.session_state.view == "forgot":

            st.subheader("Contact Support")

            st.info(
                """
Email: support@info.comply.com

Please contact IT for password assistance.
                """
            )

            if st.button(
                "← Back to Login"
            ):
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
                Real-time Clinical,
                Financial, and
                Compliance Integrity
            </h1>

            <p style="
                color:#e0e0e0;
                font-size:20px;
                line-height:1.6;
                font-style:italic;
            ">
                Preventing risk, fraud,
                and revenue leakage through
                continuous data validation.
            </p>

            <div style="
                margin-top:60px;
                border-top:
                    1px solid
                    rgba(255,255,255,0.2);

                padding-top:40px;
                text-align:center;
            ">

                <h2 style="color:white;">
                    ComplyWise
                    Flow Intelligence
                </h2>

                <p style="
                    font-size:18px;
                    color:#d9e6ff;
                ">
                    Data → Processing →
                    Insights → Secure Flow →
                    Output
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
        "Logout",
        use_container_width=True
    ):

        st.session_state.logged_in = False
        st.rerun()

    st.title(
        "❄️ ComplyWise Dashboard"
    )

    st.success(
        f"Welcome back, "
        f"{st.session_state.current_user}!"
    )

    st.divider()

    st.write(
        "Dashboard Loaded Successfully"
    )

# =========================================================
# EXECUTION
# =========================================================
if not st.session_state.logged_in:
    show_login_page()
else:
    show_main_app()
