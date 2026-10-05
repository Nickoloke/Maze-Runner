from maze import get_walls
from typing import Optional

class Runner:
    def __init__(self, x, y, orientation):
        self.x = x
        self.y = y
        self.orientation = orientation

def create_runner(x: int = 0, y: int = 0, orientation: str = "N") -> Runner:
    return Runner(x, y, orientation)

def get_x(runner: Runner) -> int:
    return runner.x

def get_y(runner: Runner) -> int:
    return runner.y

def get_orientation(runner: Runner) -> str:
    return runner.orientation

def turn(runner: Runner, direction: str) -> Runner:
    turns = {"Left": {"N": "W", "W": "S", "S": "E", "E": "N"}, "Right": {"N": "E", "E": "S", "S": "W", "W": "N"}}
    runner.orientation = turns[direction][runner.orientation]
    return runner

def forward(runner: Runner) -> Runner:
    if runner.orientation == "N":
        runner.y += 1
    elif runner.orientation == "E":
        runner.x += 1
    elif runner.orientation == "S":
        runner.y -= 1
    elif runner.orientation == "W":
        runner.x -= 1
    return runner

def sense_walls(runner: Runner, maze: dict) -> tuple[bool, bool, bool]:
    values = get_walls(maze, runner.x, runner.y)
    if runner.orientation == "N":
        return tuple(values[i] for i in [3,0,1])
    elif runner.orientation == "E":
        return tuple(values[i] for i in [0,1,2])
    elif runner.orientation == "S":
        return tuple(values[i] for i in [1,2,3])
    elif runner.orientation == "W":
        return tuple(values[i] for i in [2,3,0])
    else:
        raise ValueError("Orientation is incorrect")

def go_straight(runner: Runner, maze: dict) -> Runner:
    if not sense_walls(runner, maze)[1]:
        if runner.orientation == "N":
            runner.y += 1
        elif runner.orientation == "E":
            runner.x += 1
        elif runner.orientation == "S":
            runner.y -= 1
        elif runner.orientation == "W":
            runner.x -= 1
    else:
        raise ValueError("Wall in front of the runner")
    return runner

def move(runner: Runner, maze: dict) -> tuple[Runner, str]:
    left_wall, front_wall, right_wall = sense_walls(runner, maze)
    if not left_wall:
        turn(runner, "Left")
        go_straight(runner, maze)
        return runner, "LF"
    elif not front_wall:
        go_straight(runner, maze)
        return runner, "F"
    elif not right_wall:
        turn(runner, "Right")
        go_straight(runner, maze)
        return runner, "RF"
    else:
        turn(runner, "Right")
        turn(runner, "Right")
        go_straight(runner, maze)
        return runner, "B"

def explore(runner : Runner, maze : dict, goal : Optional[tuple[int, int]]) -> list[tuple[int, int, str]]:
    if goal is None:
        goal = (maze["width"] - 1, maze["height"] - 1)
    list_moves = []
    while get_x(runner) != goal[0] or get_y(runner) != goal[1]:
        x = get_x(runner)
        y = get_y(runner)
        runner, action = move(runner, maze)
        list_moves.append((x,y,action))
    return  list_moves


