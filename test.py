

import curses_tools as tools





def main():
    trash_files = ['duck.txt', 'hubble.txt', 'lamp.txt', 'trash_large.txt', 'trash_small.txt', 'trash_xl.txt']
    trash_frames = []
    for trash in trash_files:
        with open(trash, "r") as my_file:
            trash_frames.append(my_file.read())
    for trash in trash_frames:
        frame_height, frame_width = tools.get_frame_size(trash)
        print(frame_height, frame_width)


if __name__ == '__main__':
    main()