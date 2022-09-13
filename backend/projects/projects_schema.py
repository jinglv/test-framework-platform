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
    git_name: str
    git_address: str
    describe: str
    image: str
    is_delete: bool
    test_num: int
    is_clone: int
   