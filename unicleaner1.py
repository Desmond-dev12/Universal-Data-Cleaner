import os
import io
import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="Universal Data Cleaner", layout="wide")

# =========================
# Utility functions
# =========================

def normalize_column_name(col):
    return str(col).strip().lower().replace(" ", "_")


def remove_currency_symbols(value):
    if pd.isna(value):
        return value
    if isinstance(value, str):
        value = value.strip()
        value = value.replace("$", "").replace("GHS", "").replace(",", "")
        return value
    return value


def clean_text_series(series):
    s = series.astype(str).str.strip()
    s = s.str.replace(r"[^A-Za-z0-9\s%._-]", "", regex=True)
    return s


def convert_numeric_like_columns(df):
    df = df.copy()
    for col in df.columns:
        if df[col].dropna().empty:
            continue

        sample = df[col].dropna().astype(str)
        is_numeric_like = sample.str.contains(
            r"^\d+(\.\d+)?$|^\$\d+(\.\d+)?$|^\d+,\d+\.\d+$|^\d+\s*GHS$",
            regex=True,
            case=False,
        ).any()

        if is_numeric_like:
            df[col] = df[col].apply(remove_currency_symbols)
            df[col] = pd.to_numeric(df[col], errors="coerce")

    return df


def convert_yes_no_values(df):
    df = df.copy()
    yes_no_map = {
        "yes": True,
        "y": True,
        "true": True,
        "no": False,
        "n": False,
        "false": False,
    }

    for col in df.columns:
        sample = df[col].dropna().astype(str).str.lower()
        if sample.empty:
            continue
        if sample.str.strip().isin(yes_no_map.keys()).all():
            df[col] = sample.map(yes_no_map)
    return df


def detect_kpi_columns(df):
    sales_aliases = [
        "total_sales",
        "sales",
        "revenue",
        "total_revenue",
        "amount",
        "gross_sales",
        "total_amount",
    ]
    quantity_aliases = [
        "quantity",
        "qty",
        "total_quantity",
        "units",
        "items",
        "total_units",
    ]
    transaction_aliases = [
        "transactions",
        "total_transactions",
        "order_count",
        "num_orders",
        "orders",
    ]

    def find_column(columns, aliases):
        normalized = {str(col).strip().lower().replace(" ", "_"): col for col in columns}
        for alias in aliases:
            if alias in normalized:
                return normalized[alias]
        return None

    return {
        "sales": find_column(df.columns, sales_aliases),
        "quantity": find_column(df.columns, quantity_aliases),
        "transactions": find_column(df.columns, transaction_aliases),
    }


def get_summary(df):
    return {
        "rows": len(df),
        "columns": len(df.columns),
        "missing_values": int(df.isna().sum().sum()),
        "duplicates": int(df.duplicated().sum()),
    }


def create_snapshot(df):
    return df.copy()


def restore_snapshot(df, snapshot):
    return snapshot.copy()


def build_chart(df, chart_type, x_col, y_col):
    if chart_type == "Bar":
        return px.bar(df, x=x_col, y=y_col, title=f"{y_col} by {x_col}")
    elif chart_type == "Line":
        return px.line(df, x=x_col, y=y_col, title=f"{y_col} by {x_col}")
    elif chart_type == "Scatter":
        return px.scatter(df, x=x_col, y=y_col, title=f"{y_col} vs {x_col}")
    elif chart_type == "Histogram":
        return px.histogram(df, x=y_col, title=f"Distribution of {y_col}")
    return None


def prepare_export(df, export_type):
    buffer = io.BytesIO()

    if export_type == "CSV":
        df.to_csv(buffer, index=False)
        return buffer.getvalue(), "cleaned_data.csv", "text/csv"

    df.to_excel(buffer, index=False)
    return buffer.getvalue(), "cleaned_data.xlsx", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"


# =========================
# Main cleaning function
# =========================

def clean_dataframe(df):
    df = df.copy()

    df.columns = [normalize_column_name(col) for col in df.columns]

    for col in df.select_dtypes(include=["object"]).columns:
        df[col] = clean_text_series(df[col])

    df = convert_numeric_like_columns(df)
    df = convert_yes_no_values(df)

    numeric_cols = df.select_dtypes(include=["number"]).columns
    for col in numeric_cols:
        df[col] = df[col].fillna(df[col].mean())

    df = df.drop_duplicates()
    return df


# =========================
# App layout
# =========================

st.title("💿 Universal Data Cleaner")
st.caption("Clean messy CSV or Excel files, review summaries, visualize trends, and export cleaned data.")

uploaded_files = st.file_uploader(
    "Upload CSV or Excel files",
    type=["csv", "xlsx"],
    accept_multiple_files=True,
)

if uploaded_files:
    for uploaded_file in uploaded_files:
        file_name = uploaded_file.name
        file_ext = os.path.splitext(file_name)[1].lower()

        if file_ext == ".csv":
            df = pd.read_csv(uploaded_file)
        elif file_ext == ".xlsx":
            df = pd.read_excel(uploaded_file)
        else:
            st.error(f"Unsupported file type: {file_name}")
            continue

        snapshot = create_snapshot(df)

        st.subheader(file_name)
        st.write(f"File size: {uploaded_file.size / 1024:.2f} KB")

        with st.expander("Preview raw data", expanded=True):
            st.dataframe(df.head())

        summary = get_summary(df)
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Rows", summary["rows"])
        c2.metric("Columns", summary["columns"])
        c3.metric("Missing values", summary["missing_values"])
        c4.metric("Duplicates", summary["duplicates"])

        kpis = detect_kpi_columns(df)
        kpi_cols = st.columns(4)
        metric_count = 0

        if kpis["sales"]:
            sales_col = kpis["sales"]
            total_sales = pd.to_numeric(df[sales_col], errors="coerce").sum()
            kpi_cols[metric_count].metric("Total Sales", f"${total_sales:,.2f}")
            metric_count += 1

        if kpis["quantity"]:
            quantity_col = kpis["quantity"]
            total_quantity = pd.to_numeric(df[quantity_col], errors="coerce").sum()
            kpi_cols[metric_count].metric("Total Quantity", f"{total_quantity:,.0f}")
            metric_count += 1

        if kpis["transactions"]:
            tx_col = kpis["transactions"]
            total_transactions = pd.to_numeric(df[tx_col], errors="coerce").sum()
            kpi_cols[metric_count].metric("Total Transactions", f"{total_transactions:,.0f}")
            metric_count += 1

        if kpis["sales"] and kpis["transactions"]:
            total_sales = pd.to_numeric(df[kpis["sales"]], errors="coerce").sum()
            total_transactions = pd.to_numeric(df[kpis["transactions"]], errors="coerce").sum()
            aov = total_sales / total_transactions if total_transactions else 0
            kpi_cols[metric_count].metric("AOV", f"${aov:,.2f}")
            metric_count += 1

        if metric_count == 0:
            st.info("No sales-related KPI columns were detected in this dataset.")

        st.subheader("🧹 Data Cleaning Options")

        col1, col2 = st.columns(2)

        with col1:
            trim_whitespace = st.checkbox("Trim whitespace", value=True)
            remove_special_chars = st.checkbox("Remove special characters", value=True)
            standardize_case = st.checkbox("Standardize lowercase text", value=False)

        with col2:
            fill_missing_numeric = st.checkbox("Fill missing numeric values with mean", value=True)
            remove_duplicate_rows = st.checkbox("Remove duplicate rows", value=True)
            drop_empty_rows = st.checkbox("Drop rows with all missing values", value=False)

        if st.button("Apply Cleaning"):
            cleaned_df = df.copy()

            for col in cleaned_df.select_dtypes(include=["object"]).columns:
                s = cleaned_df[col].astype(str)

                if trim_whitespace:
                    s = s.str.strip()

                if standardize_case:
                    s = s.str.lower()

                if remove_special_chars:
                    s = s.str.replace(r"[^A-Za-z0-9\s%._-]", "", regex=True)

                cleaned_df[col] = s

            cleaned_df = convert_numeric_like_columns(cleaned_df)
            cleaned_df = convert_yes_no_values(cleaned_df)

            if fill_missing_numeric:
                numeric_cols = cleaned_df.select_dtypes(include=["number"]).columns
                for col in numeric_cols:
                    cleaned_df[col] = cleaned_df[col].fillna(cleaned_df[col].mean())

            if remove_duplicate_rows:
                cleaned_df = cleaned_df.drop_duplicates()

            if drop_empty_rows:
                cleaned_df = cleaned_df.dropna(how="all")

            df = cleaned_df
            st.success("Cleaning applied successfully!")

        if st.button("Undo to previous version"):
            df = restore_snapshot(df, snapshot)
            st.success("Restored previous version successfully!")

        st.subheader("Column selection")
        selected_columns = st.multiselect(
            "Choose columns to keep",
            df.columns,
            default=list(df.columns),
        )
        if selected_columns:
            df = df[selected_columns]

        st.subheader("📊 Data Visualization")
        show_visuals = st.checkbox("Show Visualization", value=True)

        if show_visuals:
            numeric_cols = df.select_dtypes(include=["number"]).columns.tolist()
            all_cols = df.columns.tolist()

            if not all_cols:
                st.warning("No columns available to visualize.")
            elif not numeric_cols:
                st.info("No numeric columns are available for visualization.")
            else:
                chart_type = st.selectbox("Chart type", ["Bar", "Line", "Scatter", "Histogram"])
                x_col = st.selectbox("X axis", all_cols)
                y_col = st.selectbox("Y axis", numeric_cols)

                chart = build_chart(df, chart_type, x_col, y_col)
                if chart is not None:
                    st.plotly_chart(chart, use_container_width=True)

                st.write("**Summary Statistics**")
                st.dataframe(df[numeric_cols].describe())

        st.subheader("Conversion options")
        export_type = st.radio("Export as", ["CSV", "Excel"])

        if st.button("Prepare Download"):
            output_data, output_name, mime_type = prepare_export(df, export_type)
            st.download_button(
                label=f"Download {output_name}",
                data=output_data,
                file_name=output_name,
                mime=mime_type,
            )

        st.markdown("---")
