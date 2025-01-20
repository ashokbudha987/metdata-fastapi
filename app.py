from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from helpers import combine_metadata, extract_metadata_user_query
app = FastAPI()

class QueryRequest(BaseModel):
    query: str

class MetadataResponse(BaseModel):
    extracted_metadata: str

final_metrics, final_attributes, final_columns, final_functions = combine_metadata()

@app.post("/extract_metadata", response_model=MetadataResponse)
async def extract_metadata(request: QueryRequest):
    try:
        extracted_metadata = extract_metadata_user_query(request.query, final_metrics, final_attributes, final_columns, final_functions)
        return {"extracted_metadata": extracted_metadata}
    except Exception as e:
        raise
        # raise HTTPException(status_code=500, detail=str(e))
