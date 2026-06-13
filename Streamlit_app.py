import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Defective Analysis Dashboard",
    layout="wide"
)

st.title("Defective Analysis Dashboard")

uploaded_file = st.file_uploader(
    "Upload Excel File",
    type=["xlsx"]
)

if uploaded_file is None:
    st.info("Please upload 2026-1.xlsx")
    st.stop()

df = pd.read_excel(uploaded_file)

report = st.sidebar.selectbox(
    "Select Report",
    [
        "1. Product Model Defective Count",
        "2. Warranty Wise Defective Report",
        "3. Defective Type vs Warranty",
        "4. Product vs Defective Type",
        "5. Defective Type vs Type Of Work vs Warranty",
        "6. Region vs Warranty",
        "7. IW Product vs Defective Part",
        "8. Product vs Defective Part vs Warranty",
        "9. Consumables Region vs Warranty",
        "10. Consumables Product vs Part vs Warranty",
        "11. Consumables Product vs Part vs Type Of Work",
        "12. Consumables Type Of Work vs Warranty",
        "13. Consumables IW Part vs Type Of Work"
    ]
)

def report1(df):

    df = df[df['PRODUCT_MODEL'].notna()]
    df = df[df['PRODUCT_MODEL'].astype(str).str.strip() != '']

    summary = (
        df.groupby('PRODUCT_MODEL')
        .size()
        .reset_index(name='Defective Count')
        .sort_values(
            by='Defective Count',
            ascending=False
        )
    )

    grand_total = summary[
        'Defective Count'
    ].sum()

    summary.loc[
        len(summary)
    ] = [
        'Grand Total',
        grand_total
    ]

    return summary
  if report == "1. Product Model Defective Count":

    result = report1(df)

    st.dataframe(
        result,
        use_container_width=True
    )

    st.download_button(
        "Download Report",
        result.to_csv(index=False),
        "Product_Model_Defective_Count.csv"
    )

def report2(df):

    df = df[df['PRODUCT_MODEL'].notna()]
    df = df[
        df['PRODUCT_MODEL']
        .astype(str)
        .str.strip() != ''
    ]

    pivot = pd.pivot_table(
        df,
        index='PRODUCT_MODEL',
        columns='UNIT_STATUS',
        aggfunc='size',
        fill_value=0
    )

    required_cols = [
        'OW',
        'CAMC',
        'IW',
        'EW',
        'LAMC',
        'REPEAT',
        'STOCK'
    ]

    for col in required_cols:
        if col not in pivot.columns:
            pivot[col] = 0

    pivot = pivot[required_cols]

    pivot["Grand Total"] = pivot.sum(axis=1)

    pivot = pivot.sort_values(
        "Grand Total",
        ascending=False
    )

    grand_total = pivot.sum()
    grand_total.name = "Grand Total"

    pivot = pd.concat([
        pivot,
        grand_total.to_frame().T
    ])

    return pivot

elif report == "2. Warranty Wise Defective Report":

    result = report2(df)

    st.dataframe(
        result,
        use_container_width=True
    )

    st.download_button(
        "Download Report",
        result.to_csv(),
        "Warranty_Wise_Defective_Report.csv"
    )
