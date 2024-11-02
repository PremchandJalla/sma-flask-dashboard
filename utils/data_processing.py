# utils/data_processing.py

import pandas as pd
import random
from utils.parse_stm import parse_stm  # Import the parse_stm function

def get_weather_and_game_day():
    """
    Function to generate random weather and game day data.
    This can be replaced with API calls in the future.
    """
    weather_options = ["Sunny", "Rainy", "Cold"]
    game_day_options = ["Yes", "No"]
    
    weather = random.choice(weather_options)
    game_day = random.choice(game_day_options)
    
    return weather, game_day

def process_stm_files(all_data, output_file="orders_data.xlsx"):
    """
    Processes parsed .stm data and saves it into an Excel file with multiple sheets.
    """
    orders_data = []
    items_data = []
    vat_summary_data = []

    for parsed_data in all_data:
        # Ensure each entry in all_data is a dictionary
        if not isinstance(parsed_data, dict):
            print("Skipping invalid data entry; not a dictionary:", parsed_data)
            continue

        # Check if Order Number is valid (non-empty and non-None)
        if parsed_data.get("order_number"):
            # Get dummy weather and game day data
            weather, game_day = get_weather_and_game_day()

            # Populate orders sheet data with Weather and Game Day
            order_entry = {
                "Order Number": parsed_data["order_number"],
                "Total Price": parsed_data["total_price"],
                "Order Date Time": parsed_data["order_date_time"],
                "Payment Method": parsed_data["payment_method"],
                "Total Amount": parsed_data["total_amount"],
                "VAT Amount": parsed_data["vat_amount"],
                "Change Due": parsed_data["change_due"],
                "VAT Number": parsed_data["vat_number"],
                "Receipt Print ID": parsed_data["receipt_print_id"],
                "Weather": weather,
                "Game Day": game_day
            }
        else:
            # Populate order data without Weather and Game Day for empty Order Number
            order_entry = {
                "Order Number": parsed_data["order_number"],
                "Total Price": parsed_data["total_price"],
                "Order Date Time": parsed_data["order_date_time"],
                "Payment Method": parsed_data["payment_method"],
                "Total Amount": parsed_data["total_amount"],
                "VAT Amount": parsed_data["vat_amount"],
                "Change Due": parsed_data["change_due"],
                "VAT Number": parsed_data["vat_number"],
                "Receipt Print ID": parsed_data["receipt_print_id"],
                "Weather": "",  # Leave Weather empty
                "Game Day": ""  # Leave Game Day empty
            }

        # Debugging: Print order entry for verification
        print("Order Entry:", order_entry)

        orders_data.append(order_entry)

        # Populate items sheet data
        for item in parsed_data["items"]:
            item_entry = {
                "Order Number": parsed_data["order_number"],
                "Quantity": item["quantity"],
                "Name": item["name"],
                "Price": item["price"],
                "VAT Rate": item["vat_rate"],
                "VAT Amount": item["vat_amount"]
            }
            items_data.append(item_entry)

        # Populate VAT summary sheet data
        for vat in parsed_data["vat_summary"]:
            vat_summary_entry = {
                "Order Number": parsed_data["order_number"],
                "VAT Rate": vat["vat_rate"],
                "Amount": vat["amount"]
            }
            vat_summary_data.append(vat_summary_entry)

    # Create DataFrames and save to Excel
    orders_df = pd.DataFrame(orders_data)
    items_df = pd.DataFrame(items_data)
    vat_summary_df = pd.DataFrame(vat_summary_data)

    # Debugging: Print the columns and first few rows of the orders_df DataFrame
    print("Orders DataFrame Columns:", orders_df.columns)
    print("Orders DataFrame Sample Data:")
    print(orders_df.head())

    with pd.ExcelWriter(output_file) as writer:
        orders_df.to_excel(writer, sheet_name="Orders", index=False)
        items_df.to_excel(writer, sheet_name="Items", index=False)
        vat_summary_df.to_excel(writer, sheet_name="VAT Summary", index=False)

    print(f"Data successfully saved to {output_file}")
    return output_file
