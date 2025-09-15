from fastapi import FastAPI, Body

app = FastAPI(title="API Produits")

@app.post("/products")
def create_product(name: str = Body(..., embed=True)):
    return {"id": 1, "name": name}
