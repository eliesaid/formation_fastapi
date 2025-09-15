from fastapi import FastAPI, HTTPException

app = FastAPI(title="API Items")
# Simuler une base de données en mémoire
fake_items_db = {
    1: {"name": "Chaussure"},
    2: {"name": "Sac"},
}
@app.get("/items/{id}")
def get_item(id: int):
    item = fake_items_db.get(id)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"id": id, "item": item}
