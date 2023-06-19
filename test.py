import asyncio


async def countdown_minutes_till_one_left(minutes):
    for minutes_left in range(minutes, 1, -1):
        print(f'Осталось {minutes_left} мин.')
        await asyncio.sleep(2)  # one minute


async def countdown_seconds(secs):
    for secs_left in range(secs, 0, -1):
        print(f'Осталось {secs_left} сек.')
        await asyncio.sleep(1)


async def run_five_minutes_timer():

    await countdown_minutes_till_one_left(5)
    await countdown_seconds(8)

    print('Время вышло!')
    print('\a')  # says beep with ASCII BEL symbol

# coroutine = run_five_minutes_timer()
# asyncio.run(coroutine)

loop = asyncio.get_event_loop()
loop.create_task(run_five_minutes_timer())
loop.create_task(run_five_minutes_timer())

loop.run_forever()
