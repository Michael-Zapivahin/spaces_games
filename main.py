import random
import time
import curses
import asyncio

import curses_tools


window_size = curses.initscr().getmaxyx()

COLUMN_START = 1
COLUMN_END = window_size[1]-6
ROW_START = 1
ROW_END = window_size[0]-2

FREQUENCY = 100
STARS_FLASH_FREQUENCY = 3
STARS_COUNT = 50
TIC_TIMEOUT = 10


async def fire(canvas, start_row, start_column, rows_speed=-0.3, columns_speed=0):
    """Display animation of gun shot, direction and speed can be specified."""

    row, column = start_row, start_column

    canvas.addstr(round(row), round(column), '*')
    await asyncio.sleep(0)

    canvas.addstr(round(row), round(column), 'O')
    await asyncio.sleep(0)
    canvas.addstr(round(row), round(column), ' ')

    row += rows_speed
    column += columns_speed

    symbol = '-' if columns_speed else '|'

    rows, columns = canvas.getmaxyx()
    max_row, max_column = rows - 1, columns - 1

    curses.beep()
    while True:
        while 0 < row < max_row and 0 < column < max_column:
            canvas.addstr(round(row), round(column), symbol)
            await asyncio.sleep(0)
            canvas.addstr(round(row), round(column), ' ')
            row += rows_speed
            column += columns_speed
        await asyncio.sleep(0)


async def draw_frame(canvas, ship_row, ship_column, frame_1, frame_2):
    while True:
        rows_direction, columns_direction, space_pressed = curses_tools.read_controls(canvas)
        ship_row += rows_direction
        ship_row = max(ship_row, ROW_START)
        ship_row = min(ship_row, ROW_END - 8)
        ship_column += columns_direction
        ship_column = max(ship_column, COLUMN_START)
        ship_column = min(ship_column, COLUMN_END)

        curses_tools.draw_frame(canvas, ship_row, ship_column, frame_1)
        await asyncio.sleep(0)
        curses_tools.draw_frame(canvas, ship_row, ship_column, frame_1, True)
        curses_tools.draw_frame(canvas, ship_row, ship_column, frame_2)
        await asyncio.sleep(0)
        curses_tools.draw_frame(canvas, ship_row, ship_column, frame_2, True)


async def blink(canvas, row, column, symbol='*', delay=[]):
    for _ in delay:
        await asyncio.sleep(0)

    while True:
        canvas.addstr(row, column, symbol, curses.A_DIM)
        for _ in range(TIC_TIMEOUT * 20):
            await asyncio.sleep(0)

        canvas.addstr(row, column, symbol)
        for _ in range(TIC_TIMEOUT * 3):
            await asyncio.sleep(0)

        canvas.addstr(row, column, symbol, curses.A_BOLD)
        for _ in range(TIC_TIMEOUT * 5):
            await asyncio.sleep(0)

        canvas.addstr(row, column, symbol)
        for _ in range(TIC_TIMEOUT * 3):
            await asyncio.sleep(0)


def draw_blink(canvas):

    with open("rocket_frame_1.txt", "r") as my_file:
        frame_1 = my_file.read()
    with open("rocket_frame_2.txt", "r") as my_file:
        frame_2 = my_file.read()

    coroutines = []
    ship_row, ship_column = ROW_START + 2, int(COLUMN_END / 2)
    coroutine_frames = draw_frame(canvas, ship_row, ship_column, frame_1, frame_2)
    coroutines.append(coroutine_frames)
    symbols = '+*.:'

    coroutines.append(fire(canvas, ROW_END, COLUMN_START, -0.1, 2))

    for _ in range(STARS_COUNT):
        coroutines.append(blink(
            canvas,
            random.randint(ROW_START, ROW_END),
            random.randint(COLUMN_START, COLUMN_END),
            random.choice(symbols),
            range(random.randint(1, STARS_FLASH_FREQUENCY))
        ))

    canvas.border()
    while True:
        canvas.refresh()
        for coroutine in coroutines:
            try:
                coroutine.send(None)
            except StopIteration or KeyboardInterrupt:
                pass
        time.sleep(1 / FREQUENCY)


def main():
    window = curses.initscr()
    window.nodelay(True)
    curses.curs_set(0)
    curses.update_lines_cols()
    curses.A_DIM
    curses.wrapper(draw_blink)


if __name__ == '__main__':
    main()
