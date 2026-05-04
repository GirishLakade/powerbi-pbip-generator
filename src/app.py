import streamlit as st
from pbi_desktop_gen import generate_pbip_zip

import tkinter as tk
from tkinter import filedialog

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
                
                # Use tkinter to prompt for save location
                root = tk.Tk()
                root.withdraw()
                root.wm_attributes('-topmost', 1)
                
                file_path = filedialog.asksaveasfilename(
                    defaultextension=".zip",
                    initialfile="Databricks_Analytics_PBIP.zip",
                    title="Save PBIP Project",
                    filetypes=[("ZIP files", "*.zip"), ("All files", "*.*")]
                )
                
                root.destroy()
                
                if file_path:
                    with open(file_path, "wb") as f:
                        f.write(zip_bytes)
                    st.success(f"Project generated and saved successfully to: `{file_path}`")
                else:
                    st.warning("Save operation cancelled.")
                    
            except Exception as e:
                st.error(f"An error occurred during generation: {e}")