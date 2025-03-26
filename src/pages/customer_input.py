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

    agent_name = st.session_state.get("authenticated_agent", None)
    if not agent_name:
        st.error("Agent name is missing. Please log in again.")
        st.stop()

    client = connect_to_google_sheets()
    spreadsheet_url = st.secrets["agent_mapping"][agent_name]
    spreadsheet = client.open_by_url(spreadsheet_url)

    try:
        address_sheet = spreadsheet.worksheet("Address")
        house_addresses = address_sheet.col_values(1)
    except gspread.exceptions.WorksheetNotFound:
        st.error("The 'Address' sheet is missing in the spreadsheet. Please contact the admin.")
        st.stop()

    if not house_addresses:
        st.error("No house addresses found. Please add addresses to the 'Address' sheet and try again.")
        st.stop()

    if "selected_house_address" not in st.session_state:
        st.session_state["selected_house_address"] = house_addresses[0]

    st.selectbox(
        "Please Select House Address",
        options=house_addresses,
        key="selected_house_address"
    )

    house_address = st.session_state["selected_house_address"]
    try:
        worksheet = spreadsheet.worksheet(house_address)
    except gspread.exceptions.WorksheetNotFound:
        worksheet = spreadsheet.add_worksheet(title=house_address, rows="100", cols="20")
        worksheet.append_row(["Date", "Visitor Name", "Email", "Phone Number", "Need a Realtor?", "Current Address", "Comments"])

    initialize_form_state()

    def submit():
        if not st.session_state["visitor_name"] or not st.session_state["email"] or not st.session_state["phone"]:
            st.warning("Please fill in all required fields.")
        else:
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

    with st.form(key="customer_form"):
        st.text_input("Visitor Name", key="visitor_name")
        st.text_input("Email", key="email")
        st.text_input("Phone Number", key="phone")
        st.selectbox("Need a Realtor?", ["Yes", "No"], key="need_realtor")
        st.text_input("Current Address", key="current_address")
        st.form_submit_button("Submit", on_click=submit)

if __name__ == "__main__":
    main()