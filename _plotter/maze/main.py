import os.path as opath
import sys


def maze_file_path():
    return opath.join(
        opath.abspath(opath.dirname(__file__)),
        "..",
        "..",
        "_config",
        "maze.txt"
    )


def read_maze(path):
    res = []
    with open(path) as f:
        for line in f:
            res.append(list(line.rstrip()))
    return res


def parse_history(path):
    res = []
    with open(path) as f:
        for line in f:
            pos = line.rstrip().split("\t")[3]
            res.append(tuple(map(int, pos.split(","))))
    return res


def draw_trace(maze, history):
    for pos in history:
        maze[pos[0]][pos[1]] = "*"


def draw_start(maze):
    maze[1][1] = "S"


def draw_goal(maze):
    maze[-2][-2] = "G"


def format_maze(maze):
    lines = list(map(lambda x: "".join(x), maze))
    return "\n".join(lines)


if __name__ == "__main__":
    path = maze_file_path()
    maze = read_maze(path)
    history = parse_history(sys.argv[1])
    draw_trace(maze, history)
    draw_start(maze)
    draw_goal(maze)
    maze_string = format_maze(maze)
    print(maze_string)
