from fastapi import FastAPI, Request, UploadFile, File
from PIL import Image
from modules import tagger
from service import tagger_service
import io

tagger.instance.reload()
app = FastAPI()


def make_output(data=None, success=True, error=None):
    return {
        "data": data,
        "error": error,
        "success": success
    }


@app.post("/tagimage")
async def put_object(request: Request, file: UploadFile = File(...), model:str = None):
    request_object_content = await file.read()
    img = Image.open(io.BytesIO(request_object_content))
    if model is None or model == "":
        model = tagger.instance.model_name
    result = tagger_service.make_tagger(img,model)
    return make_output(result)

@app.post("/switch")
async def switch(request: Request):
    data = await request.json()
    tagger.instance.reload(data["model"])
    return make_output({
        "result": True
    })
@app.get("/info")
async def info():
    return make_output({
        "name": "Image tagger API",
    })

@app.get("/state")
async def state():
    return make_output({
        "modelName": tagger.instance.model_name,
        "modelList": tagger.support_model_id
    })