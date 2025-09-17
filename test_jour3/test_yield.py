from fastapi import Depends

def open_resource():
    # setup (avant la route)
    resource = {"opened": True}
    try:
        yield resource
    finally:
        # teardown (après la réponse)
        resource["opened"] = False

@app.get("/res")
def read_res(res=Depends(open_resource)):
    return {"opened": res["opened"]}
