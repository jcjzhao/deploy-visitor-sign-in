import streamlit as st

def main():
    st.title("Coco's Open House")
    st.write("Please log in with your credentials to access the portal.")

    # Input fields for username and password
    st.text_input("Username", key="username")
    st.text_input("Password", type="password", key="password")
    login_button = st.button("Login")

    if login_button:
        try:
            # Retrieve credentials from secrets
            credentials = st.secrets.get("credentials", {})
            username = st.session_state.get("username", "")
            password = st.session_state.get("password", "")

            # Validate credentials
            if username in credentials and credentials[username]["password"] == password:
                # Store authenticated agent's name in session state
                st.session_state["authenticated_agent"] = credentials[username]["name"]
                st.session_state["page"] = "customer_input"
                st.rerun()  # Navigate to the customer input page
            else:
                st.error("Invalid username or password.")
        except KeyError:
            st.error("Credentials are not properly configured. Please contact the admin.")

if __name__ == "__main__":
    main()