import time
import curses








def draw(canvas):
    row, column = (5, 20)
    canvas.border()
    flash = True
    while True:
        if flash:
            canvas.addstr(row, column, '*')
            flash = False
        else:
            canvas.addstr(row, column, ' ')
            flash = True
        canvas.refresh()
        time.sleep(1/10)


if __name__ == '__main__':
    window = curses.initscr()
    curses.curs_set(0)
    curses.update_lines_cols()
    curses.wrapper(draw)
