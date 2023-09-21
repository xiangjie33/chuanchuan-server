from qiniu import Auth, put_file
import uuid
from config import config


class upload_image:
    _bucked_name = "chuanchuan-original-images"
    _domain_name = "http://s14u8e8hs.hn-bkt.clouddn.com/"
    _access_key = "qNFSgE8pZc7sIer_CAb8JZ2gOYdtXxddxo3rm0J0"
    _secret_key = "h9BXrmIJxNH84isAPhcq1XoZeO1tqaZvjLNghfav"
    _qiniu_token = None

    def __init__(self):
        self._domain_name = config.qiniuyun_domain_name
        self._bucked_name = config.qiniuyun_bucked_name
        self._access_key = config.qiniuyun_access_key
        self._secret_key = config.qiniuyun_secret_key

    def get_attribute(self, item):
        if item == "bucked_name":
            return self._bucked_name
        if item == "domain_name":
            return self._domain_name
        return None

    def qiniu_token(self, bucked_name):
        if self._qiniu_token is None:
            q = Auth(access_key=self._access_key, secret_key=self._secret_key)
            token = q.upload_token(bucked_name)
            return token
        else:
            self._qiniu_token

    def upload_img(self, file_path, image_name=None, bucked_name=_bucked_name):
        """
        收集本地信息到云服务器上
        参考地址：https://developer.qiniu.com/kodo/sdk/1242/python
        """
        # 指定上传空间，获取token
        token = self.qiniu_token(bucked_name)
        # 指定图片名称
        if image_name is not None:
            file_name = image_name
        else:
            file_name = "{}.png".format(uuid.uuid4())
        ret, info = put_file(token, file_name, file_path)
        img_url = self._domain_name + ret.get("key")
        return img_url


def get_upload_image_instance():
    return upload_image()
