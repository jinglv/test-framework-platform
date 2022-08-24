from typing import Any

from ninja import Schema


class ProjectIn(Schema):
    """
    新建项目入参
    """
    name: str
    git_name: str
    git_address: str
    describe: str
    image: str = None


class ProjectListOut(Schema):
    """
    项目列表出参
    """
    id: int
    name: str
    describe: str
    image: str
    create_time: Any
