# Python Maze Runner

A pathfinding simulation that goes through text-based mazes and calculates the shortest path using different algorithms, and outputs the resulting data. The project uses Python to manage grid states, runner orientation, and collision detection.

## Project Structure
*   `basic/`: Contains the core maze logic (`maze.py`), the runner mechanics (`runner.py`), the main execution script (`maze_runner.py`), and the `pytest` suite (`tests.py`).
*   `extension/`: Contains advanced algorithms and additional features.

## Features
*   **Text-Processing Parser:** Validates and translates `.mz` text files into a mathematical grid, plotting horizontal and vertical walls.
*   **Path Optimisation:** The runner explores the maze and automatically strips redundant loops from its visited coordinates to output the true shortest path.
*   **Automated Reporting:** Outputs an `exploration.csv` containing step-by-step coordinates and actions, alongside a `statistics.txt` file detailing the exploration score.

## Requirements
*   Python
*   Pytest (for running the unit tests, optional)

## Usage

Navigate to the directory containing `maze_runner.py` and run the script from your terminal.

**Positional Arguments:**
*   `maze`: The path to the maze file you want to solve (e.g., `maze1.mz`).

**Optional Arguments:**
*   `--starting`: The (x, y) starting coordinates (defaults to `0, 0`).
*   `--goal`: The (x, y) goal coordinates (defaults to the top right corner based on maze dimensions).
### Example Commands
Run with default start and goal positions:
```bash
python maze_runner.py maze1.mz
```
Run with custom starting goal positions
```bash
python maze_runner.py maze1.mz --starting "2, 1" --goal "4, 5"
```
The core logic is covered by a suite of unit tests. To verify the integrity of the maze generation and runner mechanics, simply run:
```bash
pytest tests.py
```