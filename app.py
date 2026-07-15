import streamlit as st
import pandas as pd
import time

# ==================================================
# PAGE CONFIG
# ==================================================

st.set_page_config(
    page_title="Missing Values Checker",
    page_icon="✅",
    layout="wide"
)

# ==================================================
# CUSTOM CSS
# ==================================================

st.markdown("""
<style>

/* Main Background */
.stApp {
    background: linear-gradient(
        135deg,
        #020617 0%,
        #0f172a 50%,
        #1e293b 100%
    );
}

/* Hide Streamlit Menu */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

/* Main Title */
.main-title{
    font-size:70px;
    font-weight:900;
    text-align:center;
    background: linear-gradient(
        90deg,
        #38bdf8,
        #67e8f9,
        #ffffff
    );

    -webkit-background-clip:text;
    -webkit-text-fill-color:transparent;

    margin-top:20px;
}

/* Subtitle */
.sub-title{
    text-align:center;
    color:#cbd5e1;
    font-size:20px;
    margin-bottom:30px;
}

/* Glass Card */
.glass-card{
    background:rgba(255,255,255,0.05);
    backdrop-filter:blur(15px);
    border:1px solid rgba(255,255,255,0.1);
    border-radius:20px;
    padding:25px;
    margin-bottom:20px;
    box-shadow:0px 8px 32px rgba(0,0,0,0.3);
}

/* Metrics */
.metric-box{
    background:linear-gradient(
        135deg,
        rgba(56,189,248,0.20),
        rgba(255,255,255,0.05)
    );

    border-radius:15px;
    padding:20px;
    text-align:center;
    border:1px solid rgba(255,255,255,0.1);
}

/* Sidebar */
section[data-testid="stSidebar"]{
    background:#050b18;
}

section[data-testid="stSidebar"] *{
    color:white;
}

/* Upload Area */
.stFileUploader{
    background: rgba(255,255,255,0.04);
    border-radius:15px;
    padding:15px;
}

/* Download Button */
.stDownloadButton > button{
    width:100%;
    background:linear-gradient(
        90deg,
        #06b6d4,
        #3b82f6
    );

    color:white !important;
    border:none;
    border-radius:10px;
    font-weight:bold;
    height:50px;
}

/* Dataframe */
[data-testid="stDataFrame"]{
    border-radius:15px;
}

</style>
""", unsafe_allow_html=True)

# ==================================================
# SIDEBAR
# ==================================================

with st.sidebar:

    st.title("✅ Missing Values Checker")

    st.markdown("---")

    st.markdown("""
### 📘 User Instructions

#### Upload Guidelines
- Upload Excel (.xlsx) file only
- Material Code column is mandatory
- Single worksheet recommended

#### Validation Process
- Detects blank cells only
- Keeps values like N/A and NA as text
- Removes empty columns automatically

#### Output
- Shows missing values by column
- Lists affected Material Codes
- Download Excel report

#### Benefits
- Faster data validation
- Better data quality checks
- Instant downloadable output
""")

    st.markdown("---")
    st.success("✅ Ready to Process")

# ==================================================
# HEADER
# ==================================================

st.markdown("""
<div class="main-title">
    Missing Values Checker
</div>

<div class="sub-title">
    Smart Excel Validation Tool for Missing Data Analysis
</div>
""", unsafe_allow_html=True)

# ==================================================
# UPLOAD SECTION
# ==================================================

st.markdown("""
<div class="glass-card">
    <h2 style="text-align:center;color:white;">
        📂 Upload Excel File
    </h2>
</div>
""", unsafe_allow_html=True)

uploaded_file = st.file_uploader(
    "Select an Excel file",
    type=["xlsx"]
)

# ==================================================
# PROCESS FILE
# ==================================================

if uploaded_file:

    start_time = time.time()

    with st.spinner("Reading Excel File..."):

        df = pd.read_excel(
            uploaded_file,
            engine="openpyxl",
            keep_default_na=False
        )

        original_cols = len(df.columns)

        df = df.dropna(axis=1, how="all")

        df = df.loc[
            :,
            ~df.columns.astype(str).str.startswith("Column")
        ]

        cleaned_cols = len(df.columns)

    # ==================================================
    # METRICS
    # ==================================================

    c1, c2, c3 = st.columns(3)

    with c1:
        st.markdown(f"""
        <div class="metric-box">
            <h4 style="color:white;">📋 Original Columns</h4>
            <h1 style="color:white;">{original_cols}</h1>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown(f"""
        <div class="metric-box">
            <h4 style="color:white;">✅ Clean Columns</h4>
            <h1 style="color:white;">{cleaned_cols}</h1>
        </div>
        """, unsafe_allow_html=True)

    with c3:
        st.markdown("""
        <div class="metric-box">
            <h4 style="color:white;">🔍 Status</h4>
            <h1 style="color:#22c55e;">Ready</h1>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ==================================================
    # CHECK COLUMN
    # ==================================================

    if "Material Code" not in df.columns:

        st.error("❌ 'Material Code' column not found in Excel.")

    else:

        progress_bar = st.progress(0)

        result = []

        check_columns = [
            col
            for col in df.columns
            if col != "Material Code"
        ]

        total_columns = len(check_columns)

        for index, col in enumerate(check_columns):

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

            progress_bar.progress(
                (index + 1) / total_columns
            )

        output_df = pd.DataFrame(result)

        st.success("✅ Processing Completed Successfully")

        # ==================================================
        # SUMMARY
        # ==================================================

        total_missing_columns = output_df[
            output_df["Unique Count"] > 0
        ].shape[0]

        s1, s2, s3 = st.columns(3)

        s1.metric(
            "Columns Checked",
            len(output_df)
        )

        s2.metric(
            "Columns with Missing Data",
            total_missing_columns
        )

        s3.metric(
            "Processing Time",
            f"{round(time.time()-start_time,2)} sec"
        )

        st.markdown("---")

        st.subheader("📊 Missing Values Analysis")

        st.dataframe(
            output_df,
            use_container_width=True,
            height=500
        )

        # ==================================================
        # EXPORT
        # ==================================================

        output_file = "missing_values_output.xlsx"

        output_df.to_excel(
            output_file,
            index=False
        )

        with open(output_file, "rb") as file:

            st.download_button(
                label="📥 Download Analysis Report",
                data=file,
                file_name="missing_values_output.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

        st.info(
            f"⏱ Total Processing Time: {round(time.time()-start_time,2)} seconds"
        )

# ==================================================
# FOOTER
# ==================================================

st.markdown("""
<br><br>
<hr>
<p style="
text-align:center;
color:#94a3b8;
font-size:14px;">
Missing Values Checker © 2026 | Data Quality Validation Tool
</p>
""", unsafe_allow_html=True)
