import os
import re
from typing import Union
from werkzeug.datastructures import FileStorage

from flask_uploads import UploadSet, IMAGES

IMAGE_SET = UploadSet("images", IMAGES)


def save_image(image: FileStorage, folder: str = None, name: str = None) -> str:
    """save image esencialemtne va a tomar un FileStorage y guardara la imagen en un folder"""
    return IMAGE_SET.save(image, folder, name)


def get_path(filename: str = None, folder: str = None) -> str:
    """Nos regresara el full path de una imagen"""
    return IMAGE_SET.path(filename, folder)


def find_image_any_format(filename: str, folder: str) -> Union[str, None]:
    """toma un filename y regresa una imagen con cualquiera de los formatos aceptados"""
    for _formart in IMAGES:
        image = f"{filename}.{_formart}"
        image_path = IMAGE_SET.path(filename=image, folder=folder)
        if os.path.isfile(image_path):
            return image_path
    return None


def _retrieve_filename(file: Union[str, FileStorage]) -> str:
    """toma una lista de file storage y regresa el file name.
    permite que le pasemos un file name o un fileStorage
    y simepre nos regresara el filename
    """

    if isinstance(file, FileStorage):
        return file.filename
    return file


def is_filename_safe(file: Union[str, FileStorage]) -> bool:
    """comprueba nuestro regex y regresa si el string coincide o no"""
    filename = _retrieve_filename(file)
    allowed_format = "|".join(IMAGES)
    regex = f"^[a-zA-Z0-9][a-zA-Z0-9_()-\.]*\.({allowed_format})$"
    return re.match(regex, filename) is not None


def get_basename(file: Union[str, FileStorage]) -> str:
    """regresa el fullname de una imagen en el path
    get_basename('some/folder/image.jpg') returns 'image.jpg'
    """
    filename = _retrieve_filename(file)
    return os.path.split(filename)[1]


def get_extension(file: Union[str, FileStorage]) -> str:
    """regresa el file extension
    get_extension('image.jpg') return '.jpg'"""
    filename = _retrieve_filename(file)
    return os.path.splitext(filename)[1]
