import asyncio


async def count(x):
    print(x * x)
    await asyncio.sleep(1)
    print('finish')


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    tasks = []
    for i in range(10):
        # task = asyncio.ensure_future(count(i))
        task = loop.create_task(count(i))
        tasks.append(task)
    loop.run_until_complete(asyncio.wait(tasks))
