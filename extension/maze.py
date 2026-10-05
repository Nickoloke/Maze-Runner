def create_maze(width: int = 5, height: int = 5) -> dict:
    maze = {"height" : height, "width" : width, "horizontal_walls" : [], "vertical_walls" : []}
    return maze

def add_horizontal_wall(maze: dict, x_coordinate: int, horizontal_line: int) -> dict:
    maze["horizontal_walls"].append((x_coordinate, horizontal_line))
    return maze

def add_vertical_wall(maze: dict, y_coordinate: int, vertical_line: int) -> dict:
    maze["vertical_walls"].append((vertical_line, y_coordinate))
    return maze

def get_dimensions(maze: dict) -> tuple[int, int]:
    return maze["width"], maze["height"]

def get_walls(maze: dict, x_coordinate: int, y_coordinate: int) -> tuple[bool, bool, bool, bool]:
    north = ((x_coordinate, y_coordinate + 1) in maze["horizontal_walls"]) or (y_coordinate == maze["height"] - 1)
    east = ((x_coordinate + 1, y_coordinate) in maze["vertical_walls"]) or (x_coordinate == maze["width"] - 1)
    south = ((x_coordinate, y_coordinate) in maze["horizontal_walls"]) or (y_coordinate == 0)
    west = ((x_coordinate, y_coordinate) in maze["vertical_walls"]) or (x_coordinate == 0)
    return north, east, south, west