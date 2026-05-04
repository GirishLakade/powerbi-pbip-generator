content = """# Power BI Desktop PBIP Generator

## Overview
This repository contains our Streamlit application designed to dynamically generate Power BI Project (`.pbip`) files. By capturing Databricks connection details and SQL queries through a web interface, this tool builds the necessary Power BI schema and bundles it into a `.zip` archive for direct download. 

This approach allows our team to streamline Power BI dataset creation and seamlessly integrate our Databricks analytics workflows.

## Features
* **Dynamic M-Query Injection:** Automatically constructs the Power Query logic required to query Databricks directly.
* **Streamlit Interface:** A clean, user-friendly frontend for our internal data teams to input connection parameters.
* **In-Memory Generation:** Creates the `.pbip` folder structure and bundles it into a ZIP archive entirely in-memory—no local file system clutter.
* **Native Download:** Utilizes Streamlit's native download handler to safely prompt the browser for a save location.

## Prerequisites
* Python 3.8+
* Streamlit

## Installation & Setup
1. Clone this repository to the local machine or deployment environment.
2. Install the required dependencies:
   ```bash
   pip install streamlit
   
