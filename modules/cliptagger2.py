import os

import PIL
from clip_interrogator import Config, Interrogator, LabelTable, load_list

DATA_PATH = './assets/clip2'


class InterrogateModels:
    model = None
    config = None

    def __init__(self):
        self.config = Config()
        self.config.apply_low_vram_defaults()

    def load(self):
        self.model = Interrogator(self.config)
        sites = ['Artstation', 'behance', 'cg society', 'cgsociety', 'deviantart', 'dribble',
                 'flickr', 'instagram', 'pexels', 'pinterest', 'pixabay', 'pixiv', 'polycount',
                 'reddit', 'shutterstock', 'tumblr', 'unsplash', 'zbrush central']
        trending_list = [site for site in sites]
        trending_list.extend(["trending on " + site for site in sites])
        trending_list.extend(["featured on " + site for site in sites])
        trending_list.extend([site + " contest winner" for site in sites])
        artists = LabelTable(load_list(DATA_PATH, 'artists.txt'), "artists", self.model)
        flavors = LabelTable(load_list(DATA_PATH, 'flavors.txt'), "flavors", self.model)
        mediums = LabelTable(load_list(DATA_PATH, 'mediums.txt'), "mediums", self.model)
        movements = LabelTable(load_list(DATA_PATH, 'movements.txt'), "movements", self.model)
        trendings = LabelTable(trending_list, "trendings", self.model)
        self.tables = [artists, flavors, mediums, movements, trendings]

    def unload(self):
        pass

    def generate_caption(self, pil_image):
        return self.interrogate(pil_image, stringify=True)

    def interrogate(self, pil_image, stringify=False):

        results = []
        for table in self.tables:
            feat = self.model.image_to_features(pil_image)
            match_results = table.rank(feat, top_count=5)
            ranks = self.model.similarities(feat, match_results)
            for i in range(len(match_results)):
                results.append({
                    "tag": match_results[i],
                    "rank": ranks[i],
                })
        if stringify:
            return ",".join([result["tag"] for result in results])
        else:
            return results

    def tag_multi(
            self,
            image: PIL.Image.Image,
            include_ranks: bool = False,
    ):
        result = self.interrogate(image)
        if include_ranks:
            return result
        return result