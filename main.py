from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

import requests

# Define FastAPI app
app = FastAPI()

# Define Superbase API credentials
SUPERBASE_PROJECT_ID = "mrklexjyzpgwyqptkmee"
SUPERBASE_URL = f"https://{SUPERBASE_PROJECT_ID}.supabase.co"
SUPERBASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im1ya2xleGp5enBnd3lxcHRrbWVlIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTcxMTMwOTg3MSwiZXhwIjoyMDI2ODg1ODcxfQ.mGSmjPf5T4SeZddc1K24GzRQXGCmZt0EwB5Fwvs93go"
TABLE_NAME = "items"
class Item(BaseModel):
    name: str
    description: str

# Function to make HTTP requests to Superbase
def make_request(method, endpoint, data=None):
    url = f"{SUPERBASE_URL}/{endpoint}"
    headers = {"apikey": SUPERBASE_KEY}
    try:
        if method == "GET":
            response = requests.get(url, headers=headers)
        elif method == "POST":
            response = requests.post(url, json=data, headers=headers)
        elif method == "PUT":
            response = requests.put(url, json=data, headers=headers)
        elif method == "DELETE":
            response = requests.delete(url, headers=headers)
        response.raise_for_status()  # Raise an exception for HTTP errors
        return response.json() if response.text else {}  # Return JSON response if available
    except requests.exceptions.HTTPError as e:
        raise HTTPException(status_code=e.response.status_code, detail=str(e))
    except requests.exceptions.JSONDecodeError as e:
        raise HTTPException(status_code=500, detail="Failed to decode JSON response from server")
# Create item
@app.post("/items/")
async def create_item(item: Item):
    response = make_request("POST", f"table/{TABLE_NAME}", data=item.dict())
    if response:
        return response
    else:
        raise HTTPException(status_code=500, detail="Failed to create item")

# Read item
@app.get("/items/{item_id}")
async def read_item(item_id: int):
    response = make_request("GET", f"table/{TABLE_NAME}?id=eq.{item_id}")
    if response:
        return response
    else:
        raise HTTPException(status_code=404, detail="Item not found")

# Update item
@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item):
    response = make_request("PUT", f"table/{TABLE_NAME}?id=eq.{item_id}", data=item.dict())
    if response:
        return response
    else:
        raise HTTPException(status_code=404, detail="Item not found")

# Delete item
@app.delete("/items/{item_id}")
async def delete_item(item_id: int):
    response = make_request("DELETE", f"table/{TABLE_NAME}?id=eq.{item_id}")
    if response:
        return {"message": "Item deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="Item not found")