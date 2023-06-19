import asyncio

async def run_timer(secs):

    for secs_left in range(secs, 0, -1):
        print(f'Осталось {secs_left} сек.')
        await asyncio.sleep(3)

    print('Время вышло!')
    print('\a')  # says beep with ASCII BEL symbol

coroutine = run_timer(3)
asyncio.run(coroutine)
