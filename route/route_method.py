import os
import time

from flask import jsonify

from config import config
from log.sys_log import logger


def predict_detail(image, upload_image_obj, predictor):
    image_read = image.read()
    timestamp = time.time()
    temp_image_path = config.dt2_temp_image_path + str(timestamp) + image.filename
    with open(temp_image_path, "wb") as file:
        file.write(image_read)
    original_images_path = upload_image_obj.upload_img(temp_image_path)
    os.remove(temp_image_path)
    logger.info("restapi[method: POST, API: /predict]-end")
    res = predictor.load_model(image_read, original_images_path)
    res["original_image"] = original_images_path
    return jsonify(res)
