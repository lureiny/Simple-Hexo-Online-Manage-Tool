from flask import request
import hmac, hashlib
import logging, time
import base64

logger = logging.getLogger('custom')
system_logger = logging.getLogger("system_hexo")


def github(request: request, key: str) -> list:
    try:
        signature = request.headers["X-Hub-Signature"]
    except KeyError:
        logger.info("非法访问，非github请求")
        return False, {"status": "Error", "message": "Forbidden"}, 403
    if signature.split("=")[0] != "sha1":
        logger.debug("不支持的hash算法: {}".format(signature.split("=")[0]))
        return False, {"status": "Error", "message": "Unsupported hash algorithm"}, 403
    sha1_hex = hmac.new(key=key.encode("utf-8"), msg=request.data, digestmod=hashlib.sha1).hexdigest()
    if sha1_hex != signature.split("=")[1]:
        logger.debug("数据校验失败")
        return False, {"status": "Error", "message": "Forbidden"}, 403
    return True, {"status": "Success", "message": "Success"}, 200


def gitee(request: request, key: str) -> list:
    try:
        signature = request.headers["X-Gitee-Token"]
        times = request.headers["X-Gitee-Timestamp"]
    except KeyError:
        logger.info("非法访问，非gitee请求")
        return False, {"status": "Error", "message": "Forbidden"}, 403
    if time.time() - int(times) / 1000 > 3600:
        logger.info("非法访问，非github请求")
        return False, {"status": "Error", "message": "Forbidden"}, 403
    sha1_hex = hmac.new(key=key.encode("utf-8"), msg="{}\n{}".format(times, key).encode("utf-8"), digestmod=hashlib.sha256).digest()
    sha1_hex = base64.b64encode(sha1_hex).decode("utf-8")
    if sha1_hex != signature:
        logger.debug("数据校验失败")
        return False, {"status": "Error", "message": "Forbidden"}, 403
    return True, {"status": "Success", "message": "Success"}, 200