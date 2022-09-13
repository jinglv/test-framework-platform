from enum import Enum

from ninja import Schema


class EnvType(str, Enum):
    """环境类型"""
    product = "product"
    preannouncement = "preannouncement"


class RunCaseIn(Schema):
    """运行测试用例入参"""
    env: int  # 环境ID, 从Env表查询
