



import os






def main():
    trash_frames = []
    path = os.path.join('trash_s_frames')
    for filename in os.listdir(path):
        with open(os.path.join(path, filename), "r") as my_file:
            trash_frames.append(my_file.read())


if __name__ == '__main__':
    main()