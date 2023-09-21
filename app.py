from flask import Flask, request

import config.config
import entity.chuanchuan_controller as predictor_image
from log.sys_log import logger, add_request_info
import entity.upload_image as upload_image
from route.route_method import predict_detail

app = Flask(__name__)


# 获取对象实例
upload_image_obj = upload_image.get_upload_image_instance()
predictor = predictor_image.get_predictor_image_instance()


@app.route("/")
def hello_world():
    add_request_info(request=request)
    logger.info("restapi[/]-hello world")
    return "Hello World!"


# 定义API路由
@app.route("/predict", methods=["POST"])
def predict():
    add_request_info(request=request)
    logger.info("restapi[method: POST, API: /predict]-start")
    # 从请求中获取图像数据
    image = request.files["image"]
    return predict_detail(image, upload_image_obj, predictor)


if __name__ == "__main__":
    logger.info("boot-start")
    port = config.config.flask_port
    host = config.config.flask_host
    debug = config.config.flask_debug
    app.run(debug=debug, host=host, port=port)
