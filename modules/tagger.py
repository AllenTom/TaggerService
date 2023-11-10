import time

from modules import deepbooru
from PIL import Image


class Tagger():
    def __init__(self):
        self.model = deepbooru.DeepDanbooru()

    def reload(self):
        start = time.time()
        print("Reloading tagger")
        self.model.load()
        self.model.start()
        print("Tagger reloaded in", time.time() - start, "seconds")

    def make_tagger(self, image: Image):
        return self.model.tag_multi(image, include_ranks=True)


instance = Tagger()
