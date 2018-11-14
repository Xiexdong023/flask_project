import uuid

"""
工具函数:自定义工具函数,方便项目的代码复用性
"""


def generate_pub_id():
	"""生成uuid 只取前16位作为id,防止他人模仿浏览器行为"""
	return "".join(str(uuid.uuid4()).split("-")[:3])
