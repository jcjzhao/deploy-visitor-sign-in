import streamlit as st

def main():
    st.title("Coc's Open House Sign-In Portal")  # Add a consistent title

    # Input fields for username and password
    st.text_input("Username", key="username")
    st.text_input("Password", type="password", key="password")
    login_button = st.button("Login")

    if login_button:
        # Validate credentials from secrets
        credentials = st.secrets.get("credentials", {})
        username = st.session_state.get("username", "")
        password = st.session_state.get("password", "")

        if username in credentials and credentials[username]["password"] == password:
            # Store the authenticated agent's name in session state
            st.session_state["authenticated_agent"] = credentials[username]["name"]
            st.session_state["page"] = "customer_input"  # Navigate to the Customer Input page
            st.rerun()  # Trigger a rerun to navigate to the next page
        else:
            st.error("Invalid username or password.")

if __name__ == "__main__":
    main()