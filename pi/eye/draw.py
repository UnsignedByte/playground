# Utils to draw eye images
import numpy as np

# direction mapping
dirs = [
    (0, 0),  # Center
    (0, -1),  # Up
    (1, 0),  # Right
    (0, 1),  # Down
    (-1, 0),  # Left
]

# Eye outline
outline = np.array(
    [
        [0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0],
        [0, 0, 1, 1, 0, 0, 0, 1, 1, 0, 0],
        [0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0],
        [0, 0, 1, 1, 0, 0, 0, 1, 1, 0, 0],
        [0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0],
    ]
)

pupil = np.array([[0, 1, 0], [1, 1, 1], [0, 1, 0]])

eyeh, eyew = outline.shape


# Drawing tools for the eye images
def draw_eye(image: np.array, x: int, y: int, eye: int):

    # Eyes are spaced 1 pixel apart horizontally
    x *= eyew + 1
    # If y is odd, offset the x position by half the width
    x += (eyew // 2 + 1) * (y % 2)
    # Eyes are spaced with 1 pixel of overlap vertically
    y *= eyeh - 1

    # Draw the outline
    image[y : y + eyeh, x : x + eyew] += outline

    # Draw the pupil in the right direction
    dx, dy = dirs[eye]
    cx, cy = x + eyew // 2, y + eyeh // 2
    image[cy + dy - 1 : cy + dy + 2, cx + dx - 1 : cx + dx + 2] += pupil


def draw_message(msg: list[list[int]]):
    # Create a blank image
    image = np.zeros(
        (
            (eyeh - 1) * len(msg) + 1,
            ((eyew + 1) * max(2 * len(m) + (y % 2) for y, m in enumerate(msg))) // 2
            - 1,
        ),
        dtype=int,
    )

    # Draw the message
    for y, row in enumerate(msg):
        for x, eye in enumerate(row):
            draw_eye(image, x, y, eye)

    return image
