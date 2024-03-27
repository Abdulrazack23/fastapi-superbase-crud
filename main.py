from pydantic import BaseModel
from fastapi import FastAPI, HTTPException
from supabase import create_client

from postgrest.exceptions import APIError
app = FastAPI(title='Fastapi Supabase')

supabase_url = ""
supabase_key = ""
supabase = create_client(supabase_url, supabase_key)

table_name = "items"
class Item(BaseModel):
    id: int
    name: str
    description: str
@app.post("/items/")
def create_item(item: Item):
    try:
        response = supabase.table(table_name).insert([item.dict()]).execute()

        if response.get("status") == 201:  
            return response.get("data")[0] 
        else:
            raise HTTPException(status_code=400, detail="Failed to create item")
    except APIError as api_error:
        error_message = api_error.message
        raise HTTPException(status_code=500, detail=f"Error from Supabase: {error_message}")

@app.get("/items/{item_id}")
def read_item(item_id: int):
    response = supabase.table(table_name).select("*").eq("id", item_id).single()

    if response.status_code == 200:
        return response.data
    else:
        raise HTTPException(status_code=404, detail="Item not found")
    
@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    try:
        response = supabase.table(table_name).update(item.dict()).eq("id", item_id).execute()

        if response.get("status") == 200:
            return response.get("data") 
        else:
            raise HTTPException(status_code=404, detail="Item not found")
    except APIError as api_error:
        error_message = api_error.message
        raise HTTPException(status_code=500, detail=f"Error from Supabase: {error_message}")

@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    try:
        response = supabase.table(table_name).delete().eq("id", item_id).execute()

        if response.get("status") == 200: 
            return {"message": "Item deleted successfully"}
        else:
            raise HTTPException(status_code=404, detail="Item not found")
    except APIError as api_error:
        error_message = api_error.message
        raise HTTPException(status_code=500, detail=f"Error from Supabase: {error_message}")
