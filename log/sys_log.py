import logging

log_file = 'chuanchuan-debug-log.log'  # 日志文件名
# 创建记录器
logger = logging.getLogger('app')

# 配置记录器
logger.setLevel(logging.INFO)

# 创建文件处理程序
file_handler = logging.FileHandler(log_file)

# 配置文件处理程序
file_handler.setLevel(logging.INFO)

# 创建格式化器
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# 绑定格式化器到文件处理程序
file_handler.setFormatter(formatter)

# 将文件处理程序添加到记录器
logger.addHandler(file_handler)

# 配置日志记录器
logging.basicConfig(filename=log_file, level=logging.DEBUG)


def add_request_info(request):
    ip_address = request.remote_addr  # 获取请求的 IP 地址
    user_agent = request.user_agent  # 获取请求的 User-Agent 头部信息
    logger.info(
        'restapi[' + str(request.path) + ']' + 'request ip: ' + str(ip_address) + ' user_agent: ' + str(user_agent))
