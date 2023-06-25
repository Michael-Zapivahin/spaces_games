import random
import curses
import asyncio
import time
import os

from curses_tools import (
    draw_frame,
    read_controls,
    get_frame_size,
)

from physics import update_speed
from obstacles import Obstacle
from explosion import explode
from game_scenario import get_garbage_delay_tics


window_size = curses.initscr().getmaxyx()

game_over_phrase = """
 / ____|                       / __ \                
 | |  __  __ _ _ __ ___   ___  | |  | |_   _____ _ __ 
 | | |_ |/ _` | '_ ` _ \ / _ \ | |  | \ \ / / _ \ '__|
 | |__| | (_| | | | | | |  __/ | |__| |\ V /  __/ |   
  \_____|\__,_|_| |_| |_|\___|  \____/  \_/ \___|_|
  """

COLUMN_START = 1
COLUMN_END = window_size[1]-6
ROW_START = 1
ROW_END = window_size[0]-2
BORDER_OFFSET = 1

year = 1957
FREQUENCY = 50
STARS_FLASH_FREQUENCY = 3
STARS_COUNT = 50
TIC_TIMEOUT = 10

coroutines = []
obstacles = []
obstacles_in_last_collision = []


async def display_current_year(canvas):
    global year

    while True:
        draw_frame(canvas, 0, 0, f'Year - {year}')
        await asyncio.sleep(0)
        draw_frame(canvas, 0, 0, f'Year - {year}', negative=True)
        await asyncio.sleep(0)


async def count_years():
    global year

    while True:
        year += 1
        await sleep(FREQUENCY)


async def show_game_over(canvas):
    canvas_height, canvas_width = canvas.getmaxyx()
    center_row, center_column = (canvas_height // 4, (canvas_width // 4) - 20)
    while True:
        draw_frame(canvas, center_row, center_column, game_over_phrase)
        await asyncio.sleep(0)


async def sleep(tics=1):
    for _ in range(tics):
        await asyncio.sleep(0)


async def fill_orbit_with_garbage(canvas, garbage_frames):
    global year

    canvas_height, canvas_width = canvas.getmaxyx()
    while True:
        garbage_delay = get_garbage_delay_tics(year) * 10
        await sleep(garbage_delay)
        if not garbage_delay:
            continue

        random_frame = random.choice(garbage_frames)
        _, frame_width = get_frame_size(random_frame)
        random_column = random.randint(1, canvas_width - frame_width - BORDER_OFFSET)
        coroutines.append(fly_garbage(canvas, random_column, random_frame))

        await asyncio.sleep(0)


async def fly_garbage(canvas, column, garbage_frame, speed=0.5):
    """Animate garbage, flying from top to bottom. Сolumn position will stay same, as specified on start."""
    rows_number, columns_number = canvas.getmaxyx()

    column = max(column, 0)
    column = min(column, columns_number - 1)

    row = 0

    frame_height, frame_width = get_frame_size(garbage_frame)
    obstacle = Obstacle(row, column, frame_height, frame_width)
    obstacles.append(obstacle)

    while row < rows_number:
        if obstacle in obstacles_in_last_collision:
            obstacles.remove(obstacle)
            obstacles_in_last_collision.remove(obstacle)
            await explode(canvas, row, column)
            return
        draw_frame(canvas, row, column, garbage_frame)
        for index in range(10):
            await asyncio.sleep(0)
        draw_frame(canvas, row, column, garbage_frame, negative=True)
        row += speed
        obstacle.row += speed

    obstacles.remove(obstacle)


async def fire(canvas, start_row, start_column, rows_speed=-0.3, columns_speed=0):
    """Display animation of gun shot, direction and speed can be specified."""

    row, column = start_row, start_column

    canvas.addstr(round(row), round(column), '*')
    await sleep(3)

    canvas.addstr(round(row), round(column), 'O')
    await sleep(3)

    canvas.addstr(round(row), round(column), ' ')
    await sleep(3)

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

        for obstacle in obstacles:
            if obstacle.has_collision(row, column):
                obstacles_in_last_collision.append(obstacle)
                return


async def draw_ship(canvas, ship_row, ship_column, frame_1, frame_2, row_speed, column_speed):
    global year
    while True:
        frame_height, frame_width = get_frame_size(frame_1)
        rows_direction, columns_direction, space_pressed = read_controls(canvas)
        row_speed, column_speed = update_speed(row_speed, column_speed, rows_direction, columns_direction)

        if space_pressed and year > 2020:
            coroutines.append(fire(canvas, ship_row, ship_column+2, -0.1))

        ship_row += row_speed
        ship_column += column_speed
        ship_row = max(ship_row, ROW_START)
        ship_row = min(ship_row, ROW_END - 8)
        ship_column = max(ship_column, COLUMN_START)
        ship_column = min(ship_column, COLUMN_END)

        draw_frame(canvas, ship_row, ship_column, frame_1)
        await asyncio.sleep(0)
        draw_frame(canvas, ship_row, ship_column, frame_1, True)
        draw_frame(canvas, ship_row, ship_column, frame_2)
        await asyncio.sleep(0)
        draw_frame(canvas, ship_row, ship_column, frame_2, True)

        for obstacle in obstacles:
            if obstacle.has_collision(ship_row, ship_column, frame_height, frame_width):
                obstacles_in_last_collision.append(obstacle)
                await show_game_over(canvas)
                return


async def blink(canvas, row, column, symbol='*', delay=1):

    await sleep(delay)

    while True:
        canvas.addstr(row, column, symbol, curses.A_DIM)
        await sleep(TIC_TIMEOUT * 20)

        canvas.addstr(row, column, symbol)
        await sleep(TIC_TIMEOUT * 3)

        canvas.addstr(row, column, symbol, curses.A_BOLD)
        await sleep(TIC_TIMEOUT * 5)

        canvas.addstr(row, column, symbol)
        await sleep(TIC_TIMEOUT * 3)


def draw(canvas):

    with open("ship_s_frames/rocket_frame_1.txt", "r") as my_file:
        frame_1 = my_file.read()
    with open("ship_s_frames/rocket_frame_2.txt", "r") as my_file:
        frame_2 = my_file.read()

    trash_frames = []
    path = os.path.join(os.getcwd(), 'trash_s_frames')
    for filename in os.listdir(path):
        with open(os.path.join(path, filename), "r") as my_file:
            trash_frames.append(my_file.read())

    row_speed, column_speed = 0.5, 0.5
    ship_row, ship_column = ROW_START + 2, int(COLUMN_END / 2)
    coroutine_frames = draw_ship(canvas, ship_row, ship_column, frame_1, frame_2, row_speed, column_speed)
    coroutines.append(coroutine_frames)
    symbols = '+*.:'

    for _ in range(STARS_COUNT):
        coroutines.append(blink(
            canvas,
            random.randint(ROW_START, ROW_END),
            random.randint(COLUMN_START, COLUMN_END),
            random.choice(symbols),
            random.randint(1, STARS_FLASH_FREQUENCY)
        ))

    coroutines.append(fill_orbit_with_garbage(canvas, trash_frames))
    coroutines.append(count_years())
    coroutines.append(display_current_year(canvas))

    canvas.border()
    while True:
        canvas.refresh()
        for coroutine in coroutines.copy():
            try:
                coroutine.send(None)
            except StopIteration or KeyboardInterrupt:
                coroutines.remove(coroutine)
        time.sleep(1 / FREQUENCY)


def main():
    window = curses.initscr()
    window.nodelay(True)
    curses.curs_set(0)
    curses.update_lines_cols()
    curses.A_DIM
    curses.wrapper(draw)


if __name__ == '__main__':
    main()
