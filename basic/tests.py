from runner import *
from maze_runner import *
from maze import *
import pytest

def test_create_maze_get_dimensions() -> None:
    """A Unit test for :py:func:`~maze.create_maze` and
    :py:func:`~maze.get_dimensions`.

    Below is the test sequence:

    1. Create a maze of size (11, 5).

    2. Assert the width (11) and height (5) of the newly created maze.
    created runner.
    """
    maze = create_maze(11, 5)
    width, height = get_dimensions(maze)
    assert width == 11
    assert height == 5


def test_create_maze_get_walls() -> None:
    """A Unit test for :py:func:`~maze.create_maze` and
    :py:func:`~maze.get_walls`

    Below is the test sequence:

    1. Create a maze of size (11, 5).

    2. Assert that there are no walls at the (4, 2)-coordinate.
    """
    maze = create_maze(11, 5)
    assert get_walls(maze, 4, 2) == (False, False, False, False)


def test_add_horizontal_wall() -> None:
    """A Unit test for :py:func:`~maze.add_horizontal_wall` and
    :py:func:`~maze.get_walls`

    Below is the test sequence:

    1. Create a maze of size (11, 5).

    2. Add a horizontal wall at (5, 2).

    4. Assert that there are no walls at the (5, 2)-coordinate, except the South.
    """
    maze = create_maze(11, 5)
    maze = add_horizontal_wall(maze, 5, 2)

    assert get_walls(maze, 5, 2) == (False, False, True, False)


def test_add_vertical_wall() -> None:
    """A Unit test for :py:func:`~maze.add_vertical_wall` and
    :py:func:`~maze.get_walls`

    Below is the test sequence:

    1. Create a maze of size (11, 5).

    2. Add a vertical wall at (2, 4).

    3. Assert that there are no walls at the (4, 2)-coordinate, except the West.
    """
    maze = create_maze(11, 5)
    maze = add_vertical_wall(maze, 2, 4)
    assert get_walls(maze, 4, 2) == (False, False, False, True)


def test_runner_sense_walls() -> None:
    """A Unit test for :py:func:`~runner.sense_walls`

    Below is the test sequence:

    1. Create a maze of size (11, 5).

    2. Add a horizontal wall at (5, 2).

    3. Add a runner at (5, 2) facing East

    4. Assert that the runner sense no walls on the left and in the front, but
    there is a wall on the right.
    """
    maze = create_maze(11, 5)
    maze = add_horizontal_wall(maze, 5, 2)
    runner = create_runner(5, 2, "E")
    assert sense_walls(runner, maze) == (False, False, True)


def test_runner_go_straight() -> None:
    """A Unit test for :py:func:`~runner.go_straight`

    Below is the test sequence:

    1. Create a maze of size (11, 5).

    2. Add a horizontal wall at (5, 2).

    3. Add a runner at (5, 2) facing East

    4. Let the runner go straight

    4. Assert that the runner is at (6, 2)
    """
    maze = create_maze(11, 5)
    maze = add_horizontal_wall(maze, 5, 2)

    runner = create_runner(5, 2, "E")

    runner = go_straight(runner, maze)

    assert get_x(runner) == 6
    assert get_y(runner) == 2


def test_move() -> None:
    """A Unit test for :py:func:`~runner.move`

    Below is the test sequence:

    1. Create a maze of size (11, 5).

    2. Add a horizontal wall at (5, 2).

    3. Add a runner at (5, 2) facing South (toward the wall)

    4. Let the runner move and get the (new) runner and the actions.

    5. Assert that the new runner is at (6, 2) facing East

    6. Assert that the actions to get there were LF
    """
    maze = create_maze(11, 5)

    maze = add_horizontal_wall(maze, 5, 2)

    runner = create_runner(5, 2, "S")

    runner, actions = move(runner, maze)

    assert (get_x(runner), get_y(runner)) == (6, 2), f"Incorrect move for runner"
    assert get_orientation(runner) == "E"

    assert actions == "LF"

def test_explore() -> None:
    """
    The test for :py:func:~runner.explore should be similar to test_move() above
    ()i.e., replaying the action to see if a test runner can follow the action to
    get to the target destination. This will be left as an exercise for any keen
    testers.
    """
    pass

def test_create_runner() -> None:
    """A Unit test for :py:func:`~runner.create_runner`

    Below is the test sequence:

    1. Create a runner at position (1,2), facing South.

    2. Assert the x, y positions (1, 2), and the orientation ("S") of the newly
    created runner.
    """
    runner = create_runner(1, 2, "S")
    assert get_x(runner) == 1
    assert get_y(runner) == 2
    assert get_orientation(runner) == "S"


def test_turn() -> None:
    """A Unit test for :py:func:`~runner.turn`

    Below is the test sequence:

    1. Create a runner at position (1,2), facing South.

    2. Let the runner turn to the Left.

    3. Assert the x, y positions (1, 2), and the orientation ("E") of the runner.
    """
    runner = create_runner(1, 2, "S")
    runner = turn(runner, "Left")
    assert get_x(runner) == 1
    assert get_y(runner) == 2
    assert get_orientation(runner) == "E"


def test_forward() -> None:
    """A Unit test for :py:func:`~runner.forward`

    Below is the test sequence:

    1. Create a runner at position (1,2), facing South.

    2. Let the runner more forward.

    3. Assert the x, y positions (1, 1), and the orientation ("S") of the runner.
    """
    runner = create_runner(1, 2, "S")
    runner = forward(runner)
    assert get_x(runner) == 1
    assert get_y(runner) == 1
    assert get_orientation(runner) == "S"

def test_shortest_path() -> None:
    """A Unit test for :py:func:`~maze_runner.shortest_path`

    Below is the test sequence:

    1. Create a maze of size (11, 5).

    2. Add a horizontal wall at (0, 1).

    3. Add a vertical wall at (1, 1).

    4. Run short_path function to get the path (with default start and goal).

    5. Check that the result is a valid path, starting from (0,0) and end at
       (10, 4).
    """
    maze = create_maze(11, 5)
    maze = add_horizontal_wall(maze, 0, 1)
    maze = add_vertical_wall(maze, 1, 1)
    path = shortest_path(maze)
    assert path[0] == (0, 0, "RF")
    assert path[-1] == (9, 4, "F")
    prefix = []
    for location in path:
        x, y, a = location
        assert (x, y) not in prefix, f"{location} is repeated"
        prefix.append((x, y))
