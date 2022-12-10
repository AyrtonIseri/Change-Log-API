from fastapi import FastAPI, status, HTTPException
from pydantic import BaseModel
from typing import Optional

class Table(BaseModel):
    no_of_columns: int
    columns_headers: list[str]
    PK: bool = True

tables = [{'no_of_columns': 4, 
           'columns_headers': ['school', 'birthday'], 
           'PK': True, 
           'id': 0}]

def valid_idx(id: int):
    if id < 0 or id >= len(tables):
        return False
    
    return True

app = FastAPI()

@app.get("/tables")
def get_tables():
    return {"tables": tables}

@app.get("/table/{id}", status_code=status.HTTP_200_OK)
async def get_table(id: int):
    
    if not valid_idx(id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Table not found in database")

    table = tables[id]

    return {"Table Selected": table}


@app.post("/table", status_code=status.HTTP_201_CREATED)
async def create_table(table: Table):
    new_id = len(tables)

    new_table = table.dict()
    new_table['id'] = new_id
    tables.append(new_table)

    return {"Message": f"Table inserted successfully at index {new_id}"}

@app.put("/table/{id}")
async def update_table(id: int, table: Table):
    
    if not valid_idx(id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Table not found in database using id {id}")

    updated_table = table.dict()
    updated_table['id'] = id
    tables[id] = updated_table
    return {"message": f"table {id} updated successfully"}

@app.delete("/table/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_table(id: int):
    
    if not valid_idx(id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Table not found in database using id {id}")

    for i in range(id, len(tables)):
        tables[i]['id'] -= 1

    tables.pop(id)