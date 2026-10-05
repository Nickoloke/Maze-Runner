from runner import create_runner,explore
from maze import create_maze,add_horizontal_wall,add_vertical_wall,get_dimensions
from typing import Optional
import argparse
import csv

def shortest_path(maze : dict, starting: Optional[tuple[int, int]] = None, goal: Optional[tuple[int, int]] = None, filename: str = "Unknown file") -> list[tuple[int, int, str]]:
    if starting is None:
        starting = (0, 0)
    if goal is None:
        goal = (maze["width"] - 1, maze['height'] - 1)
    runner1 = create_runner(starting[0],starting[1],"N")
    path = explore(runner1,maze, goal)
    visited_coordinates = []
    visited_full = []
    for step in path:
        x,y,movement = step
        if (x,y) not in visited_coordinates:
            visited_coordinates.append((x,y))
            visited_full.append(step)
        else:
            loop = visited_coordinates.index((x,y))
            visited_coordinates = visited_coordinates[0:loop + 1]
            visited_full = visited_full[0:loop + 1]
            visited_full[-1] = (x, y, movement)
    rows = []
    step = 1
    for x,y,action in path:
        rows.append({"Step":step,"x-coordinate":x,"y-coordinate":y,"Actions":action})
        step += 1
    with open("exploration.csv", "w", newline="") as csvfile:
        fieldnames = ["Step","x-coordinate","y-coordinate","Actions"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    exploration_steps = len(path)
    path_length = len(visited_full) + 1
    score = float(exploration_steps / 4 + path_length)
    with open("statistics.txt", "w", newline="") as file:
        file.write(f"{filename}\n")
        file.write(f"{score}\n")
        file.write(f"{exploration_steps}\n")
        file.write(f"{visited_full}\n")
        file.write(f"{path_length}\n")
    return visited_full

def maze_reader(maze_file: str) -> dict:
    try:
        with open(maze_file, "r") as file:
            lines = file.readlines()
            lines = [line.strip() for line in lines]
            width = (len(lines[0]) - 1) // 2
            height = (len(lines) - 1) // 2
            if not lines:
                raise ValueError(f"{maze_file} is not a valid maze")
            for i in range(0, len(lines)):
                if len(lines[i]) != len(lines[0]):
                    raise ValueError(f"{maze_file} is not a valid maze")
            for i in range(0,len(lines[0])):
                if lines[0][i] != "#":
                    raise ValueError(f"{maze_file} is not a valid maze")
            for i in range(0,len(lines[-1])):
                if lines[-1][i] != "#":
                    raise ValueError(f"{maze_file} is not a valid maze")
            for i in range(0,len(lines)):
                if lines[i][0] != "#":
                    raise ValueError(f"{maze_file} is not a valid maze")
                if lines[i][-1] != "#":
                    raise ValueError(f"{maze_file} is not a valid maze")
                for j in range(0,len(lines[0])):
                    if not lines[i][j] == "#" and not lines[i][j] == ".":
                        raise ValueError(f"{maze_file} is not a valid maze")

            maze1 = create_maze(width, height)
            for line in range(1, len(lines) - 1):
                if line % 2 == 0:
                    for column in range(1, len(lines[line]) - 1, 2):
                        if lines[line][column] == "#":
                            add_horizontal_wall(maze1, (column - 1) // 2, (height - 1) - ((line - 2) // 2))
                else:
                    for column in range(2, len(lines[line]) - 1, 2):
                        if lines[line][column] == "#":
                            add_vertical_wall(maze1, (height - 1) - ((line - 1) // 2), column // 2)
            return maze1
    except IOError as error:
        raise IOError(f"Error reading file {maze_file}") from error

def input_changer(position: str) -> tuple[int, int]:
    try:
        position = position.split(',')
        if len(position) != 2:
            raise ValueError
        x = int(position[0])
        y = int(position[1])
        return x,y
    except ValueError:
        raise ValueError(f"Position must be valid and in format of x, y")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="ECS Maze Runner")
    parser.add_argument("maze", help="The name of the maze file, e.g., maze1.mz")
    parser.add_argument("--starting", help="The starting position, e.g., \"2, 1\"")
    parser.add_argument("--goal", help="The goal position, e.g., \"4, 5\"")
    args = parser.parse_args()

    try:
        maze1 = maze_reader(args.maze)
        width, height = get_dimensions(maze1)
        start_position = None
        if args.starting:
            start_position = input_changer(args.starting)
        goal_position = None
        if args.goal:
            goal_position = input_changer(args.goal)
        if start_position:
            if not (0 <= start_position[0] < width and 0 <= start_position[1] < height):
                raise ValueError(f"Starting position {start_position} is out of bounds")
        if goal_position:
            if not (0 <= goal_position[0] < width and 0 <= goal_position[1] < height):
                raise ValueError(f"Goal position {goal_position} is out of bounds")
        path = shortest_path(maze1, start_position, goal_position,args.maze)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")