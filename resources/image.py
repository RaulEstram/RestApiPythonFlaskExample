from werkzeug.datastructures import FileStorage
from flask_restful import Resource
from flask_uploads import UploadNotAllowed
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity

from libs import image_helper
from libs.strings import gettext

from schemas.image import ImageSchema

image_schema = ImageSchema()


class ImageUpload(Resource):
    @jwt_required()
    def post(self):
        """
        sera usada para subir imagenes
        usara JWT para recuperar informacion de usuario y despues guardar la imagen el el folder del usuario

        si hay un conflicto en el nombre del archivo, agregara un numero al final.
        """
        data = image_schema.load(request.files)
        # request.files es una diccionario adentro de request, que tiene la key del nombre del archivo de la data del archivo
        # la data siempre sera un fileStorage object from werkzeug
        # por lo tanto es como tener --> {"image": FileStorage}
        user_id = get_jwt_identity()
        folder = f"user_{user_id}"  # static/images/user_n
        try:
            image_path = image_helper.save_image(data['image'], folder=folder)
            basename = image_helper.get_basename(image_path)
            return {"message": gettext("image_uploaded").format(basename)}, 201
        except UploadNotAllowed:
            extension = image_helper.get_extension(data['image'])
            return {"message": gettext("image_illegal_extension").format(extension)}, 400
