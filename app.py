import streamlit as st
import pandas as pd
import time
import base64

st.set_page_config(
    page_title="Missing Values Checker",
    layout="wide"
)

# ---------- Background Image ----------
def add_bg(image_file):
    with open(image_file, "rb") as f:
        data = f.read()

    encoded = base64.b64encode(data).decode()

    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: linear-gradient(
                rgba(0,0,0,0.75),
                rgba(0,0,0,0.75)
            ),
            url("data:image/png;base64,{encoded}");
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
        }}

        .main-title {{
            text-align:center;
            font-size:60px;
            color:white;
            font-weight:bold;
            margin-top:50px;
        }}

        .upload-box {{
            border:2px dashed #888;
            padding:30px;
            border-radius:15px;
            background:rgba(255,255,255,0.05);
        }}

        .instruction-text {{
            color:white;
            font-size:16px;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# Replace with your image
add_bg("background.jpg")

# ---------- Sidebar ----------
with st.sidebar:
    st.markdown(
        """
        <h2 style='color:white;'>User Instructions</h2>

        ### 1. Upload File
        - Upload Excel (.xlsx)
        - Maximum size: 200 MB
        - Single sheet supported

        ### 2. Processing
        - Detects blank values
        - Uses Material Code for tracking

        ### 3. Output
        - Download processed report
        - Shows missing material codes
        """,
        unsafe_allow_html=True
    )

# ---------- Main Title ----------
st.markdown(
    """
    <div class='main-title'>
        Missing Values Checker
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown("<br>", unsafe_allow_html=True)

# ---------- Upload Area ----------
st.markdown("<div class='upload-box'>", unsafe_allow_html=True)

uploaded_file = st.file_uploader(
    "Upload Excel File",
    type=["xlsx"]
)

st.markdown("</div>", unsafe_allow_html=True)

# ---------- Processing ----------
if uploaded_file:

    start = time.time()

    with st.spinner("Processing..."):

        df = pd.read_excel(
            uploaded_file,
            engine="openpyxl",
            keep_default_na=False
        )

        df = df.dropna(axis=1, how="all")
        df = df.loc[:, ~df.columns.str.startswith("Column")]

        if "Material Code" not in df.columns:
            st.error("Material Code column not found")
        else:

            result = []

            for col in df.columns:

                if col == "Material Code":
                    continue

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

            st.success("Processing Complete")

            st.dataframe(
                output_df,
                use_container_width=True
            )

            output_df.to_excel(
                "missing_values_output.xlsx",
                index=False
            )

            with open(
                "missing_values_output.xlsx",
                "rb"
            ) as f:

                st.download_button(
                    "📥 Download Report",
                    f,
                    file_name="missing_values_output.xlsx"
                )

    st.info(
        f"Time Taken: {round(time.time()-start,2)} seconds"
    )
