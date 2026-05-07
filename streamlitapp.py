import streamlit as st

# --- 1. SESSION INITIALIZATION ---
def get_snowflake_session():
    try:
        from snowflake.snowpark.context import get_active_session
        return get_active_session()
    except Exception:
        # If running outside Snowflake UI (e.g., local or Streamlit Cloud)
        return st.connection("snowflake").session()

def get_logo():
    try:
        session = get_active_session()
        logo_data = session.file.get_stream('@"ML_DATASETS"."DATA"."PIC"/comply logo.jpg')
        return logo_data.read()
    except:
        # Fallback URL if stage file isn't found
        return "https://i.ibb.co/Xz9R94p/complywise-logo.png"

# --- 3. PAGE CONFIG ---
st.set_page_config(layout="wide", page_title="ComplyWise Login")

# --- 4. DATABASE & STATE ---
USER_DATABASE = [
    {"userid": "admin", "password": "admin123"},
    {"userid": "abhiram", "password": "snow123"}
]

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "view" not in st.session_state:
    st.session_state.view = "login"

# --- 5. UI LAYOUT ---
def show_login_page():
    st.markdown("""
        <style>
        .blue-panel {
            background-color: #004a99;
            background-image: linear-gradient(160deg, #004a99 0%, #002d5c 100%);
            padding: 50px;
            border-radius: 15px;
            color: white;
            min-height: 500px;
        }
        div.stButton > button:first-child {
            background-color: #007bff;
            color: white;
            border-radius: 5px;
        }
        </style>
    """, unsafe_allow_html=True)

    col_left, col_right = st.columns([1, 1.2], gap="large")

    with col_left:
        # Display Logo
        logo_to_display = get_logo()
        st.image(logo_to_display, width=300)
        
        st.write("##")

        if st.session_state.view == "login":
            input_user = st.text_input("User ID", placeholder="Enter your ID").strip()
            input_pass = st.text_input("Password", type="password", placeholder="Enter password").strip()
            
            _, c2 = st.columns([1.5, 1])
            with c2:
                if st.button("Forgot Password?", key="fg_btn", type="secondary"):
                    st.session_state.view = "forgot"
                    st.rerun()

            if st.button("Sign In", key="login_btn", type="primary"):
                user_match = next((item for item in USER_DATABASE if item["userid"] == input_user and item["password"] == input_pass), None)
                if user_match:
                    st.session_state.logged_in = True
                    st.session_state.current_user = input_user
                    st.rerun()
                else:
                    st.error("Invalid Credentials")

        elif st.session_state.view == "forgot":
            st.subheader("Contact Support")
            st.info("Email: support@info.comply.com")
            if st.button("← Back to Login"):
                st.session_state.view = "login"
                st.rerun()

    with col_right:
        st.markdown(f"""
            <div class="blue-panel">
                <h1 style='color: white;'>Real-time Clinical, Financial, and Compliance Integrity</h1>
                <p style='color: #e0e0e0; font-size: 1.2rem;'>
                    Preventing risk, fraud, and revenue leakage through continuous data validation.
                </p>
                <br><br>
                <div style="text-align: center;">
                    <h3 style='color: white;'>ComplyWise Flow Intelligence</h3>
                    <p>Data → Processing → Insights → Secure Flow → Output</p>
                </div>
            </div>
        """, unsafe_allow_html=True)

# --- 6. MAIN APP ---
def show_main_app():
    st.sidebar.image(get_logo(), width=150)
    st.sidebar.write(f"Logged in: {st.session_state.current_user}")
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()

    st.title("❄️ Dashboard")
    st.success("Successfully logged into ComplyWise!")

# --- 7. EXECUTION ---
if not st.session_state.logged_in:
    show_login_page()
else:
    show_main_app()
