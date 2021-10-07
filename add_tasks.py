from tasks import add

"""
for i in range(3):
    result = add.delay(i, 2 * i)  # 使用celery提供的接口delay进行调用任务函数

isFailed = result.failed()  # true or failed task result
isSuccess = result.successful()
state = result.state
isFinish = result.ready()
value = result.get()
"""

# 签名调用
sign = add.s(3, 3)
result = sign.delay()
print(result)

sign = add.s()
result = sign.delay(3, 2)
print(result)


# group
from celery import group
result = []
for i in range(10):
    result.append(add.s(i, i))

result_list = group(result)().get()
print(result_list)