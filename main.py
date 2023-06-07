import time
import curses








def draw(canvas):
    row, column = (5, 20)
    while True:
        canvas.clear()
        canvas.border()
        canvas.addstr(row, column, '*', curses.A_DIM)
        canvas.refresh()
        time.sleep(2)
        canvas.addstr(row, column, '1')
        canvas.refresh()
        time.sleep(3/10)
        canvas.addstr(row, column, '2', curses.A_BOLD)
        canvas.refresh()
        time.sleep(5/10)
        canvas.addstr(row, column, '3')
        canvas.refresh()
        time.sleep(3/10)


if __name__ == '__main__':
    window = curses.initscr()
    curses.curs_set(0)
    curses.update_lines_cols()
    curses.A_DIM
    curses.wrapper(draw)
