import streamlit as st
from pbi_desktop_gen import generate_pbip_zip

st.set_page_config(page_title="PBIP Generator", layout="centered")

st.title("Power BI Desktop PBIP Generator")
st.markdown("Generate a local `.pbip` project connected to Databricks.")

with st.form("pbip_form"):
    databricks_host = st.text_input(
        "Databricks Host", 
        placeholder="e.g., adb-123456789.azuredatabricks.net"
    )
    db_url_path = st.text_input(
        "HTTP Path", 
        placeholder="e.g., sql/protocolv1/o/123456789/xxxx-xxxxxx-xxxxxx"
    )
    sql_query = st.text_area(
        "SQL Query", 
        placeholder="SELECT * FROM main.wealth_management.client_metrics",
        height=150
    )
    
    generate_clicked = st.form_submit_button("Prepare PBIP File")

# Handle the generation and download state outside the form
if generate_clicked:
    if not all([databricks_host, db_url_path, sql_query]):
        st.error("Please fill in all fields before generating.")
    else:
        with st.spinner("Generating PBIP project structure..."):
            try:
                # Generate the zip file bytes in-memory
                zip_bytes = generate_pbip_zip(sql_query, databricks_host, db_url_path)
                
                st.success("Project generated successfully! Click below to save it to your machine.")
                
                # Streamlit's native way to prompt a user file save dialog
                st.download_button(
                    label="💾 Download PBIP Project (ZIP)",
                    data=zip_bytes,
                    file_name="Databricks_Analytics_PBIP.zip",
                    mime="application/zip"
                )
            except Exception as e:
                st.error(f"An error occurred during generation: {e}")