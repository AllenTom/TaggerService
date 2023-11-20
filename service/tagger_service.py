from modules import tagger
from PIL import Image


def make_tagger(image: Image,model:str | None):
    result = tagger.instance.make_tagger(image,model)
    return result
