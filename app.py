import streamlit as st
from src.pages.login import main as login_main
from src.pages.customer_input import main as customer_input_main

import sys
from pathlib import Path

# Add the parent directory of src to the Python path
sys.path.append(str(Path(__file__).resolve().parent.parent))

def main():
    st.set_page_config(page_title="Coco's Open House", layout="centered")

    # Initialize session state for page navigation
    if "page" not in st.session_state:
        st.session_state["page"] = "login"

    # Centralized authentication check
    if st.session_state["page"] != "login" and "authenticated_agent" not in st.session_state:
        st.error("You must log in first.")
        st.session_state["page"] = "login"
        st.rerun()

    # Navigation logic
    if st.session_state["page"] == "login":
        login_main()
    elif st.session_state["page"] == "customer_input":
        customer_input_main()
    else:
        st.warning("Unexpected page. Redirecting to login...")
        st.session_state["page"] = "login"
        st.rerun()

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")