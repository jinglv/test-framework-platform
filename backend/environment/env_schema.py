from typing import Optional, Any

from ninja import Schema


class EnvIn(Schema):
    """
    环境入参
    """
    name: str
    project_id: int
    env: Optional[str] = None
    browser: Optional[str] = None
    base_url: Optional[str] = None


class EnvListOut(Schema):
    """
    环境列表出参
    """
    id: int
    name: str
    project_name: str
    env: str
    browser: str
    base_url: str
    update_time: Any
