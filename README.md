# Open House Sign-In Portal

Open House Sign-In Portal is a web application built with [Streamlit](https://streamlit.io/) that allows real estate agents to manage visitor sign-ins for open houses. Agents can select a house address, collect visitor details, and store the data in Google Sheets for easy access and management.

---

## **Features**

- **Agent Login**: Secure login for agents using credentials stored in `secrets.toml`.
- **Address Selection**: Agents can select the house address for the open house directly on the visitor input page.
- **Visitor Sign-In**: Collect visitor details such as name, email, phone number, current address, and whether they need a realtor.
- **Google Sheets Integration**: Automatically stores visitor data in a Google Sheet. New sheets are created automatically for new house addresses.
- **Streamlined Workflow**: Combines address selection and visitor input into a single page for simplicity.

---

## **Project Structure**

```
visitor-sign-in
│   ├── app.py                # Main entry point of the Streamlit application
├── src
│   ├── pages
│   │   ├── address_input.py  # Interface for users to input their Google Sheets address
│   │   └── customer_input.py  # Interface for clients to input their information
├── requirements.txt          # Lists the dependencies required for the project
└── README.md                 # Documentation for the project
```

## **Setup Instructions**

### **1. Clone the Repository**
```bash
git clone <repository-url>
cd visitor-sign-in
```

2. **Install dependencies**:
   It is recommended to create a virtual environment before installing the dependencies.
   ```
   pip install -r requirements.txt
   ```

3. **Set up Google Sheets API**:
   - Create a project in the Google Cloud Console.
   - Enable the Google Sheets API and create credentials (Service Account).
   - Download the JSON key file and store the credentials in a secure location.
   - Add the credentials to your Streamlit secrets.

   Example `secrets.toml` file:
   ```toml
   [connections.gsheets]
   type = "service_account"
   project_id = "your-project-id"
   private_key_id = "your-private-key-id"
   private_key = "-----BEGIN PRIVATE KEY-----\nYOUR_PRIVATE_KEY\n-----END PRIVATE KEY-----\n"
   client_email = "your-service-account-email@your-project-id.iam.gserviceaccount.com"
   client_id = "your-client-id"
   auth_uri = "https://accounts.google.com/o/oauth2/auth"
   token_uri = "https://oauth2.googleapis.com/token"
   auth_provider_x509_cert_url = "https://www.googleapis.com/oauth2/v1/certs"
   client_x509_cert_url = "https://www.googleapis.com/robot/v1/metadata/x509/your-service-account-email%40your-project-id.iam.gserviceaccount.com"

   [credentials]
   "john_doe" = { password = "password123", name = "John Doe" }
   "jane_smith" = { password = "securepass456", name = "Jane Smith" }

   [agent_mapping]
   "John Doe" = "https://docs.google.com/spreadsheets/d/your-spreadsheet-id"
   "Jane Smith" = "https://docs.google.com/spreadsheets/d/your-spreadsheet-id"
   ```

4. **Run the application**:
   ```
   streamlit run app.py
   ```

## Usage Guidelines

- Upon launching the application, users will be prompted to input their Google Sheets address.
- After entering the address, users can navigate to the customer input page to fill in visitor details.
- The application will save the visitor information to the specified Google Sheets.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any enhancements or bug fixes.