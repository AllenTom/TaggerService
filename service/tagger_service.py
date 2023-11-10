from modules import tagger
from PIL import Image


def make_tagger(image: Image):
    result = tagger.instance.make_tagger(image)
    return result
