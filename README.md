# 🧹 Universal Data Cleaner

Universal Data Cleaner is a practical Python and Streamlit app for cleaning messy CSV and Excel files, reviewing dataset quality, and exporting cleaned data for analysis.

It is designed for users working with real-world business data that may contain missing values, inconsistent formatting, duplicate rows, currency strings, and messy text fields.

## 📋 Project Overview

This app helps users:

- upload CSV and Excel files
- preview raw data before cleaning
- remove duplicate records
- trim whitespace and clean messy text values
- convert number-like strings and currency values into numeric formats
- fill missing numeric values using the column mean
- detect basic sales-related KPI columns automatically
- visualize cleaned data with charts
- export the cleaned file as CSV or Excel
- undo to the previous version before cleaning

## 🚀 Main Features

- upload multiple CSV and Excel files
- preview the first rows of each dataset
- view key summary metrics (rows, columns, missing values, duplicates)
- remove duplicate rows
- trim whitespace from text fields
- remove special characters from text content
- normalize lowercase text where needed
- convert text values like `$500`, `1,250.00`, and `500 GHS` into numeric values
- convert yes/no fields into boolean-style values
- fill missing numeric values using column averages
- detect sales-related KPI fields automatically
- select which columns to keep before export
- view bar, line, scatter, and histogram charts
- export cleaned output in CSV or Excel format
- restore the previous version with undo

## 💡 Why This Project Matters

This project demonstrates real-world data handling skills that are useful in analytics, business intelligence, and reporting work.

It combines:

- file processing
- data cleaning
- data type conversion
- missing value handling
- KPI detection
- basic visualization
- user interface design
- export workflows

## 🛠️ Tech Stack

- Python
- Pandas
- Streamlit
- Plotly
- OpenPyXL

## 📁 Project Structure

- `unicleaner1.py` - main Streamlit app
- `requirements.txt` - project dependencies
- `README.md` - project documentation

## ⚙️ Installation

1. Open the project folder in your terminal.
2. Install the required packages:

```bash
pip install -r requirements.txt
```

## ▶️ Run the App

From the project folder, run:

```bash
streamlit run unicleaner1.py
```

Then open the local URL shown in the terminal in your browser.

## 📖 How to Use

1. Upload one or more CSV or Excel files.
2. Review the preview and summary report.
3. Apply cleaning options such as whitespace removal, text cleanup, numeric conversion, or missing-value filling.
4. Choose which columns to keep before export.
5. View charts if needed.
6. Export the cleaned data as CSV or Excel.
7. Use the undo button to restore the previous raw file version if needed.

## 🧪 Example Use Cases

A user may receive a messy sales file with:

- duplicate rows
- currency symbols in numeric columns
- missing values
- inconsistent labels
- text values that should be treated as numbers

This app helps clean the file and prepare it for reporting, analysis, or upload into a dashboard.

## 🔮 Planned Improvements

- add stronger validation for broken or malformed files
- add more missing-value handling options (median, mode, custom fill)
- support multi-file merge and join workflows
- add reusable cleaning templates
- add more business KPI checks
- improve dashboard styling and layout
- add saved user workflows and audit logs

## 📄 License

This project is intended for learning, portfolio development, and practical data-cleaning use.
