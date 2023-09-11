import json
import re


class ReturnDto:
    def __init__(self, trace_id=None, msg_code=None, msg=None, data=None, total=None, success=None):
        self.trace_id = trace_id
        self.msg_code = msg_code
        self.msg = msg
        self.data = data
        self.total = total
        self.success = success

    def is_success(self):
        return self.msg_code == '10000'

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)

    # 将驼峰型属性名转换为下划线型属性名
    @classmethod
    def from_camel_case(cls, camel_dict):
        snake_dict = {}
        for key, value in camel_dict.items():
            snake_key = re.sub(r'(?<!^)(?=[A-Z])', '_', key).lower()
            snake_dict[snake_key] = value
        return cls(**snake_dict)
