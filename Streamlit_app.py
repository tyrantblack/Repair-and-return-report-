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
def report3(df):

    def_type_map = {
        15: "UNIT",
        12: "PCB",
        6: "SPARE",
        14: "CONSUMABLES",
        13: "SUB UNIT"
    }

    df["DEFECTIVE_TYPE"] = df["DEF_TYPE"].map(def_type_map)

    df = df[df["DEFECTIVE_TYPE"].notna()]

    pivot = pd.pivot_table(
        df,
        index="DEFECTIVE_TYPE",
        columns="UNIT_STATUS",
        aggfunc="size",
        fill_value=0
    )

    required_cols = [
        "OW","CAMC","IW","EW",
        "LAMC","REPEAT","STOCK"
    ]

    for col in required_cols:
        if col not in pivot.columns:
            pivot[col] = 0

    pivot = pivot[required_cols]

    pivot["Grand Total"] = pivot.sum(axis=1)

    overall_total = pivot["Grand Total"].sum()

    pivot["Contribution %"] = (
        pivot["Grand Total"] /
        overall_total * 100
    ).round(2)

    pivot = pivot.sort_values(
        "Grand Total",
        ascending=False
    )

    grand_total = pivot[
        required_cols + ["Grand Total"]
    ].sum()

    grand_total["Contribution %"] = 100

    grand_total.name = "Grand Total"

    pivot = pd.concat([
        pivot,
        grand_total.to_frame().T
    ])

    return pivot

elif report == "3. Defective Type vs Warranty":

    result = report3(df)

    st.dataframe(
        result,
        use_container_width=True
    )

def report4(df):

    def_type_map = {
        15: "UNIT",
        12: "PCB",
        6: "SPARE",
        14: "CONSUMABLES",
        13: "SUB UNIT"
    }

    df["DEFECTIVE_TYPE"] = (
        df["DEF_TYPE"]
        .map(def_type_map)
    )

    df = df[
        df["DEFECTIVE_TYPE"]
        .notna()
    ]

    pivot = pd.pivot_table(
        df,
        index="PRODUCT_MODEL",
        columns="DEFECTIVE_TYPE",
        aggfunc="size",
        fill_value=0
    )

    required_cols = [
        "UNIT",
        "PCB",
        "SPARE",
        "CONSUMABLES",
        "SUB UNIT"
    ]

    for col in required_cols:
        if col not in pivot.columns:
            pivot[col] = 0

    pivot = pivot[required_cols]

    pivot["Grand Total"] = pivot.sum(axis=1)

    total = pivot["Grand Total"].sum()

    pivot["Contribution %"] = (
        pivot["Grand Total"] /
        total * 100
    ).round(2)

    pivot = pivot.sort_values(
        "Grand Total",
        ascending=False
    )

    grand_total = pivot[
        required_cols + ["Grand Total"]
    ].sum()

    grand_total["Contribution %"] = 100

    grand_total.name = "Grand Total"

    pivot = pd.concat([
        pivot,
        grand_total.to_frame().T
    ])

    return pivot

elif report == "4. Product vs Defective Type":

    result = report4(df)

    st.dataframe(
        result,
        use_container_width=True
    )

def report5(df):

    def_type_map = {
        15:"UNIT",
        12:"PCB",
        6:"SPARE",
        14:"CONSUMABLES",
        13:"SUB UNIT"
    }

    df["DEFECTIVE_TYPE"] = (
        df["DEF_TYPE"]
        .map(def_type_map)
    )

    df = df[
        df["DEFECTIVE_TYPE"]
        .notna()
    ]

    warranty_cols = [
        "OW","CAMC","IW",
        "EW","LAMC",
        "REPEAT","STOCK"
    ]

    rows = []

    overall_total = len(df)

    for defect in sorted(
        df["DEFECTIVE_TYPE"].unique()
    ):

        defect_df = df[
            df["DEFECTIVE_TYPE"] == defect
        ]

        pivot = pd.pivot_table(
            defect_df,
            index="TYPE_OF_WORK",
            columns="UNIT_STATUS",
            aggfunc="size",
            fill_value=0
        )

        for col in warranty_cols:
            if col not in pivot.columns:
                pivot[col] = 0

        pivot = pivot[warranty_cols]

        pivot["Grand Total"] = (
            pivot.sum(axis=1)
        )

        for work,row in pivot.iterrows():

            rows.append({
                "DEF_TYPE": defect,
                "TYPE_OF_WORK": work,
                **{
                    c:int(row[c])
                    for c in warranty_cols
                },
                "Grand Total":
                int(row["Grand Total"]),
                "Contribution %":
                round(
                    row["Grand Total"] /
                    overall_total * 100,
                    2
                )
            })

    return pd.DataFrame(rows)

elif report == "5. Defective Type vs Type Of Work vs Warranty":

    result = report5(df)

    st.dataframe(
        result,
        use_container_width=True
    )

def report6(df):

    pivot = pd.pivot_table(
        df,
        index="REGION",
        columns="UNIT_STATUS",
        aggfunc="size",
        fill_value=0
    )

    required_cols = [
        "OW","CAMC","IW",
        "EW","LAMC",
        "REPEAT","STOCK"
    ]

    for col in required_cols:
        if col not in pivot.columns:
            pivot[col] = 0

    pivot = pivot[required_cols]

    pivot["Grand Total"] = (
        pivot.sum(axis=1)
    )

    total = pivot["Grand Total"].sum()

    pivot["Contribution %"] = (
        pivot["Grand Total"] /
        total * 100
    ).round(2)

    pivot = pivot.sort_values(
        "Grand Total",
        ascending=False
    )

    return pivot

elif report == "6. Region vs Warranty":

    result = report6(df)

    st.dataframe(
        result,
        use_container_width=True
    )

def report7(df):

    df = df[
        df["UNIT_STATUS"]
        .astype(str)
        .str.upper()
        .eq("IW")
    ]

    df = df[
        df["PRODUCT_MODEL"].notna() &
        df["DEF_MOD_BRD_NAME"].notna()
    ]

    overall_total = len(df)

    rows = []

    for model in sorted(df["PRODUCT_MODEL"].unique()):

        model_df = df[
            df["PRODUCT_MODEL"] == model
        ]

        counts = (
            model_df["DEF_MOD_BRD_NAME"]
            .value_counts()
            .reset_index()
        )

        counts.columns = [
            "DEF_MOD_BRD_NAME",
            "Count"
        ]

        model_total = counts["Count"].sum()

        contribution = round(
            model_total /
            overall_total * 100,
            2
        )

        first = True

        for _,r in counts.iterrows():

            rows.append({
                "PRODUCT_MODEL":
                model if first else "",
                "DEF_MOD_BRD_NAME":
                r["DEF_MOD_BRD_NAME"],
                "Count":
                int(r["Count"]),
                "Contribution %":""
            })

            first = False

        rows.append({
            "PRODUCT_MODEL":"",
            "DEF_MOD_BRD_NAME":
            "Grand Total",
            "Count":
            int(model_total),
            "Contribution %":
            contribution
        })

    return pd.DataFrame(rows)

elif report == "7. IW Product vs Defective Part":

    result = report7(df)
    st.dataframe(result, use_container_width=True)

def report8(df):

    warranty_cols = [
        "OW","CAMC","IW",
        "EW","LAMC","REPEAT"
    ]

    model_order = (
        df.groupby("PRODUCT_MODEL")
        .size()
        .sort_values(
            ascending=False
        )
        .index
    )

    rows = []

    for model in model_order:

        model_df = df[
            df["PRODUCT_MODEL"] == model
        ]

        pivot = pd.pivot_table(
            model_df,
            index="DEF_MOD_BRD_NAME",
            columns="UNIT_STATUS",
            aggfunc="size",
            fill_value=0
        )

        for col in warranty_cols:
            if col not in pivot.columns:
                pivot[col] = 0

        pivot = pivot[warranty_cols]

        pivot["Grand Total"] = (
            pivot.sum(axis=1)
        )

        pivot = pivot.sort_values(
            "Grand Total",
            ascending=False
        )

        first = True

        for part,row in pivot.iterrows():

            rows.append({
                "PRODUCT_MODEL":
                model if first else "",
                "DEF_MOD_BRD_NAME":
                part,
                **{
                    c:int(row[c])
                    for c in warranty_cols
                },
                "Grand Total":
                int(row["Grand Total"])
            })

            first = False

    return pd.DataFrame(rows)

elif report == "8. Product vs Defective Part vs Warranty":

    result = report8(df)
    st.dataframe(result, use_container_width=True)

def report9(df):

    df = df[
        df["DEF_TYPE"] == 14
    ]

    return report6(df)

elif report == "9. Consumables Region vs Warranty":

    result = report9(df)
    st.dataframe(result, use_container_width=True)

def report10(df):

    df = df[
        df["DEF_TYPE"] == 14
    ]

    warranty_cols = [
        "OW","CAMC","IW",
        "EW","LAMC","REPEAT"
    ]

    rows = []

    model_order = (
        df.groupby("PRODUCT_MODEL")
        .size()
        .sort_values(
            ascending=False
        )
        .index
    )

    for model in model_order:

        model_df = df[
            df["PRODUCT_MODEL"] == model
        ]

        pivot = pd.pivot_table(
            model_df,
            index=[
                "DEF_PART_SN",
                "DEF_MOD_BRD_NAME"
            ],
            columns="UNIT_STATUS",
            aggfunc="size",
            fill_value=0
        )

        for col in warranty_cols:
            if col not in pivot.columns:
                pivot[col] = 0

        pivot = pivot[warranty_cols]

        pivot["Grand Total"] = (
            pivot.sum(axis=1)
        )

        pivot = pivot.sort_values(
            "Grand Total",
            ascending=False
        )

        first=True

        for (sn,part),row in pivot.iterrows():

            rows.append({
                "PRODUCT_MODEL":
                model if first else "",
                "DEF_PART_SN":sn,
                "DEF_MOD_BRD_NAME":part,
                **{
                    c:int(row[c])
                    for c in warranty_cols
                },
                "Grand Total":
                int(row["Grand Total"])
            })

            first=False

    return pd.DataFrame(rows)

elif report == "10. Consumables Product vs Part vs Warranty":

    result = report10(df)
    st.dataframe(result, use_container_width=True)

def report11(df):

    df = df[
        df["DEF_TYPE"] == 14
    ]

    work_cols = sorted(
        df["TYPE_OF_WORK"]
        .dropna()
        .unique()
    )

    rows=[]

    for model in (
        df.groupby("PRODUCT_MODEL")
        .size()
        .sort_values(
            ascending=False
        )
        .index
    ):

        model_df = df[
            df["PRODUCT_MODEL"] == model
        ]

        pivot = pd.pivot_table(
            model_df,
            index=[
                "DEF_PART_SN",
                "DEF_MOD_BRD_NAME"
            ],
            columns="TYPE_OF_WORK",
            aggfunc="size",
            fill_value=0
        )

        for col in work_cols:
            if col not in pivot.columns:
                pivot[col]=0

        pivot= pivot[work_cols]

        pivot["Grand Total"]=(
            pivot.sum(axis=1)
        )

        first=True

        for (sn,part),row in pivot.iterrows():

            rows.append({
                "PRODUCT_MODEL":
                model if first else "",
                "DEF_PART_SN":sn,
                "DEF_MOD_BRD_NAME":part,
                **{
                    c:int(row[c])
                    for c in work_cols
                },
                "Grand Total":
                int(row["Grand Total"])
            })

            first=False

    return pd.DataFrame(rows)

elif report == "11. Consumables Product vs Part vs Type Of Work":

    result = report11(df)
    st.dataframe(result, use_container_width=True)

def report12(df):

    df = df[
        df["DEF_TYPE"] == 14
    ]

    warranty_cols = [
        "OW","CAMC","IW",
        "EW","LAMC","REPEAT"
    ]

    pivot = pd.pivot_table(
        df,
        index="TYPE_OF_WORK",
        columns="UNIT_STATUS",
        aggfunc="size",
        fill_value=0
    )

    for col in warranty_cols:
        if col not in pivot.columns:
            pivot[col]=0

    pivot = pivot[warranty_cols]

    pivot["Grand Total"] = (
        pivot.sum(axis=1)
    )

    return pivot.sort_values(
        "Grand Total",
        ascending=False
    )

elif report == "12. Consumables Type Of Work vs Warranty":

    result = report12(df)
    st.dataframe(result, use_container_width=True)

def report13(df):

    df = df[
        (df["DEF_TYPE"] == 14) &
        (
            df["UNIT_STATUS"]
            .astype(str)
            .str.upper()
            .eq("IW")
        )
    ]

    work_cols = sorted(
        df["TYPE_OF_WORK"]
        .dropna()
        .unique()
    )

    pivot = pd.pivot_table(
        df,
        index=[
            "DEF_PART_SN",
            "DEF_MOD_BRD_NAME"
        ],
        columns="TYPE_OF_WORK",
        aggfunc="size",
        fill_value=0
    )

    for col in work_cols:
        if col not in pivot.columns:
            pivot[col]=0

    pivot = pivot[work_cols]

    pivot["Grand Total"] = (
        pivot.sum(axis=1)
    )

    return (
        pivot
        .sort_values(
            "Grand Total",
            ascending=False
        )
        .reset_index()
    )

elif report == "13. Consumables IW Part vs Type Of Work":

    result = report13(df)
    st.dataframe(result, use_container_width=True)
