# Create your views here.
import hashlib
import os

from django.db import transaction
from ninja import Router, UploadedFile, File

from backend.api_response import response, Error
from backend.settings import IMAGE_DIR

router = Router(tags=["commons"])


@router.post("/upload")
@transaction.atomic
def project_image_upload(request, file: UploadedFile = File(...)):
    """
    项目图片上传
    """
    # 判断文件后缀名
    suffix = file.name.split(".")[-1]
    if suffix not in ["png", "jpg", "jpeg", "gif"]:
        return response(error=Error.IMAGE_SUFFIX_ERROR)

    # 判断文件大小 1024 * 1024 * 2 = 2MB
    if file.size > 2097152:
        return response(error=Error.IMAGE_SIZE_ERROR)

    # 文件名生成md5
    file_md5 = hashlib.md5(bytes(file.name, encoding="utf8")).hexdigest()
    file_name = file_md5 + "." + suffix

    # 保存到本地
    upload_file = os.path.join(IMAGE_DIR, file_name)
    with open(upload_file, 'wb+') as f:
        for chunk in file.chunks():
            f.write(chunk)
    upload_file_info = {
        "name": file_name
    }
    return response(data=upload_file_info)
