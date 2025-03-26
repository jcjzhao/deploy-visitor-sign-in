import streamlit as st
from datetime import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials

def connect_to_google_sheets():
    """Connect to Google Sheets using credentials from Streamlit secrets."""
    try:
        creds = st.secrets["connections"]["gsheets"]
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        creds = ServiceAccountCredentials.from_json_keyfile_dict(creds, scope)
        return gspread.authorize(creds)
    except Exception as e:
        st.error(f"Failed to connect to Google Sheets: {e}")
        st.stop()

def initialize_form_state():
    """Initialize session state for form inputs."""
    for key, default in {
        "visitor_name": "",
        "email": "",
        "phone": "",
        "need_realtor": "Yes",
        "current_address": "",
    }.items():
        if key not in st.session_state:
            st.session_state[key] = default

def main():
    st.title("Coco's Open House")

    # Ensure the agent is authenticated
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
        house_addresses = [address.strip() for address in address_sheet.col_values(1)]  # Strip spaces
    except gspread.exceptions.WorksheetNotFound:
        st.error("The 'Address' sheet is missing in the spreadsheet. Please contact the admin.")
        st.stop()

    if not house_addresses:
        st.error("No house addresses found. Please add addresses to the 'Address' sheet and try again.")
        st.stop()

    # Ensure all addresses in the "Address" sheet have corresponding worksheets
    for address in house_addresses:
        sanitized_address = address.replace("/", "-").replace("\\", "-").strip()  # Sanitize address
        try:
            spreadsheet.worksheet(sanitized_address)  # Check if the worksheet exists
        except gspread.exceptions.WorksheetNotFound:
            # Create a new sheet for the address if it doesn't exist
            worksheet = spreadsheet.add_worksheet(title=sanitized_address, rows="100", cols="20")
            worksheet.append_row(["Date", "Visitor Name", "Email", "Phone Number", "Need a Realtor?", "Current Address", "Comments"])

    # Initialize the selected house address in session state
    if "selected_house_address" not in st.session_state:
        st.session_state["selected_house_address"] = house_addresses[0]  # Default to the first address

    # Dropdown for house address selection
    st.selectbox(
        "Please Select House Address",
        options=house_addresses,
        key="selected_house_address"
    )

    # Get the selected house address
    house_address = st.session_state["selected_house_address"]

    # Form submission logic
    def submit():
        # Ensure the worksheet exists before submitting data
        try:
            worksheet = spreadsheet.worksheet(house_address)
        except gspread.exceptions.WorksheetNotFound:
            st.error(f"Worksheet for '{house_address}' is missing. Please contact the admin.")
            return

        # Validate required fields
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
                "",  # Leave the "Comments" column empty
            ]
            worksheet.append_row(new_row)

            # Clear the input fields after successful submission
            st.session_state["visitor_name"] = ""
            st.session_state["email"] = ""
            st.session_state["phone"] = ""
            st.session_state["need_realtor"] = "Yes"
            st.session_state["current_address"] = ""

    # Form for customer input
    with st.form(key="customer_form"):
        st.text_input("Visitor Name", key="visitor_name")
        st.text_input("Email", key="email")
        st.text_input("Phone Number", key="phone")
        st.selectbox("Need a Realtor?", ["Yes", "No"], key="need_realtor")
        st.text_input("Current Address", key="current_address")
        st.form_submit_button("Submit", on_click=submit)

if __name__ == "__main__":
    main()