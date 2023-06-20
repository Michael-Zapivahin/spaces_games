import random
import curses
import asyncio
import time

from curses_tools import (
    draw_frame,
    read_controls,
    get_frame_size,
)

from physics import update_speed
from obstacles import Obstacle


window_size = curses.initscr().getmaxyx()

COLUMN_START = 1
COLUMN_END = window_size[1]-6
ROW_START = 1
ROW_END = window_size[0]-2

FREQUENCY = 100
STARS_FLASH_FREQUENCY = 3
STARS_COUNT = 50
TIC_TIMEOUT = 10

coroutines = []
obstacles = []




def main():
    window = curses.initscr()
    window.nodelay(True)
    curses.curs_set(0)
    curses.update_lines_cols()
    curses.A_DIM
    curses.wrapper(draw)


if __name__ == '__main__':
    main()
