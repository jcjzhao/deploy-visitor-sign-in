import streamlit as st
from datetime import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials

def connect_to_google_sheets():
    try:
        creds = st.secrets["connections"]["gsheets"]
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        creds = ServiceAccountCredentials.from_json_keyfile_dict(creds, scope)
        return gspread.authorize(creds)
    except Exception as e:
        st.error(f"Failed to connect to Google Sheets: {e}")
        st.stop()

def main():
    # Add a consistent title for the app
    st.title("Coco's Open House Sign-In Portal")

    # Retrieve agent name from session state
    agent_name = st.session_state.get("authenticated_agent", None)

    if not agent_name:
        st.error("Agent name is missing. Please log in again.")
        st.stop()

    # Connect to Google Sheets
    client = connect_to_google_sheets()
    spreadsheet_url = st.secrets["agent_mapping"][agent_name]
    spreadsheet = client.open_by_url(spreadsheet_url)

    # Fetch the list of house addresses from the "Address" sheet
    try:
        address_sheet = spreadsheet.worksheet("Address")
        house_addresses = address_sheet.col_values(1)  # Get all house addresses from the first column
    except gspread.exceptions.WorksheetNotFound:
        st.error("The 'Address' sheet is missing in the spreadsheet. Please contact the admin.")
        st.stop()

    if not house_addresses:
        st.error("No house addresses found. Please add addresses to the 'Address' sheet and try again.")
        st.stop()

    # Initialize session state for selected house address
    if "selected_house_address" not in st.session_state:
        st.session_state["selected_house_address"] = house_addresses[0]  # Default to the first address

    # Dropdown for house address selection
    st.selectbox(
        "Please Select House Address",
        options=house_addresses,
        key="selected_house_address"
    )

    # Ensure the selected house address has a corresponding sheet
    house_address = st.session_state["selected_house_address"]
    try:
        worksheet = spreadsheet.worksheet(house_address)
    except gspread.exceptions.WorksheetNotFound:
        # Create a new sheet for the house address if it doesn't exist
        worksheet = spreadsheet.add_worksheet(title=house_address, rows="100", cols="20")
        worksheet.append_row(["Date", "Visitor Name", "Email", "Phone Number", "Need a Realtor?", "Current Address", "Comments"])

    # Initialize session state for form inputs
    if "visitor_name" not in st.session_state:
        st.session_state["visitor_name"] = ""
    if "email" not in st.session_state:
        st.session_state["email"] = ""
    if "phone" not in st.session_state:
        st.session_state["phone"] = ""
    if "need_realtor" not in st.session_state:
        st.session_state["need_realtor"] = "Yes"
    if "current_address" not in st.session_state:
        st.session_state["current_address"] = ""
    if "comments" not in st.session_state:
        st.session_state["comments"] = ""

    # Function to handle form submission
    def submit():
        if not st.session_state["visitor_name"] or not st.session_state["email"] or not st.session_state["phone"]:
            st.warning("Please fill in all required fields.")
        else:
            # Prepare the data to be added
            current_date = datetime.now().strftime("%Y-%m-%d")
            new_row = [
                current_date,
                st.session_state["visitor_name"],
                st.session_state["email"],
                st.session_state["phone"],
                st.session_state["need_realtor"],
                st.session_state["current_address"],
                st.session_state["comments"],
            ]

            # Append the data to the worksheet
            worksheet.append_row(new_row)

            # Clear the input fields (but keep the selected house address unchanged)
            st.session_state["visitor_name"] = ""
            st.session_state["email"] = ""
            st.session_state["phone"] = ""
            st.session_state["need_realtor"] = "Yes"
            st.session_state["current_address"] = ""
            st.session_state["comments"] = ""

    # Form for customer input
    with st.form(key="customer_form"):
        st.text_input("Visitor Name", key="visitor_name")
        st.text_input("Email", key="email")
        st.text_input("Phone Number", key="phone")
        st.selectbox("Need a Realtor?", ["Yes", "No"], key="need_realtor")
        st.text_input("Current Address", key="current_address")  # New field
        st.text_area("Comments", key="comments")

        submit_button = st.form_submit_button("Submit", on_click=submit)

if __name__ == "__main__":
    main()