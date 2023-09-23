import os
import time
import platform

import numpy as np
from detectron2.utils.visualizer import Visualizer, ColorMode
import cv2
from detectron2.config import get_cfg
from detectron2.engine import DefaultPredictor

from config import config
from entity.chuanchuan_model import PredictorModel  # 导入注册文件，完成注册
from entity.chuanchuan_dataset import PredictorData  # 导入注册文件，完成注册
from log.sys_log import logger
import entity.upload_image as upload_image
import utils.file_util
from utils import file_util


class predictor_image:
    # 预测模型对象
    predictor = None

    predictor_model = None

    predictor_dataset = None

    upload_image_obj = None

    def __init__(self, model_path="", merge_from_file="", dataset_name=""):
        self.get_predictor_model(model_path, merge_from_file)
        self.get_predictor_dataset(dataset_name)
        self.get_predictor()
        self.get_upload_image_obj()

    def get_predictor_model(self, model_path="", merge_from_file=""):
        if self.predictor_model is None:
            self.predictor_model = PredictorModel(model_path, merge_from_file)
        else:
            if (
                self.predictor_model.get("model_path") == model_path
                and self.predictor_model.get("merge_from_file") == merge_from_file
            ):
                logger.info("model_path or merge_from_file is not update")
                pass
            else:
                logger.info("model_path or merge_from_file is update")
                self.predictor_model = PredictorModel(model_path, merge_from_file)

    def get_predictor_dataset(self, dataset_name=""):
        if self.predictor_dataset is None:
            self.predictor_dataset = PredictorData(dataset_name)
        else:
            if self.predictor_dataset.get("thing_classes") == dataset_name:
                logger.info("thing_classes is not update")
                pass
            else:
                logger.info("thing_classes is update")
                self.predictor_dataset = PredictorData(dataset_name)

    # 加载预测模型对象
    def get_predictor(self):
        model_conf = self.predictor_model
        cfg = get_cfg()
        cfg.MODEL.DEVICE = "cpu"  # 设置模型设备为CPU
        # 加载模型文件
        cfg.merge_from_file(model_conf.get("merge_from_file"))
        # 加载训练好的模型文件
        cfg.MODEL.WEIGHTS = model_conf.get("model_path")
        logger.info("loading from: {}".format(cfg.MODEL.WEIGHTS))
        cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = 0.6  # 阈值
        cfg.MODEL.ROI_HEADS.NUM_CLASSES = 1  # 类别数
        self.predictor = DefaultPredictor(cfg)

    def load_model(self, image_data, qiniu_image_name=""):
        try:
            nparr = np.frombuffer(image_data, np.uint8)
            image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            outputs = self.predictor(image)
            dataset = self.predictor_dataset
            v = Visualizer(
                image[:, :, ::-1],
                metadata=dataset,
                scale=0.8,
                instance_mode=ColorMode.IMAGE_BW,  # remove the colors of unsegmented pixels
            )
            num_matches = len(outputs["instances"])
            v = v.draw_instance_predictions(outputs["instances"].to("cpu"))
            # img = v.get_image()[:, :, ::-1]
            # cv2.imshow('rr', img)
            # cv2.waitKey(0)

            timestamp = time.time()
            system = platform.system()
            if str(system).lower() == "Windows".lower():
                image_path = "D:\\files\\PyCode\\resources\\result\\" + str(3) + ".jpg"
            else:
                image_path = "/tmp/" + str(timestamp) + ".jpg"
            cv2.imwrite(image_path, v.get_image()[:, :, ::-1])
            domain_name = self.upload_image_obj.get_attribute("domain_name")
            recognition_image_name = qiniu_image_name.replace(domain_name, "").replace(
                ".", "_recognition."
            )
            recognition_image = self.upload_image_obj.upload_img(
                image_path, recognition_image_name
            )
            return {"num_matches": num_matches, "recognition_image": recognition_image}
        except Exception as e:
            logger.error(e)
            return {"num_matches": -1, "image": -1}

    def get_upload_image_obj(self):
        if self.upload_image_obj is None:
            self.upload_image_obj = upload_image.get_upload_image_instance()
        return self.upload_image_obj


def get_predictor_image_instance():
    merge_from_file = config.dt2_merge_from_file
    model_path = config.dt2_model_path
    dataset_name = config.dt2_dataset_name
    if not file_util.file_exists(model_path):
        model_path = os.path.join(
            os.getcwd(), "model" + file_util.separator + "model_final.pth"
        )
    return predictor_image(model_path, merge_from_file, dataset_name)
