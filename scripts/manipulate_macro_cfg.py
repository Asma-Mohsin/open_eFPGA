#!/usr/bin/env python3
import math

#TODO: Improve this script so e.g. arguments can be given from the command line


# ignore_strings = ["BlockRAM", "cvxif_pau", "data_mem", "LUT4AB", "W_IO"]
# ignore_strings = ["BlockRAM", "cvxif_pau", "data_mem"]
ignore_strings = []

def rotate(origin, point, angle):
    """
    Rotate a point counterclockwise by a given angle around a given origin.

    The angle should be given in radians.
    """
    ox, oy = origin
    px, py = point

    qx = ox + math.cos(angle) * (px - ox) - math.sin(angle) * (py - oy)
    qy = oy + math.sin(angle) *  (px - ox) + math.cos(angle) * (py - oy)
    return qx, qy

def read_tiles(file_path):
    """
    Reads the input file and extracts tile information into a list of dictionaries.

    Parameters:
        file_path (str): Path to the input file.

    Returns:
        list: A list of dictionaries with tile data (e.g., [{'name': value, 'x': value, ...}]).
    """
    tiles = []
    with open(file_path, 'r') as f:
        lines = f.readlines()
        for line in lines:
            if line.strip() and not line.startswith(" "):
                parts = line.strip().split()
                name = parts[0]
                x, y = map(float, parts[1:3])  # Assuming x, y coordinates are the 2nd and 3rd columns
                flip = parts[3]
                tiles.append({'name': name, 'x': x, 'y': y, "flip": flip})
    return tiles

def print_tiles(tiles):
    """
    Prints the tile data in a readable format.

    Parameters:
        tiles (list): A list of dictionaries with tile data.
    """
    for tile in tiles:
        print(f"TILE name: {tile['name']} x: {tile['x']}, y: {tile['y']}, flip: {tile['flip']}")

def rotate_tiles(tiles, origin, angle_degrees):
    """
    Rotates all tiles around a given origin by a specified angle.

    Parameters:
        tiles (list): A list of dictionaries with tile data.
        origin (tuple): The (x, y) coordinates of the rotation origin.
        angle_degrees (float): The rotation angle in degrees.

    Returns:
        list: A list of rotated tile data.
    """
    # Convert the angle from degrees to radians
    angle = math.radians(angle_degrees)
    
    for tile in tiles:
        if any(ignore_string in tile["name"] for ignore_string in ignore_strings):
            continue
        flip = "N"
        x, y = rotate(origin, (tile["x"], tile["y"]), angle)
        x += 2000
        tile.update({"x": x, "y": y, "flip": flip})
    
    return tiles

def move_tiles(tiles, x_offset, y_offset):
    for tile in tiles:
        if any(ignore_string in tile["name"] for ignore_string in ignore_strings):
            continue
        x = tile["x"] + x_offset
        y = tile["y"] + y_offset
        tile.update({"x": x, "y": y})
    return tiles


def change_space_between_tiles_vertical(tiles, space, start_bot=True):
    """
    Adjusts the vertical space between tiles in each row.

    Parameters:
        tiles (list): A list of dictionaries containing tile data.
        space (float): The amount of space to add between tiles vertically.
        start_top (bool): Whether to start adjusting from the topmost row (True)
                          or the bottommost row (False).

    Returns:
        list: The modified list of tiles with updated y-coordinates.
    """
    # Group tiles by their y-coordinate (rows)
    rows = {}
    for tile in tiles:
        if any(ignore_string in tile["name"] for ignore_string in ignore_strings):
            continue
        y = tile['y']
        if y not in rows:
            rows[y] = []
        rows[y].append(tile)
    sorted_rows = sorted(rows.keys(), reverse=not start_bot)
    print(sorted_rows)

    # Update the horizontal spacing for each column
    y_offset = 0
    for column_x in sorted_rows:
        for tile in sorted(rows[column_x], key=lambda t: t['x']):
            if any(ignore_string in tile["name"] for ignore_string in ignore_strings):
                continue

            if start_bot:
                tile['y'] += y_offset
            else:
                tile['y'] -= y_offset

        y_offset += space  # Increment the x_offset by the space value

    return tiles


def change_space_between_tiles_horizontal(tiles, space, start_left=True):
    """
    Adjusts the horizontal space between tiles in each column.

    Parameters:
        tiles (list): A list of dictionaries containing tile data.
        space (float): The amount of space to add between tiles horizontally.
        start_top (bool): Whether to start adjusting from the topleftmost column (True)
                          or the bottommost column (False).

    Returns:
        list: The modified list of tiles with updated x-coordinates.
    """
    # Group tiles by their y-coordinate (rows)
    rows = {}
    for tile in tiles:
        if any(ignore_string in tile["name"] for ignore_string in ignore_strings):
            continue
        x = tile['x']
        if x not in rows:
            rows[x] = []
        rows[x].append(tile)
    sorted_rows = sorted(rows.keys(), reverse=not start_left)
    print(sorted_rows)

    # Update the horizontal spacing for each column
    x_offset = 0
    for column_x in sorted_rows:
        for tile in sorted(rows[column_x], key=lambda t: t['y']):
            if any(ignore_string in tile["name"] for ignore_string in ignore_strings):
                continue

            if start_left:
                tile['x'] += x_offset
            else:
                tile['x'] -= x_offset

        x_offset += space  # Increment the x_offset by the space value

    return tiles

def write_tiles_to_file_flip(tiles, file_path):
    """
    Writes the tile data to a specified file.

    Parameters:
        tiles (list): A list of dictionaries with tile data.
        file_path (str): Path to the output file.
    """
    with open(file_path, "w") as f:
        for tile in tiles:
            if tile['flip'] == "N":
                line = f"{tile['name']} {tile['x']} {tile['y']} W\n"
            else:
                line = f"{tile['name']} {tile['x']} {tile['y']} {tile['flip']}\n"
            f.write(line)

def write_tiles_to_file(tiles, file_path):
    """
    Writes the tile data to a specified file.

    Parameters:
        tiles (list): A list of dictionaries with tile data.
        file_path (str): Path to the output file.
    """
    with open(file_path, "w") as f:
        for tile in tiles:
            line = f"{tile['name']} {int(tile['x'])} {int(tile['y'])} {tile['flip']}\n"
            f.write(line)

def main():
    #TODO: add these as command line parameters
    input_path = "../openlane/user_project_wrapper/macro_tmp_test.cfg"  # Path to your input configuration file
    output_path = "../openlane/user_project_wrapper/macro_shifted_test.cfg"
    # origin = (2400, 245)  # Rotation origin (x, y)
    origin = (150, 50)  # Rotation origin (x, y)
    angle = -90  # Rotation angle in degrees
    x_offset = 100
    y_offset = 100
    x_space = 5
    y_space = 100

    # Read the tiles from the input file
    tiles = read_tiles(input_path)

    tiles = change_space_between_tiles_horizontal(tiles, x_space, False)
    print_tiles(tiles)
    # move_tiles(tiles, x_offset, y_offset)

    # Rotate the tiles around the given origin
    # tiles = rotate_tiles(tiles, origin, angle)

    # Write the rotated tiles to the output file
    write_tiles_to_file(tiles, output_path)

if __name__ == "__main__":
    main()
