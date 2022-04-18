import os

DEBUG = True
SQLALCHEMY_DATABASE_URI = "sqlite:///data.db"
SQLALCHEMY_TRACK_MODIFICATIONS = False
PROPAGATE_EXCEPTIONS = True

JWT_SECRET_KEY = os.environ["JWT_SECRET_KEY"]
JWT_BLOCKLIST_ENABLED = True
JWT_BLOCKLIST_TOKEN_CHECKS = [
    "access",
    "refresh",
]

# UPLOADED_IMAGES_DEST = os.path.join("static", "images")  # manage root folder


