import streamlit as st
from qc_backend import run_qc, build_zip

st.title("QC Tool")

uploaded_file = st.file_uploader("Upload Assignments Excel", type=["xlsx"])

assignee = st.selectbox("Assignee", ["Denise", "Adam", "John", "Sandra"])
qc_type = st.selectbox("QC Type", ["New Loan", "Mods / Renewals / Extensions"])

# session state setup
if "zip_buffer" not in st.session_state:
    st.session_state.zip_buffer = None

if "file_count" not in st.session_state:
    st.session_state.file_count = 0


if st.button("🚀 Run QC + Download"):

    if not uploaded_file:
        st.error("Please upload an Excel file first.")
        st.stop()

    # Step 1: run QC
    results = run_qc(uploaded_file, assignee, qc_type)

    # Step 2: build ZIP immediately
    zip_buffer = build_zip(results)

    # Step 3: store in session state
    st.session_state.zip_buffer = zip_buffer
    st.session_state.file_count = len(results)

    st.success(f"Created {len(results)} files")


# Step 4: auto-show download after run
if st.session_state.zip_buffer:

    st.download_button(
        label="⬇️ Download All Files (ZIP)",
        data=st.session_state.zip_buffer,
        file_name="QC_Output.zip",
        mime="application/zip"
    )