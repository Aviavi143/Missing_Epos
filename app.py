import streamlit as st
import pandas as pd
import time

st.title("Excel Missing Data Checker ✅")

uploaded_file = st.file_uploader("Upload Excel File", type=["xlsx"])

if uploaded_file:
    start = time.time()

    st.write("Loading file... ⏳")

    # Prevent NA/N/A from being treated as null
    df = pd.read_excel(
        uploaded_file,
        engine="openpyxl",
        keep_default_na=False
    )

    st.write(f"Original columns count: {len(df.columns)}")

    # Clean columns
    df = df.dropna(axis=1, how='all')
    df = df.loc[:, ~df.columns.str.startswith("Column")]

    st.write(f"Clean columns count: {len(df.columns)}")

    if "Material Code" not in df.columns:
        st.error("❌ 'Material Code' column not found")
    else:
        result = []

        for col in df.columns:
            if col == "Material Code":
                continue

            # Only treat truly blank cells as missing
            missing = df[
                df[col].astype(str).str.strip() == ""
            ]

            materials = (
                missing["Material Code"]
                .astype(str)
                .unique()
            )

            result.append({
                "Column Name": col,
                "Missing Material Codes": ", ".join(materials),
                "Unique Count": len(materials)
            })

        output_df = pd.DataFrame(result)

        st.success("✅ Processing complete!")
        st.dataframe(output_df)

        output_file = "output.xlsx"
        output_df.to_excel(output_file, index=False)

        with open(output_file, "rb") as f:
            st.download_button(
                "📥 Download Output",
                f,
                file_name="output.xlsx"
            )

    st.write("⏱ Time taken:", round(time.time() - start, 2), "seconds")
