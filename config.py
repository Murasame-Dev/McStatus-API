import os

BACKGROUND_URL = os.environ.get("BACKGROUND_URL", "https://www.loliapi.com/acg/")
DEFAULT_ICON = os.environ.get("DEFAULT_ICON", "mc_status_img/minecraft-creeper-face.png")
FONT_PATH = os.environ.get("FONT_PATH", "mc_status_img/MiSans-Bold.ttf")
IMAGE_WIDTH = int(os.environ.get("IMAGE_WIDTH", "0"))
IMAGE_HEIGHT = int(os.environ.get("IMAGE_HEIGHT", "0"))
