from tasks import add

for i in range(3):
    result = add.delay(i, 2 * i)  # 使用celery提供的接口delay进行调用任务函数

while not result.ready():
    pass
print("完成:", result.get())
