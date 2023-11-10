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
async def put_object(request: Request, file: UploadFile = File(...)):
    request_object_content = await file.read()
    img = Image.open(io.BytesIO(request_object_content))
    result = tagger_service.make_tagger(img)
    return make_output(result)


@app.get("/info")
async def info():
    return make_output({
        "name": "Image tagger API",
        "success": True,
    })
