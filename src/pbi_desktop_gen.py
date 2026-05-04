import io
import zipfile
import json
import uuid

def generate_pbip_zip(sql_query: str, databricks_host: str, db_url_path: str, project_name: str = "Databricks_Analytics") -> bytes:
    """
    Generates an in-memory zip file containing a valid PBIP project structure.
    Returns the bytes of the zip file.
    """
    # Clean up inputs for JSON string escaping
    safe_sql = sql_query.replace('"', '""').replace('\n', ' ')
    
    # Construct the M Query for Databricks
    # Note: Power BI uses the Databricks.Catalogs or Databricks.Query connector.
    m_query = f"""let
    Source = Databricks.Query("{databricks_host}", "{db_url_path}", "{safe_sql}")
in
    Source"""

    # 1. Root PBIP File
    pbip_content = {
        "version": "1.0",
        "artifacts": [
            {
                "report": {
                    "path": f"{project_name}.Report"
                }
            }
        ],
        "settings": {
            "enableAutoRecovery": True
        }
    }

    # 2. Semantic Model (formerly Dataset) model.bim
    # Using a high compatibility level (1567+) ensures support for modern features
    model_bim = {
        "name": "SemanticModel",
        "compatibilityLevel": 1604,
        "model": {
            "culture": "en-US",
            "dataAccessOptions": {
                "legacyRedirects": True,
                "returnErrorValuesAsNull": True
            },
            "defaultPowerBIDataSourceVersion": "powerBI_V3",
            "tables": [
                {
                    "name": "DatabricksData",
                    "partitions": [
                        {
                            "name": "DatabricksData",
                            "mode": "import", # Change to "directQuery" if needed
                            "source": {
                                "type": "m",
                                "expression": m_query.split('\n')
                            }
                        }
                    ]
                }
            ]
        }
    }

    # 3. Report Definition (definition.pbir)
    definition_pbir = {
        "version": "4.0",
        "datasetReference": {
            "byPath": {
                "path": f"../{project_name}.SemanticModel"
            },
            "byConnection": None
        }
    }

    # Create the in-memory zip file
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
        
        # Root .pbip file
        zip_file.writestr(f"{project_name}.pbip", json.dumps(pbip_content, indent=2))
        
        # --- Semantic Model Directory ---
        sm_dir = f"{project_name}.SemanticModel"
        zip_file.writestr(f"{sm_dir}/model.bim", json.dumps(model_bim, indent=2))
        zip_file.writestr(f"{sm_dir}/item.metadata.json", json.dumps({"type": "dataset"}, indent=2))
        zip_file.writestr(f"{sm_dir}/item.config.json", json.dumps({"logicalId": str(uuid.uuid4())}, indent=2))
        
        # --- Report Directory ---
        rep_dir = f"{project_name}.Report"
        zip_file.writestr(f"{rep_dir}/definition.pbir", json.dumps(definition_pbir, indent=2))
        zip_file.writestr(f"{rep_dir}/item.metadata.json", json.dumps({"type": "report"}, indent=2))
        zip_file.writestr(f"{rep_dir}/item.config.json", json.dumps({"logicalId": str(uuid.uuid4())}, indent=2))

    return zip_buffer.getvalue()