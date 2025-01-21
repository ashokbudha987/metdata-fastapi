from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from helpers import combine_metadata, extract_metadata_user_query
from itlm_db_connector.factory import DatabaseFactory
app = FastAPI()

class QueryRequest(BaseModel):
    query: str

class MetadataResponse(BaseModel):
    extracted_metadata: str

class SampleDataRequest(BaseModel):
    database_type: str
    db_config: dict
    table_name: str

class SampleDataResponse(BaseModel):
    table_ddl: str
    sample_rows_query: str



final_metrics, final_attributes, final_columns, final_functions = combine_metadata()

@app.post("/extract_metadata", response_model=MetadataResponse)
async def extract_metadata(request: QueryRequest):
    try:
        extracted_metadata = extract_metadata_user_query(request.query, final_metrics, final_attributes, final_columns, final_functions)
        return {"extracted_metadata": extracted_metadata}
    except Exception as e:
        raise
        # raise HTTPException(status_code=500, detail=str(e))

@app.post("/get_metadata", response_model=SampleDataResponse)
async def get_metadata(request: SampleDataRequest):
    try:
        db_config = request.db_config
        connector = DatabaseFactory.get_connector(
            request.database_type
        )(**db_config)
        table_ddl = connector.get_ddl(table_name=request.table_name)
        sample_rows_query = connector.get_sample_rows_query(table_name=request.table_name)
        return {"table_ddl": table_ddl, "sample_rows_query": sample_rows_query}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


