from ninja import Schema


class RegisterIn(Schema):
    """
    注册数据入参校验
    """
    username: str
    password: str
    confirm_password: str


class RegisterOut(Schema):
    """
    注册数据出参校验
    """
    id: int
    username: str


class LoginIn(Schema):
    """
    登录参数入参校验
    """
    username: str
    password: str
