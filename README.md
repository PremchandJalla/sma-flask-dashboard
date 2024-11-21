# Star Micronics POS Data Analysis Dashboard

This project is designed to streamline and analyze POS data from Star Micronics. By uploading `.stm` files, the system consolidates data into an Excel file with multiple sheets and performs insightful analysis to generate interactive dashboards. 

Additionally, the application now supports **inventory prediction** and **purchase order (PO) generation** based on inventory data.

---

## Project Workflow

### 1. **Upload & Parse Data**
- The application accepts a zip file containing `.stm` files.
- A Python script parses each `.stm` file and consolidates the data into an Excel file with three sheets:
  - **Orders**: Contains fields such as `Order Number`, `Total Price`, `Order Date Time`, `Payment Method`, `Total Amount`, `VAT Amount`, `Change Due`, `VAT Number`, and `Receipt Print ID`.
  - **Items**: Contains fields including `Order Number`, `Quantity`, `Name`, `Price`, `VAT Rate`, and `VAT Amount`.
  - **VAT Summary**: Includes fields `Order Number`, `VAT Rate`, and `Amount`.

---

### 2. **Enrich Data with External API**
- After extracting data from `.stm` files, an API call is made to retrieve weather and game day information.
- Two new fields, `Weather` and `Game Day`, are added to the **Orders** sheet based on the date and time of each order.

---

### 3. **Data Analysis**
The analysis phase has two approaches:
1. **LLM-Powered Analysis**: Leverages a fine-tuned Language Learning Model to generate insights in a fixed format by prompting the model.
2. **Pandas Data Analysis**: Uses the Pandas library to perform traditional data analysis and derive various insights from the data.

---

### 4. **Dashboard Generation**
The final step utilizes the Dash framework to create an interactive dashboard for data visualization. Key insights include:
- **Sales Insights**: Total spending by day of the week.
- **Top-Selling Items**: Identification of the most popular items.
- **VAT Anomalies**: Highlights discrepancies in VAT reporting.
- **Spending Patterns**: Analysis of sales trends based on weather and game day conditions.

---

### 5. **Inventory Prediction**
- A machine learning model predicts future inventory requirements based on historical sales data.
- Predictions consider factors such as seasonal trends, weather conditions, and game day impacts.
- Inventory forecasts help optimize stock levels, reducing overstocking and shortages.

#### Example Output:
- Predicted demand for each item over the next week or month.
- Insights into potential out-of-stock scenarios.

---

### 6. **Purchase Order (PO) Generation**
- Automatically generates purchase orders based on inventory predictions and predefined thresholds.
- POs are tailored to ensure optimal stock replenishment.
- Each PO includes:
  - **Item Name**
  - **Quantity Required**
  - **Supplier Details**
  - **Reorder Level**

#### Example Output:
- Downloadable PDF or Excel file containing the PO details for suppliers.

---

## Dashboard Screenshots

### Upload Data
![image](https://github.com/user-attachments/assets/00b62277-119c-450d-84dd-3e006948c2c4)

### Sales Insights Dashboard
![image](https://github.com/user-attachments/assets/1749ff5c-79ac-4b64-a3c6-d473c71f519b)

### Top-Selling Items
![image](https://github.com/user-attachments/assets/406976a5-4c4f-4b46-ba45-431c11c43214)

### Inventory Prediction
![image](https://github.com/user-attachments/assets/7d26855e-5e4b-452d-b566-1846e4180d5f)


### Purchase Order (PO) Generation
![image](https://github.com/user-attachments/assets/b01cf5eb-c62c-4ff5-9549-86f9df98fcc0)

![image](https://github.com/user-attachments/assets/de77a651-9718-40db-9c63-30108db385d2)

---

## Installation & Usage

### Prerequisites
- Python 3.x
- Required Python libraries (listed in `requirements.txt`)

---

### Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/PremchandJalla/sma-flask-dashboard.git
