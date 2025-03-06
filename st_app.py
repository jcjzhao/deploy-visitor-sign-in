import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import os
from datetime import datetime
import json

def load_config():
    with open("config.json") as config_file:
        return json.load(config_file)

def connect_to_google_sheets(creds_path, scope):
    try:
        creds = ServiceAccountCredentials.from_json_keyfile_name(creds_path, scope)
        return gspread.authorize(creds)
    except Exception as e:
        st.error(f"Failed to connect to Google Sheets: {e}")
        st.stop()

def fetch_addresses(sheet):
    return sheet.col_values(1)

def main():
    config = load_config()

    st.title("Visitor Sign-In Portal")
    st.markdown("Enter the details of the new visitor below.")

    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds_path = os.path.join("credentials", "credentials.json")
    client = connect_to_google_sheets(creds_path, scope)
    spreadsheet_url = config["spreadsheet_url"]

    spreadsheet = client.open_by_url(spreadsheet_url)
    addresses_sheet = spreadsheet.get_worksheet(0)
    addresses = fetch_addresses(addresses_sheet)

    with st.form(key="visitor_form"):
        address = st.selectbox("Address", options=addresses)
        visitor_name = st.text_input(label="Visitor Name")
        email = st.text_input(label="Email")
        phone = st.text_input(label="Phone Number")
        need_realtor = st.selectbox("Need a Realtor?", options=["Yes", "No"])
        comments = st.text_area(label="Comments")

        submit_button = st.form_submit_button(label="Submit Details")

        if submit_button:
            if not address or not visitor_name or not email or not phone:
                st.warning("Ensure all mandatory fields are filled.")
                st.stop()
            else:
                current_date = datetime.now().strftime("%Y-%m-%d")
                visitor_data = pd.DataFrame(
                    [
                        {
                            "Date": current_date,
                            "Address": address,
                            "Visitor Name": visitor_name,
                            "Email": email,
                            "Phone Number": phone,
                            "Need a Realtor?": need_realtor,
                            "Comments": comments,
                        }
                    ]
                )

                try:
                    sheet = spreadsheet.worksheet(address)
                except gspread.exceptions.WorksheetNotFound:
                    sheet = spreadsheet.add_worksheet(title=address, rows="100", cols="20")
                    sheet.append_row(["Date", "Address", "Visitor Name", "Email", "Phone Number", "Need a Realtor?", "Comments"])

                existing_data = pd.DataFrame(sheet.get_all_records()).dropna(how="all")
                updated_df = pd.concat([existing_data, visitor_data], ignore_index=True)
                sheet.append_row(visitor_data.iloc[0].tolist())

                st.success("Visitor details successfully submitted!")

if __name__ == "__main__":
    main()