import os.path as opath
import sys

OUTPUT_FNAME = "route.txt"

maze = []
maze_path = opath.join(opath.dirname(__file__),
                       "..", "..", "..", "_settings", "maze.txt")
history_path = sys.argv[1]
outout_path = opath.join(opath.dirname(history_path), OUTPUT_FNAME)

with open(maze_path) as f:
    for line in f:
        maze.append(list(line.rstrip()))

with open(history_path) as f:
    for line in f:
        pos = tuple(map(int, line.split()[3].split(",")))
        if 0 <= pos[0] < len(maze) and 0 <= pos[1] < len(line):
            maze[pos[0]][pos[1]] = "*"

maze[1][1] = "S"
maze[-2][-2] = "G"

res = "\n".join("".join(line) for line in maze)
with open(outout_path, mode="w") as f:
    f.write(res)
