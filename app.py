import streamlit as st
import pandas as pd
import time

# --------------------------------------------------
# Page Config
# --------------------------------------------------
st.set_page_config(
    page_title="Missing Values Checker",
    page_icon="✅",
    layout="wide"
)

# --------------------------------------------------
# Custom CSS
# --------------------------------------------------
st.markdown("""
<style>

/* Main Background */
.stApp {
    background: linear-gradient(135deg, #0f172a, #1e293b);
}

/* Main Title */
.main-title {
    text-align: center;
    font-size: 60px;
    font-weight: bold;
    color: white;
    margin-top: 20px;
}

.sub-title {
    text-align: center;
    color: #d1d5db;
    font-size: 18px;
    margin-bottom: 30px;
}

/* Upload Section */
.upload-container {
    border: 2px dashed #6b7280;
    border-radius: 15px;
    padding: 25px;
    background-color: rgba(255,255,255,0.05);
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: #111827;
}

/* Cards */
.card {
    background-color: rgba(255,255,255,0.05);
    border-radius: 15px;
    padding: 20px;
    color: white;
}

.small-card {
    background-color: rgba(255,255,255,0.08);
    border-radius: 15px;
    padding: 15px;
    text-align: center;
    color: white;
}

</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# Sidebar Instructions
# --------------------------------------------------
with st.sidebar:

    st.markdown("## 📘 User Instructions")

    st.markdown("""
### 1. Upload File
- Upload Excel (.xlsx) file only
- Maximum recommended size: 200 MB
- Ensure data contains **Material Code** column

### 2. Validation Process
- Detects blank values only
- Ignores NA/N/A text values
- Removes empty columns automatically

### 3. Download Results
- Missing values reported by column
- Displays affected Material Codes
- Download processed Excel report

### 4. Benefits
- Faster data quality checks
- Easy identification of missing data
- Ready-to-share output report
""")

# --------------------------------------------------
# Header
# --------------------------------------------------
st.markdown(
    """
    <div class='main-title'>
        ✅ Missing Values Checker
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class='sub-title'>
        Upload an Excel file and identify missing values by Material Code
    </div>
    """,
    unsafe_allow_html=True
)

# --------------------------------------------------
# Upload Area
# --------------------------------------------------
st.markdown("<div class='upload-container'>", unsafe_allow_html=True)

uploaded_file = st.file_uploader(
    "📂 Upload Excel File",
    type=["xlsx"]
)

st.markdown("</div>", unsafe_allow_html=True)

# --------------------------------------------------
# Processing Logic
# --------------------------------------------------
if uploaded_file:

    start_time = time.time()

    with st.spinner("Processing file..."):

        df = pd.read_excel(
            uploaded_file,
            engine="openpyxl",
            keep_default_na=False
        )

        original_cols = len(df.columns)

        # Remove empty columns
        df = df.dropna(axis=1, how="all")

        # Remove unwanted auto-generated columns
        df = df.loc[:, ~df.columns.astype(str).str.startswith("Column")]

        cleaned_cols = len(df.columns)

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            label="Original Columns",
            value=original_cols
        )

    with col2:
        st.metric(
            label="Clean Columns",
            value=cleaned_cols
        )

    if "Material Code" not in df.columns:

        st.error("❌ 'Material Code' column not found.")

    else:

        result = []

        progress = st.progress(0)

        cols_to_check = [
            c for c in df.columns
            if c != "Material Code"
        ]

        total_cols = len(cols_to_check)

        for i, col in enumerate(cols_to_check):

            missing = df[
                df[col]
                .astype(str)
                .str.strip()
                == ""
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

            progress.progress((i + 1) / total_cols)

        output_df = pd.DataFrame(result)

        st.success("✅ Processing Complete")

        st.subheader("Results")

        st.dataframe(
            output_df,
            use_container_width=True
        )

        # Save Output
        output_file = "missing_values_output.xlsx"

        output_df.to_excel(
            output_file,
            index=False
        )

        # Download Button
        with open(output_file, "rb") as file:

            st.download_button(
                label="📥 Download Output File",
                data=file,
                file_name="missing_values_output.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

        st.info(
            f"⏱ Processing Time: {round(time.time() - start_time, 2)} seconds"
        )

        # Summary
        st.subheader("Summary")

        total_missing = output_df[
            output_df["Unique Count"] > 0
        ].shape[0]

        col1, col2 = st.columns(2)

        with col1:
            st.metric(
                "Columns With Missing Data",
                total_missing
            )

        with col2:
            st.metric(
                "Total Checked Columns",
                len(output_df)
            )
