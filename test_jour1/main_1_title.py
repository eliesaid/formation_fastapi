from fastapi import FastAPI

app = FastAPI(
    title="Mon Application FastAPI",
    description="Une API simple pour dire bonjour",
    version="1.0.0"
)

@app.get("/")
def read_root():
    return {"message": "Hello World"}
