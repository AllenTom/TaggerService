from modules import tagger
from PIL import Image


def make_tagger(image: Image, model: str | None, threshold: float = 0.5):
    result = tagger.instance.make_tagger(image, model, threshold=threshold)
    return result
