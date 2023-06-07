import time
import curses
import asyncio


async def blink(canvas, row, column, symbol='*'):
    while True:
        canvas.addstr(row, column, symbol+'1', curses.A_DIM)
        await asyncio.sleep(0)

        canvas.addstr(row, column, symbol+'2')
        await asyncio.sleep(0)

        canvas.addstr(row, column, symbol+'3', curses.A_BOLD)
        await asyncio.sleep(0)

        canvas.addstr(row, column, symbol+'4')
        await asyncio.sleep(0)






def draw(canvas):
    row, column = (5, 20)
    coroutine = blink(canvas, 5, 20, '*')
    canvas.border()
    while True:
        try:
            coroutine.send(None)
            canvas.refresh()
            time.sleep(2/4)
        except StopIteration:
            return



if __name__ == '__main__':
    window = curses.initscr()
    curses.curs_set(0)
    curses.update_lines_cols()
    curses.A_DIM
    curses.wrapper(draw)
