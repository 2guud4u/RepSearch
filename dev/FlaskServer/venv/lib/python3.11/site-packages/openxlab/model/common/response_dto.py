import re


class ReturnDto:
    def __init__(self, trace_id=None, msg_code=None, msg=None, data=None, total=None, success=None):
        self.trace_id = trace_id
        self.msg_code = msg_code
        self.msg = msg
        self.data = data
        self.total = total
        self.success = success

    # 将驼峰型属性名转换为下划线型属性名
    @classmethod
    def from_camel_case(cls, camel_dict):
        snake_dict = {}
        for key, value in camel_dict.items():
            snake_key = re.sub(r'(?<!^)(?=[A-Z])', '_', key).lower()
            snake_dict[snake_key] = value
        return cls(**snake_dict)


class DownloadUrlDto:
    def __int__(self, url=None, updating=None, updating_readme=None):
        self.url = url
        self.updating = updating
        self.updating_readme = updating_readme
