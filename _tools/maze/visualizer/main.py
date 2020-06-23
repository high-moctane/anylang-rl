import os.path as opath
import sys


abs_file = opath.dirname(__file__)

maze = []
maze_path = opath.join(abs_file, "..", "..", "..", "_settings", "maze.txt")
with open(maze_path) as f:
    for line in f:
        maze.append(list(line.rstrip()))

history_path = sys.argv[1]

with open(history_path) as f:
    for line in f:
        line = line.rstrip()
        pos = eval(line.split("\t")[3])
        if 0 <= pos[0] < len(maze) and 0 <= pos[1] < len(line):
            maze[pos[0]][pos[1]] = "*"

maze[1][1] = "S"
maze[-2][-2] = "G"

res = "\n".join("".join(line) for line in maze)
print(res)
