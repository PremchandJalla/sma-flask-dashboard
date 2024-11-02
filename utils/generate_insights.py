import pandas as pd
import json

def calculate_insights(data_file):
    # Load the dataset
    data = pd.ExcelFile(data_file)
    orders_df = data.parse('Orders')
    items_df = data.parse('Items')
    vat_summary_df = data.parse('VAT Summary')

    # Calculate total revenue and average order value
    orders_df['Total Amount'] = orders_df['Total Amount'].str.replace(' EUR', '').astype(float)
    total_revenue = orders_df['Total Amount'].sum()
    average_order_value = orders_df['Total Amount'].mean()

    # Identify top-selling items
    items_df['Quantity'] = items_df['Quantity'].astype(int)
    top_selling_items = items_df.groupby('Name')['Quantity'].sum().sort_values(ascending=False).head(5).to_dict()

    # Spending by day of the week
    orders_df['Order Date Time'] = pd.to_datetime(orders_df['Order Date Time'])
    spending_by_day = orders_df.groupby(orders_df['Order Date Time'].dt.day_name())['Total Amount'].sum().to_dict()

    # Detect VAT anomalies (e.g., zero VAT amounts or unusual rates)
    vat_summary_df['Amount'] = vat_summary_df['Amount'].str.replace(' EUR', '').astype(float)
    vat_anomalies = vat_summary_df[vat_summary_df['Amount'] == 0.0].to_dict(orient='records')

    # Average total amount by weather condition and game day
    avg_by_conditions = (
        orders_df.groupby(['Weather', 'Game Day'])['Total Amount']
        .mean()
        .unstack(fill_value=0)
        .round(2)
        .to_dict()
    )

    # Ensure all dictionary keys are strings
    insights = {
        "total_revenue": f"€{total_revenue:.2f}",
        "average_order_value": f"€{average_order_value:.2f}",
        "top_selling_items": top_selling_items,
        "spending_by_day": spending_by_day,
        "vat_anomalies": vat_anomalies,
        "avg_by_conditions": {str(k): v for k, v in avg_by_conditions.items()}
    }

    # Save insights to output.json
    with open('output.json', 'w') as f:
        json.dump(insights, f, indent=4)

    return insights
