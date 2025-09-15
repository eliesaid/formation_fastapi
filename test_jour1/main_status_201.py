from fastapi import FastAPI, Body  

app = FastAPI(title="Mini API")

@app.post("/items", status_code=201)
def add_item(name: str = Body(..., embed=True)):
    return {"id": 1, "name": name}



