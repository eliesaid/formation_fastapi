from fastapi import FastAPI, Depends

app = FastAPI()

class SettingsProvider:
    def __init__(self, name: str, version: str):
        self.name = name
        self.version = version

    def __call__(self):
        # sera appelée par FastAPI pour produire la valeur injectée
        return {"app_name": self.name, "version": self.version}

get_settings = SettingsProvider(name="ShopAPI", version="1.0")

@app.get("/health")
def health(settings: dict = Depends(get_settings)):
    return {"status": "ok", "version": settings["version"]}
