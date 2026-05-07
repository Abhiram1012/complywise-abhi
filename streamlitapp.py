import streamlit as st
import re
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.exceptions import SnowparkSQLException

# ---------------------------------------------------------
# 1. PAGE CONFIGURATION
# ---------------------------------------------------------
st.set_page_config(
    page_title="Indian Legal RAG Assistant",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------------------------------------------
# 2. USER DATABASE & STATE
# ---------------------------------------------------------
USER_DATABASE = [
    {"userid": "admin", "password": "admin123"},
    {"userid": "abhiram", "password": "snow123"}
]

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "view" not in st.session_state:
    st.session_state.view = "login"

# ---------------------------------------------------------
# 3. HELPER FUNCTIONS
# ---------------------------------------------------------
def get_logo():
    try:
        # Try to get active session for the logo from stage
        session = get_active_session()
        logo_data = session.file.get_stream('@"ML_DATASETS"."DATA"."PIC"/comply logo.jpg')
        return logo_data.read()
    except:
        return "https://i.ibb.co/Xz9R94p/complywise-logo.png"

# ---------------------------------------------------------
# 4. LOGIN PAGE UI (PIC 1 STYLE WITH BORDER)
# ---------------------------------------------------------
def show_login_page():
    st.markdown("""
        <style>
        .stApp { background-color: #f4f7f9; }
        .login-card {
            background-color: white;
            padding: 40px;
            border-radius: 15px;
            border: 1px solid #e0e6ed;
            box-shadow: 0px 10px 25px rgba(0,0,0,0.05);
        }
        .blue-panel {
            background: linear-gradient(160deg, #004a99 0%, #002d5c 100%);
            padding: 50px;
            border-radius: 15px;
            color: white;
            min-height: 520px;
            display: flex;
            flex-direction: column;
            justify-content: center;
        }
        div.stButton > button:first-child {
            border-radius: 5px;
        }
        </style>
    """, unsafe_allow_html=True)

    col_left, col_right = st.columns([1, 1.2], gap="large")

    with col_left:
        st.markdown('<div class="login-card">', unsafe_allow_html=True)
        st.image(get_logo(), width=280)
        st.write("##")

        if st.session_state.view == "login":
            input_user = st.text_input("User ID", placeholder="Enter your ID").strip()
            input_pass = st.text_input("Password", type="password", placeholder="Enter password").strip()
            
            c1, c2 = st.columns([1.5, 1])
            with c2:
                if st.button("Forgot Password?", key="fg_btn", type="secondary"):
                    st.session_state.view = "forgot"
                    st.rerun()

            if st.button("Sign In", key="login_btn", type="primary", use_container_width=True):
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
        
        st.markdown('</div>', unsafe_allow_html=True)

    with col_right:
        st.markdown(f"""
            <div class="blue-panel">
                <h1 style='color: white; font-size: 2.5rem;'>Indian Legal RAG Assistant</h1>
                <p style='color: #e0e0e0; font-size: 1.2rem;'>
                    Real-time Clinical, Financial, and Compliance Integrity. 
                    Preventing risk through continuous data validation.
                </p>
                <div style="margin-top: 30px; padding-top: 20px; border-top: 1px solid rgba(255,255,255,0.2);">
                    <p>Powered by Snowflake Cortex & ComplyWise Intelligence</p>
                </div>
            </div>
        """, unsafe_allow_html=True)

# ---------------------------------------------------------
# 5. MAIN APPLICATION (LEGAL RAG ASSISTANT)
# ---------------------------------------------------------
def show_main_app():
    # Establish Snowflake Connection inside the main app
    try:
        cnx = st.connection("snowflake")
        session = cnx.session()
    except Exception as e:
        st.error(f"⚠️ Could not connect to Snowflake: {e}")
        st.stop()

    # Sidebar
    st.sidebar.image(get_logo(), width=150)
    st.sidebar.divider()
    st.sidebar.markdown(f"**Welcome, {st.session_state.current_user}**")
    
    if st.sidebar.button("Log Out"):
        st.session_state.logged_in = False
        st.rerun()

    # Legal Assistant Content
    st.title("⚖️ Indian Legal RAG Assistant")
    st.write("---")
    
    st.success(f"Connected to Snowflake as: **{session.get_current_user()}**")
    
    # Placeholder for your RAG Logic
    query = st.chat_input("Ask a legal question...")
    if query:
        st.chat_message("user").write(query)
        st.chat_message("assistant").write("I am analyzing the legal documents in Snowflake...")

# ---------------------------------------------------------
# 6. EXECUTION FLOW
# ---------------------------------------------------------
if not st.session_state.logged_in:
    show_login_page()
else:
    show_main_app()
