# 🧹 Universal Data Cleaner

Universal Data Cleaner is a simple data-cleaning and conversion app built with Python and Streamlit.

It helps users upload CSV and Excel files, clean the data, review key metrics, visualize patterns, and export the cleaned file in a new format.

## 📋 Project Overview

This app is designed for people working with messy spreadsheet data. It makes it easier to:

-  clean up raw files
-  remove duplicate records
-  fill missing numeric values
- select useful columns
-  review key dataset information
-  create quick visual insights
- export cleaned data back into CSV or Excel

## 🚀 Main Features

-  upload multiple CSV and Excel files
-  preview the first rows of each dataset
-  remove duplicate rows
-  fill missing numeric values using the column average
-  select which columns to keep before export
-  view bar, line, scatter, and histogram charts
-  review summary statistics
-  detect common sales-related KPI columns when they exist
-  convert data into CSV or Excel format
-  download the cleaned file

## 💡 Why This Project Matters

This project shows practical data-handling skills using real tools that are widely used in analytics and business work.

It combines:

- file processing
-  data cleaning
-  data analysis
-  business KPI checks
-  data visualization
-  user interface building

## 🛠️ Tech Stack

- 🐍 Python
-  Pandas
-  Streamlit
- 📊 Plotly
- 📗 OpenPyXL

## 📁 Project Structure

- `unicleaner1.py` - 🖥️ main Streamlit app
- `requirements.txt` - 📦 project dependencies
- `README.md` - 📖 project documentation

## ⚙️ Installation

1. 📂 Open the project folder in your terminal.
2. 📦 Install the required packages:

```bash
pip install -r requirements.txt
```

## ▶️ Run the App

From the project folder, run:

```bash
streamlit run unicleaner1.py
```

Then open the local URL shown in the terminal in your browser. 🌐

## 📖 How to Use

1.  Upload one or more CSV or Excel files.
2.  Review the preview and summary report.
3.  Clean the dataset if needed.
4.  Choose which columns to keep.
5.  Turn on the visualization section if you want charts.
6.  Select the output format: CSV or Excel.
7.  Click the download button to save the cleaned file.

## 🧪 Example Use Case

A user may receive sales data in Excel format, remove duplicate entries, fill missing values, review the summary metrics, and export the cleaned data for reporting or further analysis.

## 🔮 Planned Improvements

-  improve validation for unusual or broken files
-  add stronger text-cleaning options
-  add more missing-value handling choices
-  improve dashboard styling
-  add more business KPIs and data checks
-  deploy the app online for public access

## 📄 License

This project is intended for learning, personal use, and portfolio development.
