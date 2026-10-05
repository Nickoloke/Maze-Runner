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
        raise ValueError("Unknown orientation")

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
        raise ValueError("Wall in front of runner")
    return runner


def explore(runner: Runner, maze: dict, goal: Optional[tuple[int, int]]):
    if goal is None:
        goal = (maze["width"] - 1, maze["height"] - 1)

    # Uses a stack to store path history for backtracks
    stack = [(runner.x, runner.y, runner.orientation, [])]
    # Keeps track of visited coordinates
    visited = set()
    # Keeps track of how many points have been explored
    explored = 0
    while stack:
        # Pops the last element
        x, y, orientation, path = stack.pop()

        # Checks if it's the goal
        if (x, y) == goal:
            return path,explored

        # Checks if we have already processed this point
        if (x, y) in visited:
            continue

        # Marks as visited and increases point counter
        visited.add((x, y))
        explored += 1

        # Retrieves wall information around point
        walls = get_walls(maze, x, y)

        right_turns = {"N": "E", "E": "S", "S": "W", "W": "N"}
        left_turns = {"N": "W", "W": "S", "S": "E", "E": "N"}

        if not walls[0]: # Checks North
            if (x, y + 1) not in visited:
                # Calculate the move action required to go North
                target = "N"

                action = "F"

                if orientation == target:
                    action = "F"
                elif right_turns[orientation] == target:
                    action = "RF"
                elif left_turns[orientation] == target:
                    action = "LF"
                else:
                    action = "B"

                # Add to stack
                new_path = path + [(x, y, action)]
                stack.append((x, y + 1, target, new_path))


        if not walls[1]: # Checks east
            if (x + 1, y) not in visited:
                target = "E"
                action = "F"

                if orientation == target:
                    action = "F"
                elif right_turns[orientation] == target:
                    action = "RF"
                elif left_turns[orientation] == target:
                    action = "LF"
                else:
                    action = "B"

                new_path = path + [(x, y, action)]
                stack.append((x + 1, y, target, new_path))

        if not walls[2]: # Checks south
            if (x,y - 1) not in visited:
                target = "S"
                action = "F"

                if orientation == target:
                    action = "F"
                elif right_turns[orientation] == target:
                    action = "RF"
                elif left_turns[orientation] == target:
                    action = "LF"
                else:
                    action = "B"

                new_path = path + [(x, y, action)]
                stack.append((x, y - 1, target, new_path))

        if not walls[3]: # Checks west
            if (x - 1, y) not in visited:
                target = "W"
                action = "F"

                if orientation == target:
                    action = "F"
                elif right_turns[orientation] == target:
                    action = "RF"
                elif left_turns[orientation] == target:
                    action = "LF"
                else:
                    action = "B"

                new_path = path + [(x, y, action)]
                stack.append((x - 1, y, target, new_path))
    return [], explored



