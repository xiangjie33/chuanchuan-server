import configparser
import os
import sys

if sys.platform.startswith("win"):
    conf_file = "config-win.ini"
else:
    conf_file = "config-linux.ini"
separator = os.path.sep
config_path = os.path.join(os.getcwd(), "config" + separator + conf_file)
config_parser = configparser.ConfigParser()
config_parser.read(config_path)

# 七牛云配置
qiniuyun_bucked_name = config_parser.get("qiniuyun", "bucked_name")
qiniuyun_domain_name = config_parser.get("qiniuyun", "domain_name")
qiniuyun_access_key = config_parser.get("qiniuyun", "access_key")
qiniuyun_secret_key = config_parser.get("qiniuyun", "secret_key")

# dt2配置
dt2_dataset_name = config_parser.get("dt2", "dataset_name")
dt2_merge_from_file = config_parser.get("dt2", "merge_from_file")
dt2_model_path = config_parser.get("dt2", "model_path")
dt2_temp_image_path = config_parser.get("dt2", "temp_image_path")

# flask配置
flask_port = config_parser.get("flask", "port")
flask_host = config_parser.get("flask", "host")
flask_debug = config_parser.get("flask", "debug")
