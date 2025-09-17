from fastapi import FastAPI, Depends

app = FastAPI()

def get_settings():
    # Une source unique de vérité (config)
    return {"app_name": "ShopAPI", "version": "1.0"}

@app.get("/info")
def info(settings: dict = Depends(get_settings)):
    return settings
