import streamlit as st
import pandas as pd
import gspread

# Set page title and description
st.title("CSV and Google Sheets Data Merger")
st.write("Upload multiple CSV files, select columns, and merge with Google Sheets data")

# Create a file uploader for multiple CSV files
uploaded_files = st.file_uploader("Choose one or more CSV files", type=["csv"], accept_multiple_files=True)

# Create input fields for the user's Google Sheets URL
google_sheets_url = st.text_input("Enter Google Sheets URL")

# Initialize an empty DataFrame to store merged data
merged_data = pd.DataFrame()

# Check if CSV files are uploaded
if uploaded_files:
    for uploaded_file in uploaded_files:
        # Read the uploaded CSV file into a DataFrame
        df = pd.read_csv(uploaded_file)

        # Allow the user to select columns to include
        selected_columns = st.multiselect(f"Select columns from {uploaded_file.name}", df.columns.tolist())

        if selected_columns:
            # Filter the DataFrame based on selected columns
            selected_data = df[selected_columns]

            # Append the selected data to the merged data
            merged_data = pd.concat([merged_data, selected_data], axis=1)

# Check if a Google Sheets URL is provided
if google_sheets_url:
    try:
        # Authenticate with Google Sheets using the gspread library and service account JSON key
        gc = gspread.service_account(filename="acc.json")

        # Open the Google Sheet by URL
        worksheet = gc.open_by_url(google_sheets_url).sheet1

        # Convert the merged data DataFrame to a list of lists for writing
        data_to_write = merged_data.values.tolist()

        # Write the data to the Google Sheet starting from cell A1
        worksheet.clear()
        worksheet.insert_rows(data_to_write, 1)

        st.success("Merged data successfully written to Google Sheets.")

    except Exception as e:
        st.error(f"An error occurred while writing data to Google Sheets: {str(e)}")

# Display the merged data
if not merged_data.empty:
    st.subheader("Merged Data:")
    st.dataframe(merged_data)
