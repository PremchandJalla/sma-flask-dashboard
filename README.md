# Star Micronics POS Data Analysis Dashboard

This project is designed to streamline and analyze POS data from Star Micronics. By uploading `.stm` files, the system consolidates data into an Excel file with multiple sheets and performs insightful analysis to generate interactive dashboards.

## Project Workflow

1. **Upload & Parse Data**
   - The application accepts a zip file containing `.stm` files.
   - A Python script parses each `.stm` file and consolidates the data into an Excel file with three sheets:
     - **Orders**: Contains fields such as `Order Number`, `Total Price`, `Order Date Time`, `Payment Method`, `Total Amount`, `VAT Amount`, `Change Due`, `VAT Number`, and `Receipt Print ID`.
     - **Items**: Contains fields including `Order Number`, `Quantity`, `Name`, `Price`, `VAT Rate`, and `VAT Amount`.
     - **VAT Summary**: Includes fields `Order Number`, `VAT Rate`, and `Amount`.

2. **Enrich Data with External API**
   - After extracting data from `.stm` files, an API call is made to retrieve weather and game day information.
   - Two new fields, `Weather` and `Game Day`, are added to the **Orders** sheet based on the date and time of each order.

3. **Data Analysis**
   - The analysis phase has two approaches:
     - **LLM-Powered Analysis**: Leverages a fine-tuned Language Learning Model to generate insights in a fixed format by prompting the model.
     - **Pandas Data Analysis**: Uses the Pandas library to perform traditional data analysis and derive various insights from the data.

4. **Dashboard Generation**
   - The final step utilizes the Dash framework to create an interactive dashboard for data visualization.
   - The dashboard includes various insights such as:
     - Total spending by day of the week.
     - Top-selling items.
     - VAT anomalies.
     - Spending patterns based on weather and game day conditions.

## Dashboard Screenshots

Here are some screenshots of the dashboard to illustrate its functionality:

### Upload Data
![image](https://github.com/user-attachments/assets/00b62277-119c-450d-84dd-3e006948c2c4)



### Sales Insights Dashboard and Spending by Day
![image](https://github.com/user-attachments/assets/1749ff5c-79ac-4b64-a3c6-d473c71f519b)


### Top-Selling Items

![image](https://github.com/user-attachments/assets/406976a5-4c4f-4b46-ba45-431c11c43214)


## Installation & Usage

### Prerequisites
- Python 3.x
- Required Python libraries (listed in `requirements.txt`)

### Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/PremchandJalla/sma-flask-dashboard.git

2. Navigate to the project directory:

   ```bash
   cd sma-flask-dashboard

2. Run the application:

   ```bash
   python app.py
