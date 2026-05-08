import streamlit as st
import base64

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
# 3. ASSETS (IMAGE CONVERSION TO BYTES)
# ---------------------------------------------------------
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

# ---------------------------------------------------------
# 4. USER DATABASE
# ---------------------------------------------------------
USER_DATABASE = [
    {"userid": "admin", "password": "admin123"},
    {"userid": "abhiram", "password": "snow123"}
]

# ---------------------------------------------------------
# 5. UI: LOGIN PAGE
# ---------------------------------------------------------
def show_login_page():
    # Load logo as base64 to inject directly into HTML
    try:
        logo_base64 = get_base64_of_bin_file("comply logo.jpg")
    except:
        logo_base64 = ""

    st.markdown(f"""
        <style>
        /* Hide Streamlit Header */
        header, [data-testid="stHeader"] {{
            visibility: hidden;
            display: none !important;
        }}
        
        .block-container {{
            padding-top: 2rem !important;
        }}

        .stApp {{
            background-color: #f4f7f9;
        }}

        /* The Login Card */
        .login-card {{
            background-color: white;
            padding: 40px;
            border-radius: 15px;
            border: 1px solid #e0e6ed;
            box-shadow: 0px 10px 25px rgba(0,0,0,0.05);
            display: flex;
            flex-direction: column;
        }}

        /* Logo styling to remove all ghost boxes */
        .custom-logo {{
            width: 280px;
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
            box-shadow: 0px 4px 20px rgba(0,0,0,0.2);
        }}

        div.stButton > button:first-child {{
            background-color: #007bff;
            color: white;
            border-radius: 8px;
            border: none;
            font-weight: 600;
        }}
        </style>
    """, unsafe_allow_html=True)

    col_left, col_right = st.columns([1, 1.2], gap="large")

    with col_left:
        # We wrap the logo in the SAME markdown as the card start
        # This prevents Streamlit from inserting an empty container in between
        st.markdown(f'''
            <div class="login-card">
                <img src="data:image/jpeg;base64,{logo_base64}" class="custom-logo">
        ''', unsafe_allow_html=True)

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
# 6. EXECUTION LOGIC
# ---------------------------------------------------------
if not st.session_state.logged_in:
    show_login_page()
else:
    st.title("ComplyWise Dashboard")
    if st.button("Log Out"):
        st.session_state.logged_in = False
        st.rerun()
