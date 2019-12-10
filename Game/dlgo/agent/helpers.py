from dlgo.gotypes import Point

__all__ = [
    'is_point_an_eye',
]

# Detect eyes
def is_point_an_eye(board, point, color):
    # Occupied point
    if board.get(point) is not None:
        return False

    # All neighbours are friendly
    for neighbor in point.neighbors():
        # Out of board
        if board.is_on_grid(neighbor):
            neighbor_color = board.get(neighbor)
            if neighbor_color != color:
                return False
    
    # Control 3 out of 4 corners if the point in the middle of the board
    # Control all corners if the point on the edge
    friendly_corners = 0
    off_board_corners = 0
    corners = [
        Point(point.row - 1, point.col - 1),
        Point(point.row - 1, point.col + 1),
        Point(point.row + 1, point.col - 1),
        Point(point.row + 1, point.col + 1),
    ]

    for corner in corners:
        if board.is_on_grid(corner):
            corner_color = board.get(corner)
            if corner_color == color:
                friendly_corners += 1
            else:
                off_board_corners += 1
    
    # If the point on the edge or the corner
    if off_board_corners > 0:
        return off_board_corners + friendly_corners == 4
    # Normal point
    return friendly_corners >= 3