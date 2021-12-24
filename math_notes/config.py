from pathlib import Path


# Read the app_id and app_key required for MathPix API.
app_id_path = Path("configs/app_id.txt")
app_key_path = Path("configs/app_key.txt")

APP_ID = app_id_path.read_text()
APP_KEY = app_key_path.read_text()
