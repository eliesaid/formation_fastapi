from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI()

@app.get("/accepted")
def accepted():
    return JSONResponse(content={"ok": True}, status_code=202)
