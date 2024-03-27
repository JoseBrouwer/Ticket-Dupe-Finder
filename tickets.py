import pandas as pd
import re
import os
from tkinter import Tk, filedialog


def get_file_path():
    """
    Opens a file selection dialog and returns the selected file path.
    """
    root = Tk()
    root.withdraw()  # Hide the main window
    file_path = filedialog.askopenfilename()
    return file_path


def read_file(file_path):
    """
    Reads a file based on its extension and returns a pandas DataFrame.
    Supports CSV and Excel files.
    """
    _, file_extension = os.path.splitext(file_path)
    if file_extension in [".csv"]:
        return pd.read_csv(file_path)
    elif file_extension in [".xlsx", ".xls"]:
        return pd.read_excel(file_path)
    else:
        raise ValueError("Unsupported file type. Please use a CSV or Excel file.")


# Path to your file - adjust this as necessary
# file_path = input("Enter the path to your file: ")
file_path = get_file_path()
# Check if a file was selected
if not file_path:
    print("No file selected. Exiting...")
    exit()

# Regular expression to match phone numbers of different formats
phone_number_regex = re.compile(r"(?:\d{3}|\(\d{3}\)) \d{3}-\d{4}")

# Dictionary to hold phone numbers (core digits) and their associated ticket IDs
phone_tickets_dict = {}

try:
    # Read the file into a DataFrame
    df = read_file(file_path)

    # Iterate over each row in the DataFrame
    for index, row in df.iterrows():
        subject = row["Subject"]
        ticket_id = row["Ticket ID"]

        # Search for phone numbers in the "Subject" column
        if not pd.isna(subject):  # Check if subject is not missing (NaN)
            phone_search = phone_number_regex.search(str(subject))
        if phone_search:
            phone_number = phone_search.group()
            if phone_number in phone_tickets_dict:
                # If the phone number is already there, append the ticket ID
                phone_tickets_dict[phone_number].append(ticket_id)
            else:
                # Otherwise, create a new entry in the dictionary
                phone_tickets_dict[phone_number] = [ticket_id]

    with open("tickets.txt", "w") as file:
        for phone_number, ticket_ids in phone_tickets_dict.items():
            if len(ticket_ids) > 1:
                file.write(
                    f"Phone Number: {phone_number}\nTicket IDs: {ticket_ids}\n\n"
                )

    print("Done writing ticket IDs by phone number to tickets.txt")
    os.system("pause")
except FileNotFoundError:
    print("Error: File not found.")
    os.system("pause")
except ValueError as e:
    print(e)
    os.system("pause")
