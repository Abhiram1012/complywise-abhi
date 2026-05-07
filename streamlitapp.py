import streamlit as st

st.set_page_config(
    page_title="ComplyWise Login",
    page_icon="🔒",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# FULL HEADER + TOOLBAR REMOVAL
st.markdown("""
<style>

/* Hide Streamlit Header */
header {
    visibility: hidden;
}

/* Hide Main Menu */
#MainMenu {
    visibility: hidden;
}

/* Hide Footer */
footer {
    visibility: hidden;
}

/* Remove top blank space */
.block-container {
    padding-top: 0rem !important;
    margin-top: 0rem !important;
}

/* Remove toolbar */
[data-testid="stToolbar"] {
    display: none;
}

/* Remove decoration */
[data-testid="stDecoration"] {
    display: none;
}

/* Remove status widget */
[data-testid="stStatusWidget"] {
    display: none;
}

/* Remove sidebar collapsed control */
[data-testid="collapsedControl"] {
    display: none;
}

</style>
""", unsafe_allow_html=True)
