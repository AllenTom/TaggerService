import logging
import sys
import time

from modules import deepbooru, wd14, cliptagger2, category
from PIL import Image

support_model_id = ["wd14_MOAT", "wd14_SwinV2", "wd14_ConvNext", "wd14_ConvNextV2", "wd14_ViT", "DeepDanbooru", "clip2",'category']

logger = logging.getLogger(__name__)


class Tagger():
    def __init__(self):
        self.model = wd14.WaifuDiffusion()
        self.model_name = ""

    def reload(self, model_name="wd14_MOAT"):
        if self.model_name == model_name:
            return
        start = time.time()
        logger.info("Reloading tagger to %s", model_name)
        if model_name == "wd14_MOAT":
            wd_model = wd14.WaifuDiffusion()
            wd_model.load("MOAT")
            self.model = wd_model
            self.model_name = "wd14_MOAT"
            self.model.start()
        elif model_name == "wd14_SwinV2":
            wd_model = wd14.WaifuDiffusion()
            wd_model.load("SwinV2")
            self.model = wd_model
            self.model_name = "wd14_SwinV2"
            self.model.start()
        elif model_name == "wd14_ConvNext":
            wd_model = wd14.WaifuDiffusion()
            wd_model.load("ConvNext")
            self.model = wd_model
            self.model_name = "wd14_ConvNext"
            self.model.start()
        elif model_name == "wd14_ConvNextV2":
            wd_model = wd14.WaifuDiffusion()
            wd_model.load("ConvNextV2")
            self.model = wd_model
            self.model_name = "ConvNextV2"
            self.model.start()

        elif model_name == "wd14_ViT":
            wd_model = wd14.WaifuDiffusion()
            wd_model.load("ViT")
            self.model = wd_model
            self.model_name = "wd14_ViT"
            self.model.start()
        elif model_name == "clip2":
            self.model = cliptagger2.InterrogateModels()
            self.model_name = "clip2"
            self.model.load()
        elif model_name == 'category':
            self.model = category.CategoryPredictor()
            self.model_name = "category"
            self.model.load()
            self.model.start()
        else:
            self.model = deepbooru.DeepDanbooru()
            self.model_name = "DeepDanbooru"
            self.model.load()
            self.model.start()
        logger.info("Tagger reloaded in %s seconds", time.time() - start)

    def make_tagger(self, image: Image, model: str | None = None, threshold: float = 0.5):
        if model is not None:
            if model not in support_model_id:
                return {
                    "error": f"Model {model} not supported",
                    "success": False
                }
            self.reload(model)
        return self.model.tag_multi(image, include_ranks=True, threshold=threshold)


instance = Tagger()
