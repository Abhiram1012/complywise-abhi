import streamlit as st
import base64
import random
import time
from snowflake.snowpark import Session

# ---------------------------------------------------------
# 1. PAGE CONFIGURATION
# ---------------------------------------------------------
st.set_page_config(
    layout="wide",
    page_title="ComplyWise | Secure Login",
    page_icon="🔒"
)

# ---------------------------------------------------------
# 2. SNOWFLAKE SESSION
# ---------------------------------------------------------
def get_snowflake_session():

    connection_parameters = {
        "account": st.secrets["snowflake"]["BSKPNCS-SGB36220"],
        "user": st.secrets["snowflake"]["ABHIC"],
        "password": st.secrets["snowflake"]["Abhiram8074670349"],
        "warehouse": st.secrets["snowflake"]["compute_wh"],
        "database": st.secrets["snowflake"]["ML_DATASETS"],
        "schema": st.secrets["snowflake"]["DATA"],
        "role": st.secrets["snowflake"]["accountadmin"]
    }

    return Session.builder.configs(connection_parameters).create()

# ---------------------------------------------------------
# 3. SESSION STATE
# ---------------------------------------------------------
defaults = {
    "logged_in": False,
    "view": "login",
    "reset_step": "verify_user",
    "otp_code": None,
    "target_email": None
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value

# ---------------------------------------------------------
# 4. HELPER FUNCTIONS
# ---------------------------------------------------------
def get_base64_of_bin_file(bin_file):
    try:
        with open(bin_file, "rb") as f:
            return base64.b64encode(f.read()).decode()
    except Exception:
        return ""

def send_snowflake_email(target_email, otp_code):

    session = get_snowflake_session()

    subject = "ComplyWise Password Reset OTP"

    body = f"""
Your ComplyWise verification code is: {otp_code}

This OTP is valid for 10 minutes.
"""

    try:

        sql_command = f"""
        CALL SYSTEM$SEND_EMAIL(
            'MY_EMAIL_INT',
            '{target_email}',
            '{subject}',
            '{body}'
        )
        """

        session.sql(sql_command).collect()

        return True

    except Exception as e:
        st.error(f"Email Error: {e}")
        return False

# ---------------------------------------------------------
# 5. LOGIN PAGE
# ---------------------------------------------------------
def show_login_page():

    logo_base64 = get_base64_of_bin_file("comply logo.jpg")

    st.markdown(
        f"""
        <style>

        [data-testid="stHeader"] {{
            visibility: hidden;
            display: none !important;
        }}

        .block-container {{
            padding-top: 2rem !important;
        }}

        .stApp {{
            background-color: #f4f7f9;
        }}

        .login-card {{
            background-color: white;
            padding: 40px;
            border-radius: 15px;
            border: 1px solid #e0e6ed;
            box-shadow: 0px 10px 25px rgba(0,0,0,0.05);
        }}

        .custom-logo {{
            width: 320px;
            margin-bottom: 25px;
            display: block;
        }}

        .blue-panel {{
            background-color: #004a99;
            background-image: linear-gradient(160deg, #004a99 0%, #002d5c 100%);
            padding: 60px 50px;
            border-radius: 20px;
            color: white;
            min-height: 520px;
            display: flex;
            flex-direction: column;
            justify-content: center;
        }}

        </style>
        """,
        unsafe_allow_html=True
    )

    col_left, col_right = st.columns([1, 1.2], gap="large")

    # ---------------------------------------------------------
    # LEFT PANEL
    # ---------------------------------------------------------
    with col_left:

        st.markdown(
            f"""
            <div class="login-card">
            <img src="data:image/jpeg;base64,{logo_base64}" class="custom-logo">
            """,
            unsafe_allow_html=True
        )

        # ---------------------------------------------------------
        # LOGIN VIEW
        # ---------------------------------------------------------
        if st.session_state.view == "login":

            st.subheader("Sign In")

            u_input = st.text_input(
                "User ID or Email",
                placeholder="Enter ID or Email"
            )

            u_pass = st.text_input(
                "Password",
                type="password",
                placeholder="Enter Password"
            )

            c1, c2 = st.columns([1.5, 1])

            with c2:
                if st.button("Forgot Password?"):
                    st.session_state.view = "forgot"
                    st.session_state.reset_step = "verify_user"
                    st.rerun()

            if st.button(
                "Sign In",
                type="primary",
                use_container_width=True
            ):

                session = get_snowflake_session()

                query = f"""
                SELECT USERID, EMAIL
                FROM ML_DATASETS.DATA.COMPLYWISE_USERS
                WHERE (
                    USERID = '{u_input.strip()}'
                    OR EMAIL = '{u_input.strip()}'
                )
                AND PASSWORD = '{u_pass}'
                """

                result = session.sql(query).collect()

                if len(result) > 0:

                    st.session_state.logged_in = True

                    st.success("Login Successful")

                    time.sleep(1)

                    st.rerun()

                else:
                    st.error("Invalid credentials")

        # ---------------------------------------------------------
        # FORGOT PASSWORD VIEW
        # ---------------------------------------------------------
        elif st.session_state.view == "forgot":

            st.subheader("Reset Password")

            # ---------------------------------------------------------
            # STEP 1 - VERIFY EMAIL
            # ---------------------------------------------------------
            if st.session_state.reset_step == "verify_user":

                email_target = st.text_input(
                    "Enter Registered Email",
                    placeholder="email@example.com"
                )

                if st.button(
                    "Send OTP",
                    type="primary",
                    use_container_width=True
                ):

                    session = get_snowflake_session()

                    query = f"""
                    SELECT EMAIL
                    FROM ML_DATASETS.DATA.COMPLYWISE_USERS
                    WHERE EMAIL = '{email_target.strip()}'
                    """

                    exists = session.sql(query).collect()

                    if len(exists) > 0:

                        otp = str(random.randint(1000, 9999))

                        st.session_state.otp_code = otp
                        st.session_state.target_email = email_target

                        with st.spinner("Sending OTP..."):

                            if send_snowflake_email(email_target, otp):

                                st.success("OTP Sent Successfully")

                                st.session_state.reset_step = "enter_otp"

                                st.rerun()

                    else:
                        st.error("Email not found")

            # ---------------------------------------------------------
            # STEP 2 - VERIFY OTP
            # ---------------------------------------------------------
            elif st.session_state.reset_step == "enter_otp":

                st.info(
                    f"OTP sent to: {st.session_state.target_email}"
                )

                otp_in = st.text_input(
                    "Enter 4-Digit OTP",
                    placeholder="0000"
                )

                if st.button(
                    "Verify OTP",
                    type="primary",
                    use_container_width=True
                ):

                    if otp_in == st.session_state.otp_code:

                        st.success("OTP Verified")

                        st.session_state.reset_step = "new_password"

                        st.rerun()

                    else:
                        st.error("Incorrect OTP")

            # ---------------------------------------------------------
            # STEP 3 - UPDATE PASSWORD
            # ---------------------------------------------------------
            elif st.session_state.reset_step == "new_password":

                new_p = st.text_input(
                    "New Password",
                    type="password"
                )

                conf_p = st.text_input(
                    "Confirm Password",
                    type="password"
                )

                if st.button(
                    "Update Password",
                    type="primary",
                    use_container_width=True
                ):

                    if new_p == conf_p and new_p != "":

                        session = get_snowflake_session()

                        update_query = f"""
                        UPDATE ML_DATASETS.DATA.COMPLYWISE_USERS
                        SET PASSWORD = '{new_p}'
                        WHERE EMAIL = '{st.session_state.target_email}'
                        """

                        session.sql(update_query).collect()

                        st.success("Password Updated Successfully")

                        time.sleep(1.5)

                        st.session_state.view = "login"
                        st.session_state.reset_step = "verify_user"
                        st.session_state.otp_code = None
                        st.session_state.target_email = None

                        st.rerun()

                    else:
                        st.error("Passwords do not match")

            # ---------------------------------------------------------
            # BACK BUTTON
            # ---------------------------------------------------------
            if st.button("← Back to Login"):

                st.session_state.view = "login"
                st.session_state.reset_step = "verify_user"

                st.rerun()

        st.markdown("</div>", unsafe_allow_html=True)

    # ---------------------------------------------------------
    # RIGHT PANEL
    # ---------------------------------------------------------
    with col_right:

        st.markdown(
            """
            <div class="blue-panel">
                <h1>ComplyWise Integrity</h1>

                <p>
                    Continuous data validation and
                    risk prevention.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

# ---------------------------------------------------------
# 6. MAIN EXECUTION
# ---------------------------------------------------------
if not st.session_state.logged_in:

    show_login_page()

else:

    st.title("Main Dashboard")

    st.success("Successfully Authenticated")

    if st.button("Log Out"):

        st.session_state.logged_in = False
        st.session_state.view = "login"

        st.rerun()
