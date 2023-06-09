import random
import time
import curses
import asyncio

import curses_tools


FREQUENCY = 1000
FLASH_FREQUENCY = 3
COLUMN_START = 1
COLUMN_END = 160
ROW_START = 1
ROW_END = 13
DELAY = 10
SHIP_DELAY = 2
STARS_COUNT = 100


async def draw_frame(canvas, row, column, frame_1, frame_2, delay):
    curses_tools.draw_frame(canvas, row, column, frame_1)
    for _ in delay:
        await asyncio.sleep(0)
    curses_tools.draw_frame(canvas, row, column, frame_1, True)
    curses_tools.draw_frame(canvas, row, column, frame_2)
    for _ in delay:
        await asyncio.sleep(0)
    curses_tools.draw_frame(canvas, row, column, frame_2, True)


async def blink(canvas, row, column, symbol='*', delay=[]):
    for _ in delay:
        await asyncio.sleep(0)

    while True:
        canvas.addstr(row, column, symbol, curses.A_DIM)
        for _ in range(1, FLASH_FREQUENCY * 4):
            await asyncio.sleep(0)

        canvas.addstr(row, column, symbol)
        for _ in range(1, FLASH_FREQUENCY):
            await asyncio.sleep(0)

        canvas.addstr(row, column, symbol, curses.A_BOLD)
        for _ in range(1, FLASH_FREQUENCY * 2):
            await asyncio.sleep(0)

        canvas.addstr(row, column, symbol)
        for _ in range(1, FLASH_FREQUENCY):
            await asyncio.sleep(0)


def draw_blink(canvas):

    with open("rocket_frame_1.txt", "r") as my_file:
        frame_1 = my_file.read()
    with open("rocket_frame_2.txt", "r") as my_file:
        frame_2 = my_file.read()

    coroutines = []
    ship_row, ship_column = ROW_START + 2, int(COLUMN_END / 2)
    coroutine_frames = draw_frame(canvas, ship_row, ship_column, frame_1, frame_2, range(DELAY))
    # coroutines.append(coroutine_frames)
    symbols = '+*.:'

    for _ in range(STARS_COUNT):
        coroutines.append(blink(
            canvas,
            random.randint(ROW_START, ROW_END),
            random.randint(COLUMN_START, COLUMN_END),
            random.choice(symbols),
            range(random.randint(1, FLASH_FREQUENCY))
        ))

    canvas.border()
    while True:
        for coroutine in coroutines:
            try:
                coroutine.send(None)
                coroutine_frames.send(None)
                canvas.refresh()
                time.sleep(1 / FREQUENCY)
            except StopIteration:
                rows_direction, columns_direction, space_pressed = curses_tools.read_controls(canvas)
                ship_row += rows_direction
                ship_row = max(ship_row, ROW_START)
                ship_row = min(ship_row, ROW_END-8)
                ship_column += columns_direction
                ship_column = max(ship_column, COLUMN_START)
                ship_column = min(ship_column, COLUMN_END)
                coroutine_frames = draw_frame(canvas, ship_row, ship_column, frame_1, frame_2, range(SHIP_DELAY))



def main():
    window = curses.initscr()
    window.nodelay(True)
    curses.curs_set(0)
    curses.update_lines_cols()
    curses.A_DIM
    curses.wrapper(draw_blink)


if __name__ == '__main__':
    main()
