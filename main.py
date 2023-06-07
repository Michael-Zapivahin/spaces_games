import random
import time
import curses
import asyncio

import curses_tools


async def draw_frame(canvas, row, column, frame_1, frame_2, delay):

    curses_tools.draw_frame(canvas, row, column, frame_1)
    for time in delay:
        await asyncio.sleep(0)
    curses_tools.draw_frame(canvas, row, column, frame_1, True)
    curses_tools.draw_frame(canvas, row, column, frame_2)
    for time in delay:
        await asyncio.sleep(0)
    curses_tools.draw_frame(canvas, row, column, frame_2, True)



async def fire(canvas, start_row, start_column, rows_speed=-0.3, columns_speed=0.6):
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

    while 0 < row < max_row and 0 < column < max_column:
        canvas.addstr(round(row), round(column), symbol)
        await asyncio.sleep(0)
        canvas.addstr(round(row), round(column), ' ')
        row += rows_speed
        column += columns_speed


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


def draw_blink(canvas):
    with open("rocket_frame_1.txt", "r") as my_file:
        frame_1 = my_file.read()
    with open("rocket_frame_2.txt", "r") as my_file:
        frame_2 = my_file.read()

    coroutines = []
    coroutine_frames = draw_frame(canvas, 2, 75, frame_1, frame_2, range(1, 10))
    symbols = '+*.:'

    for column in range(1, 5):
        for row in range(1, 5):
            coroutines.append(blink(
                canvas,
                random.randint(1, 13),
                random.randint(1, 70),
                random.choice(symbols),
                range(1, random.randint(1, 20))
            ))
            coroutines.append(blink(
                canvas,
                random.randint(1, 13),
                random.randint(90, 160),
                random.choice(symbols),
                range(1, random.randint(1, 20))
            ))

    canvas.border()
    while True:
        for coroutine in coroutines:
            try:
                coroutine_frames.send(None)
            except StopIteration:
                coroutine_frames = draw_frame(canvas, 2, 75, frame_1, frame_2, range(1, 20))
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
    curses.wrapper(draw_blink)


if __name__ == '__main__':
    main()
