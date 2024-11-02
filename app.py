from flask import Flask, request, jsonify, redirect, url_for, flash, render_template, send_file
import os
import zipfile
import pandas as pd
from utils.parse_stm import parse_stm
from utils.data_processing import process_stm_files
from utils.nvidia_mistral import generate_insight
from utils.generate_insights import calculate_insights
from dash import Dash, html, dcc, dash_table  # Import dash_table from dash
import plotly.express as px
import json

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Configuration
UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["ENRICHED_DATA_FILE"] = "data/enriched_orders_data.xlsx"
app.config["ORIGINAL_DATA_FILE"] = "/Users/premchandjalla/Desktop/SMA FLASK APP/orders_data.xlsx"
NVIDIA_API_KEY = "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"

# Ensure upload and data folders exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs("data", exist_ok=True)

# Prompts for NVIDIA insights generation
prompts = {
    "total_revenue": "Calculate the total revenue and average order value from the dataset.",
    "top_selling_items": "Identify the top-selling items and the number of times each was sold.",
    "spending_by_day": "Provide the total spending by day of the week.",
    "vat_anomalies": "Detect any anomalies in the VAT data and list possible issues.",
    "avg_by_conditions": "Calculate the average total amount by weather condition and game day.",
}

# Function to create Dash app and integrate it with Flask
def create_dashboard(server):
    dash_app = Dash(
        __name__,
        server=server,
        routes_pathname_prefix='/dashboard/'
    )

    # Load insights data from output.json for the dashboard
    try:
        with open('output.json', 'r') as f:
            data = json.load(f)
    except FileNotFoundError:
        data = {}

    # Prepare data for visualization if available
    spending_by_day_df = pd.DataFrame(list(data.get('spending_by_day', {}).items()), columns=['Day', 'Total Spending'])
    top_selling_items_df = pd.DataFrame(list(data.get('top_selling_items', {}).items()), columns=['Item', 'Quantity Sold'])
    vat_anomalies_df = pd.DataFrame(data.get('vat_anomalies', []))

    # Process avg_by_conditions data if it exists
    avg_by_conditions_data = data.get('avg_by_conditions', {})
    avg_by_conditions_df = pd.DataFrame.from_dict(avg_by_conditions_data, orient='index').reset_index()

    # Dynamically adjust column names based on DataFrame structure
    if avg_by_conditions_df.shape[1] == 4:
        avg_by_conditions_df.columns = ['Game Day', 'Cold', 'Rainy', 'Sunny']
    elif avg_by_conditions_df.shape[1] == 2:
        avg_by_conditions_df.columns = ['Game Day', 'Average Spending']
    else:
        avg_by_conditions_df.columns = [f"Column {i+1}" for i in range(avg_by_conditions_df.shape[1])]
        print("Warning: avg_by_conditions data does not have the expected structure.")

    # Check if 'Game Day' column is available before creating the graph
    try:
        if 'Game Day' in avg_by_conditions_df.columns:
            melted_avg_by_conditions_df = avg_by_conditions_df.melt(
                id_vars=['Game Day'], var_name='Condition', value_name='Average Spending'
            )
            avg_by_conditions_figure = px.bar(
                melted_avg_by_conditions_df,
                x='Condition', y='Average Spending', color='Game Day', barmode='group',
                title="Average Spending by Weather Condition and Game Day"
            )
        else:
            print("Warning: 'Game Day' column is missing in avg_by_conditions data. Skipping related chart.")
            avg_by_conditions_figure = None
    except Exception as e:
        print(f"Error creating avg_by_conditions chart: {e}")
        avg_by_conditions_figure = None

    dash_app.layout = html.Div([
        html.H1("Sales Insights Dashboard"),
        
        html.Div([
            html.H2(f"Total Revenue: {data.get('total_revenue', 'N/A')}"),
            html.H2(f"Average Order Value: {data.get('average_order_value', 'N/A')}")
        ], style={'text-align': 'center'}),
        
        html.Div([
            html.H3("Total Spending by Day of the Week"),
            dcc.Graph(id='spending-by-day', figure=px.bar(spending_by_day_df, x='Day', y='Total Spending',
                                                          title="Total Spending by Day"))
        ]),

        html.Div([
            html.H3("Top Selling Items"),
            dcc.Graph(id='top-selling-items', figure=px.bar(top_selling_items_df, x='Item', y='Quantity Sold',
                                                            title="Top Selling Items"))
        ]),

        html.Div([
            html.H3("VAT Anomalies"),
            dash_table.DataTable(
                id='vat-anomalies-table',
                columns=[{"name": i, "id": i} for i in vat_anomalies_df.columns],
                data=vat_anomalies_df.to_dict('records'),
                page_size=10,
                style_table={'height': '300px', 'overflowY': 'auto'}
            )
        ]),

        html.Div([
            html.H3("Average Spending by Weather Condition and Game Day"),
            dcc.Graph(id='avg-by-conditions', figure=avg_by_conditions_figure) if avg_by_conditions_figure else html.P("No data available for Average Spending by Weather Condition and Game Day")
        ])
    ])

    return dash_app

create_dashboard(app)

@app.route("/", methods=["GET", "POST"])
def upload_file():
    if request.method == "POST":
        print("File upload received.")
        
        file = request.files.get("file")
        if not file or not file.filename.endswith(".zip"):
            flash("Please upload a valid zip file.")
            print("Invalid file format or missing file.")
            return redirect(request.url)

        file_path = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
        file.save(file_path)
        extracted_files = []
        
        try:
            with zipfile.ZipFile(file_path, 'r') as zip_ref:
                zip_ref.extractall("data/")
                extracted_files = zip_ref.namelist()
                print(f"Files extracted: {extracted_files}")
        except zipfile.BadZipFile:
            flash("Invalid zip file.")
            print("Error: Bad zip file.")
            return redirect(request.url)
        
        all_data = []
        for filename in extracted_files:
            if filename.startswith("__MACOSX") or filename.startswith("._"):
                print(f"Skipping hidden macOS file: {filename}")
                continue

            if filename.endswith(".stm"):
                try:
                    with open(os.path.join("data", filename), 'r', encoding='utf-8') as stm_file:
                        content = stm_file.read()
                        parsed_data = parse_stm(content)
                        all_data.append(parsed_data)
                        print(f"Parsed data for {filename}: {parsed_data}")
                except UnicodeDecodeError as e:
                    print(f"Error parsing {filename}: {e}")
                    flash(f"Error parsing file {filename}: {e}")
                    continue
                except Exception as e:
                    print(f"General error parsing {filename}: {e}")
                    flash(f"Error parsing file {filename}: {e}")
                    continue

        output_file = os.path.join(app.config["UPLOAD_FOLDER"], "orders_data.xlsx")
        try:
            process_stm_files(all_data, output_file)
            print("Data successfully processed and saved to Excel.")
        except Exception as e:
            flash(f"Error processing data to Excel: {e}")
            print(f"Error processing data to Excel: {e}")
            return redirect(request.url)

        # Clean up uploaded file
        os.remove(file_path)
        print("Uploaded zip file removed after processing.")

        # Generate insights
        insights = calculate_insights(output_file)
        with open("output.json", "w") as f:
            json.dump(insights, f, indent=4)
        print("Insights generated and saved to output.json.")

        # Redirect to the dashboard to view insights
        return redirect(url_for("dashboard"))

    return render_template("upload.html")


@app.route("/generate-insights-llm", methods=["GET"])
def generate_insights_llm():
    insights = {}
    for key, prompt in prompts.items():
        try:
            print(f"Sending prompt for '{key}': {prompt}")
            insight = generate_insight(prompt, NVIDIA_API_KEY)
            print(f"Received insight for '{key}':\n{insight}\n")
            insights[key] = insight
        except Exception as e:
            error_message = f"Error generating insight for '{key}': {str(e)}"
            print(error_message)
            insights[key] = error_message
    return jsonify(insights)


@app.route("/generate-insights", methods=["GET"])
def generate_insights():
    data_file = os.path.join(app.config["UPLOAD_FOLDER"], "orders_data.xlsx")
    if not os.path.exists(data_file):
        return jsonify({"error": "Data file not found. Please upload and process the data first."}), 404

    insights = calculate_insights(data_file)
    with open("output.json", "w") as f:
        json.dump(insights, f, indent=4)
    for key, value in insights.items():
        print(f"{key}: {value}")
    return jsonify(insights)


@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")


@app.route("/download-enriched-data")
def download_enriched_data():
    enriched_file_path = app.config["ENRICHED_DATA_FILE"]
    if os.path.exists(enriched_file_path):
        return send_file(enriched_file_path, as_attachment=True)
    else:
        flash("Enriched data file not found.")
        print("Enriched data file not found.")
        return redirect(url_for("upload_file"))


if __name__ == "__main__":
    app.run(debug=True)
