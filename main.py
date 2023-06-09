import random
import time
import curses
import asyncio

import curses_tools


async def draw_frame(canvas, row, column, frame_1, frame_2, delay):
    curses_tools.draw_frame(canvas, row, column, frame_1)
    for _ in delay:
        await asyncio.sleep(0)
    curses_tools.draw_frame(canvas, row, column, frame_1, True)
    curses_tools.draw_frame(canvas, row, column, frame_2)
    for time in delay:
        await asyncio.sleep(0)
    curses_tools.draw_frame(canvas, row, column, frame_2, True)


async def blink(canvas, row, column, symbol='*', delay=[]):
    for _ in delay:
        await asyncio.sleep(0)

    while True:
        canvas.addstr(row, column, symbol, curses.A_DIM)
        for _ in range(1, 11):
            await asyncio.sleep(0)

        canvas.addstr(row, column, symbol)
        for _ in range(1, 3):
            await asyncio.sleep(0)

        canvas.addstr(row, column, symbol, curses.A_BOLD)
        for _ in range(1, 5):
            await asyncio.sleep(0)

        canvas.addstr(row, column, symbol)
        for _ in range(1, 3):
            await asyncio.sleep(0)


def draw_blink(canvas):

    with open("rocket_frame_1.txt", "r") as my_file:
        frame_1 = my_file.read()
    with open("rocket_frame_2.txt", "r") as my_file:
        frame_2 = my_file.read()

    coroutines = []
    coroutine_frames = draw_frame(canvas, 2, 75, frame_1, frame_2, range(1, 10))
    symbols = '+*.:'
    ship_row, ship_column = 2, 75

    for _ in range(1, 5):
        for _ in range(1, 5):
            coroutines.append(blink(
                canvas,
                random.randint(1, 13),
                random.randint(1, 72),
                random.choice(symbols),
                range(1, random.randint(1, 20))
            ))
            coroutines.append(blink(
                canvas,
                random.randint(1, 13),
                random.randint(80, 160),
                random.choice(symbols),
                range(1, random.randint(1, 20))
            ))

    canvas.border()
    while True:
        for coroutine in coroutines:
            try:
                coroutine_frames.send(None)
            except StopIteration:
                rows_direction, columns_direction, space_pressed = curses_tools.read_controls(canvas)
                ship_row += rows_direction
                ship_row = max(ship_row, 1)
                ship_row = min(ship_row, 5)
                ship_column += columns_direction
                ship_column = max(ship_column, 2)
                ship_column = min(ship_column, 158)
                coroutine_frames = draw_frame(canvas, ship_row, ship_column, frame_1, frame_2, range(1, 2))
            try:
                coroutine.send(None)
                canvas.refresh()
                time.sleep(1/1000)
            except StopIteration:
                break


def main():
    window = curses.initscr()
    window.nodelay(True)
    curses.curs_set(0)
    curses.update_lines_cols()
    curses.A_DIM
    curses.wrapper(draw_blink)


if __name__ == '__main__':
    main()
