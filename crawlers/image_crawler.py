from PIL import Image
from models.responses import CrawlerResponse
from models.image import Image as ImageModel

def crawl(asset_path):
    try:
        image = Image.open(asset_path["path"])
    except IsADirectoryError:
        return CrawlerResponse("ThePathIsADirectory", None)
    except FileNotFoundError:
        return CrawlerResponse("FileNotFound", None)

    image_model = ImageModel(
        asset_path["path"],
        image.filename,
        image.filename.split(".")[-1],
        image.format,
        image.height,
        image.width
    )

    return CrawlerResponse("success", image_model)