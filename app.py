import streamlit as st
from src.pages.login import main as login_main
from src.pages.customer_input import main as customer_input_main

import sys
from pathlib import Path

# Add the parent directory of src to the Python path
sys.path.append(str(Path(__file__).resolve().parent.parent))

def main():
    # Simplify the interface by removing unnecessary titles
    st.set_page_config(page_title="Coco's Open House Sign-In Portal", layout="centered")

    # Initialize session state for page navigation
    if "page" not in st.session_state:
        st.session_state["page"] = "login"  # Default to the Login page

    # Centralized check for authentication
    if st.session_state["page"] != "login" and "authenticated_agent" not in st.session_state:
        st.error("You must log in first.")
        st.session_state["page"] = "login"
        st.rerun()

    # Navigation logic based on session state
    if st.session_state["page"] == "login":
        login_main()  # Call the Login page
    elif st.session_state["page"] == "customer_input":
        customer_input_main()  # Call the Customer Input page
    else:
        # Fallback for unexpected page values
        st.error("Page not found. Please log in again.")
        st.session_state["page"] = "login"
        st.rerun()

if __name__ == "__main__":
    main()