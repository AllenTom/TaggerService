import torch
from PIL import Image
from torchvision.transforms import Normalize, Compose, Resize, ToTensor
from transformers import ViTImageProcessor, ViTForImageClassification

from modules import share

labels = ['animal', 'cartoon', 'landscape', 'other', 'portrait', 'screenshot']

model_name = "2024-07-05-16-54-53-vit-base-patch16-224-cifar10-1"
processor = ViTImageProcessor.from_pretrained("google/vit-base-patch16-224")

mu, sigma = processor.image_mean, processor.image_std
use_model = ViTForImageClassification.from_pretrained(model_name)


class CategoryPredictor:
    def __init__(self):
        self.model = None


    def load_model(self):
        self.model = use_model.to(share.device)
    def unload_model(self):
        self.model = None

    def load(self):
        self.load_model()

    def start(self):
        pass


    def stop(self):
        self.unload_model()
    def tag_multi(self, pil_image, threshold=0.5,
                  include_ranks=False):
        result = self.predict(pil_image)
        if include_ranks:
            with_rank_list = []
            for tag, prob in result['prob_map'].items():
                if prob >= threshold:
                    with_rank_list.append({
                        "tag": tag,
                        "rank": float(f"{prob:.3f}")
                    })
            return with_rank_list
    def predict(self, pil_image):
        image = pil_image.convert('RGB')
        norm = Normalize(mean=mu, std=sigma)  # normalize image pixels range to [-1,1]
        _transf = Compose([
            Resize((224, 224)),  # Resize to 224x224
            ToTensor(),
            norm
        ])
        input_tensor = _transf(image).unsqueeze(0)
        # get default mu,sigma

        # Move the model and the input tensor to the same device
        input_tensor = input_tensor.to(share.device)

        # Make the model evaluate the input tensor and get the prediction
        model = self.model.eval()
        with torch.no_grad():
            logits = model(input_tensor).logits
            pred = logits.argmax(1).item()
        image_type = labels[pred]
        prob = torch.softmax(logits, dim=1).squeeze().tolist()
        prob_map = dict(zip(labels, prob))
        max_prob = max(prob_map, key=prob_map.get)
        return {
            "image_type": image_type,
            "prob_map": prob_map,
            "max_prob": max_prob
        }
