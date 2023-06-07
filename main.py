import random
import time
import curses
import asyncio


async def blink(canvas, row, column, symbol='*', delay=[]):
    for time in delay:
        await asyncio.sleep(0)

    while True:
        canvas.addstr(row, column, f'{symbol}-1', curses.A_DIM)
        for counter in range(1, 11):
            await asyncio.sleep(0)

        canvas.addstr(row, column, f'{symbol}-2')
        for counter in range(1, 3):
            await asyncio.sleep(0)

        canvas.addstr(row, column, f'{symbol}-3', curses.A_BOLD)
        for counter in range(1, 5):
            await asyncio.sleep(0)

        canvas.addstr(row, column, f'{symbol}-4')
        for counter in range(1, 3):
            await asyncio.sleep(0)


def draw(canvas):
    coroutines = []
    symbols = '+*.:'
    for column in range(1, 10):
        for row in range(1, 5):
            coroutines.append(blink(
                canvas,
                random.randint(1, 7),
                random.randint(1, 150),
                random.choice(symbols),
                range(1, random.randint(1, 20))
            ))

    canvas.border()
    while True:
        for coroutine in coroutines:
            try:
                coroutine.send(None)
                canvas.refresh()
                time.sleep(1/200)
            except StopIteration:
                break


def main():
    curses.initscr()
    curses.curs_set(0)
    curses.update_lines_cols()
    curses.A_DIM
    curses.wrapper(draw)


if __name__ == '__main__':
    main()
